# Generated by Django 4.2.2 on 2023-06-18 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0016_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='sections',
        ),
        migrations.AddField(
            model_name='result',
            name='section',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Quiz.section'),
        ),
    ]
