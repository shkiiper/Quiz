# Generated by Django 4.2.2 on 2023-06-16 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0006_alter_question_testing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='testing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='Quiz.testing'),
        ),
    ]