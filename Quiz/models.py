from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

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
        if self.correct_answer == self.user_answer: #Проверяется, совпадает ли значение correct_answer с user_answer объекта Question.
            # Если да, то устанавливается значение is_correct в True, иначе остается False.
            self.is_correct = True
        super().save(*args, **kwargs)

        testing = self.test #Получается связанный объект Testing через поле test.
        testing.total_question = Question.objects.filter(test=testing).count() #Выполняются запросы к базе данных для подсчета общего количества вопросов
        testing.total_correct_answer = Question.objects.filter(test=testing, is_correct=True).count() #и общего количества правильных ответов
        testing.save()

        if testing.total_correct_answer >= 10: #Если total_correct_answer в объекте Testing больше или равно 10, то устанавливается status в True для связанного объекта Section.
            section = testing.section
            section.status = True
            section.save()

        current_user = User.objects.first() #получаем текущего пользователя
        if current_user:
            section = testing.section # получаем id текушего раздела
            result, created = Result.objects.get_or_create(
                #Выполняется метод get_or_create модели Result для создания или получения объекта Result.
                # Если объект был создан, то значение created будет True, иначе False.
                user=current_user, # присваиваем значение current_user в поле user модели Result
                section_name=section.name, # присваиваем значение name в поле section_name модели Result
                defaults={
                    'status': section.status,# присваиваем значение status в поле status модели Result
                    'total_question': testing.total_question,## присваиваем значение total_question в поле total_question модели Result
                    'total_correct_answer': testing.total_correct_answer,# присваиваем значение total_correct_answer в поле total_correct_answer модели Result
                    'section_id': section.id,# присваиваем значение id в поле section_id модели Result
                }
            )

            if not created:#Если объект Result не был создан (т.е., created равно False), значения обновляются и сохраняются в базе данных.
                result.status = section.status
                result.total_question = testing.total_question
                result.total_correct_answer = testing.total_correct_answer
                result.section_id = section.id
                result.save()



#Сигнал post_save является одним из сигналов в Django, который срабатывает после сохранения объекта модели.
# Он позволяет выполнять определенные действия или обработку данных после того, как объект модели был сохранен.
#это на всякий случай, если в методе save не найдется текущий пользоватекль
@receiver(post_save, sender=Question, dispatch_uid="update_section_status")
def update_section_status(sender, instance, created, **kwargs):
    if created:
        current_user = instance.user
        if current_user.is_authenticated:
            testing = instance.test
            if testing.total_correct_answer >= 10:
                section = testing.section
                section.status = True
                section.save()


class Review(models.Model):
    review_text = models.TextField()

    def __str__(self):
        return self.review_text


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, default=None)
    section_name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    total_question = models.IntegerField(default=0)
    total_correct_answer = models.IntegerField(default=0)

    def __str__(self):
        return f"Результат: {self.user.username} - {self.section_name}"
