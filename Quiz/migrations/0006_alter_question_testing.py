# Generated by Django 4.2.2 on 2023-06-16 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0005_alter_question_testing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='testing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='Quiz.testing'),
        ),
    ]
