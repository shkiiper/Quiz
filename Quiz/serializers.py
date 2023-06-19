from rest_framework import serializers
from django.contrib.auth import get_user_model

from Quiz.models import Review, Question, Testing, Section, Lesson, Result

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_photo', 'is_teacher', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'review_text', ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class TestingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testing
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'duration', 'picture', 'photo_material', 'video', 'document']


class SectionSerializer(serializers.ModelSerializer):
    material = LessonSerializer(read_only=True)
    test = TestingSerializer(read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'description', 'picture', 'test', 'material', 'status']


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'user', 'section', 'section_name', 'status', 'total_question', 'total_correct_answer']
