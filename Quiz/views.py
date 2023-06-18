from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from .models import Review, Testing, Question, Section, Lesson, Result
from .serializers import UserSerializer, ReviewSerializer, TestingSerializer, QuestionSerializer, SectionSerializer, \
    LessonSerializer, ResultSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


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
    serializer_class = SectionSerializer
    permission_classes = [AllowAny]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]


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