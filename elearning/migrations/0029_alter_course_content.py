# Generated by Django 4.2.1 on 2023-07-17 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0028_alter_course_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='content',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
