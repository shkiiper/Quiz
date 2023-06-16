from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    sections = models.ManyToManyField('Section', related_name='users', blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    def __str__(self):
        return self.username


class Section(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='section_photos/', null=True, blank=True)
    test = models.OneToOneField('Testing', on_delete=models.CASCADE, blank=True, null=True)
    material = models.OneToOneField('Lesson', on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=False)


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='section_photos/', null=True, blank=True)
    photo_material = models.ImageField(upload_to='photo_material_photos/', null=True, blank=True)
    video = models.FileField(upload_to='section_videos/', null=True, blank=True)
    document = models.FileField(upload_to='section_documents/', null=True, blank=True)


class Testing(models.Model):
    total_question = models.IntegerField(default=0)
    total_correct_answer = models.IntegerField(default=0)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    choice1 = models.CharField(max_length=200, default='вариант')
    choice2 = models.CharField(max_length=200, default='вариант')
    choice3 = models.CharField(max_length=200, default='вариант')
    correct_answer = models.CharField(max_length=200)
    user_answer = models.CharField(max_length=200, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    test = models.ForeignKey('Testing', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.question_text

    def save(self, *args, **kwargs):
        if self.correct_answer == self.user_answer:
            self.is_correct = True
        super().save(*args, **kwargs)

        testing = self.test
        testing.total_question = Question.objects.filter(test=testing).count()
        testing.total_correct_answer = Question.objects.filter(test=testing, is_correct=True).count()
        testing.save()

        if testing.total_correct_answer >= 10:
            section = testing.section
            section.status = True
            section.save()


class Review(models.Model):
    review_text = models.TextField()

    def __str__(self):
        return self.review_text
