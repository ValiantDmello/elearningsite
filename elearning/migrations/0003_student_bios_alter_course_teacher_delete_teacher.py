# Generated by Django 4.2.2 on 2023-07-03 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0002_remove_teacher_is_teacher_course_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='bios',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_teacher', to='elearning.student'),
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
