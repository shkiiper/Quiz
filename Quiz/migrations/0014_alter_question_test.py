# Generated by Django 4.2.2 on 2023-06-16 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0013_alter_question_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='test',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Quiz.testing'),
        ),
    ]
