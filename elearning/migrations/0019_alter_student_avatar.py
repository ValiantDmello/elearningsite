# Generated by Django 4.2.2 on 2023-07-08 22:48

from django.db import migrations, models
import elearning.models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0018_alter_student_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='avatar',
            field=models.ImageField(default='avatars/avatar-default.svg', upload_to=elearning.models.rename_avatar),
        ),
    ]
