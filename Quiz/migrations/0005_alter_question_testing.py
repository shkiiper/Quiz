# Generated by Django 4.2.2 on 2023-06-16 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0004_remove_question_test_question_testing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='testing',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='Quiz.testing'),
        ),
    ]
