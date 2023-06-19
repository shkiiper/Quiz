from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from .models import Review, Testing, Question, Section, Lesson, Result
from .serializers import UserSerializer, ReviewSerializer, TestingSerializer, QuestionSerializer, SectionSerializer, \
    LessonSerializer, ResultSerializer, SectionReadOnlySerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# Данный код представляет собой класс TokenObtainPairView, который является представлением (view) веб-приложения, написанного с использованием фреймворка Django
# и его модуля Django REST Framework. Давайте разберем его поэтапно:
# В начале класса определены разрешения (permissions) для доступа к данному представлению. В данном случае указано [AllowAny], что означает,
# что любой пользователь имеет право доступа к этому представлению.
# Метод get_extra_actions(self) возвращает пустой список дополнительных действий. В данном коде он не используется.
# Метод post(self, request) обрабатывает HTTP POST запросы, которые отправляются на данное представление. Он получает имя пользователя (username) и пароль (password) из данных запроса (request.data).
# Затем происходит аутентификация пользователя с помощью функции authenticate, которая проверяет предоставленные имя пользователя и пароль.
# Если пользователь существует и данные аутентификации верны, то выполняются следующие действия.
# Создается объект RefreshToken с использованием функции RefreshToken.for_user(user). Объект RefreshToken представляет токен обновления (refresh token), который может быть использован для получения нового доступного токена (access token).
# Значения access token и refresh token приводятся к строковому формату (str(refresh.access_token) и str(refresh)).
# Затем сериализуется объект пользователя (user) с использованием UserSerializer. Сериализация представляет процесс преобразования объекта Python в формат данных, который может быть легко передан через сеть или сохранен в базе данных.
# Данные пользователя полученные в результате сериализации (serializer.data) сохраняются в переменной user_data.
# Создается словарь response_data, содержащий значения access token, refresh token и данные пользователя.
# В случае успешной аутентификации, возвращается HTTP-ответ (Response) с данными response_data.
# Если аутентификация не прошла успешно (например, неверные учетные данные), возвращается HTTP-ответ с сообщением об ошибке ({'error': 'Invalid credentials'}) и статусом 400 (Bad Request).
# Этот код реализует точку входа API для получения пары токенов (access token и refresh token) в обмен на правильные учетные данные пользователя. Такой подход широко используется для аутентификации и авторизации пользователей в веб-приложениях.
class TokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def get_extra_actions(self):
        return []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            serializer = UserSerializer(user)
            user_data = serializer.data

            response_data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user_data
            }
            return Response(response_data)
        else:
            return Response({'error': 'Invalid credentials'}, status=400)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]


class TestingViewSet(viewsets.ModelViewSet):
    queryset = Testing.objects.all()
    serializer_class = TestingSerializer
    permission_classes = [AllowAny]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SectionSerializer
        elif self.request.method == 'GET':
            return SectionReadOnlySerializer
        return SectionSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]


# этот класс был демо версией Result
class PerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sections = Section.objects.all()
        data = []

        for section in sections:
            testing = section.test
            total_question = testing.total_question
            total_correct_answer = testing.total_correct_answer

            data.append({
                'id': request.user.id,
                'name': section.name,
                'status': section.status,
                'total_question': total_question,
                'total_correct_answer': total_correct_answer
            })

        return Response(data)


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
