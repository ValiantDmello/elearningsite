# Generated by Django 4.2.2 on 2023-07-09 03:43

from django.db import migrations, models
import elearning.models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0019_alter_student_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(default='course_cover/course-default.png', upload_to=elearning.models.rename_course_cover),
        ),
    ]