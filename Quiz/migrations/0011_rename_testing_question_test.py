# Generated by Django 4.2.2 on 2023-06-16 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0010_alter_question_testing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='testing',
            new_name='test',
        ),
    ]
