# Generated by Django 4.2.2 on 2023-07-21 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0031_alter_lesson_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.FileField(blank=True, upload_to='lesson_videos/'),
        ),
    ]
