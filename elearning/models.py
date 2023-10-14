import datetime
import os
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
User._meta.get_field('first_name').blank = False
User._meta.get_field('first_name').null = False
User._meta.get_field('last_name').blank = False
User._meta.get_field('last_name').null = False

def rename_avatar(instance, filename):
    # get the filename extension
    ext = filename.split('.')[-1]
    # generate a unique UUID and convert it to a string for the filename
    filename = f"{uuid.uuid4()}.{ext}"
    # return the new filename including the path
    return os.path.join('avatars', filename)

# Create your models here.
class Student(User):
    avatar = models.ImageField(upload_to=rename_avatar,default='avatars/avatar-default.svg')
    bios = models.TextField(blank=True)
    billing_address = models.CharField(max_length=300,null=True,blank=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    is_premier = models.BooleanField(default=False)
    premier_expiration = models.DateField(blank=True,null=True)
    is_teacher = models.BooleanField(default=False)
    #teach_courses =

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Student'

    # auto set is_premier status
    def save(self, *args, **kwargs):
        if self.premier_expiration:
            if datetime.date.today() <= self.premier_expiration:
                self.is_premier = True
            else:
                self.is_premier = False
        super().save(*args, **kwargs)



class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


def rename_course_cover(instance, filename):
    # get the filename extension
    ext = filename.split('.')[-1]
    # generate a unique UUID and convert it to a string for the filename
    filename = f"{uuid.uuid4()}.{ext}"
    # return the new filename including the path
    return os.path.join('course_cover', filename)

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300,blank=True)
    image = models.ImageField(upload_to=rename_course_cover,default='course_cover/course-default.png')
    teacher = models.ForeignKey(Student, related_name='course_teacher',on_delete=models.CASCADE)
    category = models.ManyToManyField(Category,related_name='course_category')
    # content = models.JSONField(blank=True,null=True)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    allow_premier = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class PremiePlan(models.Model):
    name = models.CharField(max_length=10)
    days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
    tag = models.CharField(max_length=5,blank=True,null=True)
    daily = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    def __str__(self):
        display = str(self.days)+'days' + str(self.price)
        return display

    def save(self, *args, **kwargs):
        self.daily = self.price/self.days
        super().save(*args, **kwargs)

class Payment(models.Model):
    TYPE_CHOICE =[
        ('p','Premier'),
        ('c','Course')
    ]
    STATUS_CHOICES = [
        ('0', 'Initial'),
        ('1', 'Success'),
        ('2', 'Pending'),
    ]
    time = models.DateTimeField(default=datetime.datetime)
    student = models.ForeignKey(Student, related_name='payment_student',on_delete=models.PROTECT)
    type = models.CharField(max_length=1,choices=TYPE_CHOICE)
    course = models.ForeignKey(Course,related_name='payment_course',on_delete=models.PROTECT,blank=True,null=True)
    plan = models.ForeignKey(PremiePlan,related_name='payment_plan',on_delete=models.PROTECT,blank=True,null=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=0)

    def __str__(self):
        return str(self.id)


class HomepageRec(models.Model):
    course = models.ForeignKey(Course,related_name='recommend_course',on_delete=models.CASCADE)

    def __str__(self):
        return str(self.course.name)

class CourseEnrollment(models.Model):
    ENROLLMENT_TYPES = (
        ('Premium', 'Premium'),
        ('Paid', 'Paid'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date = models.DateField(auto_now_add=True)
    enrollment_type = models.CharField(max_length=10, choices=ENROLLMENT_TYPES)
    progress = models.IntegerField(default=0)

@receiver(post_save, sender=Payment)
def create_course_enrollment(sender, instance, created, **kwargs):
    if created and instance.type == 'c' and instance.status == '1':
        CourseEnrollment.objects.create(student=instance.student, course=instance.course, enrollment_type='Paid')



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_no = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to='lesson_videos/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    ANSWER_CHOICES = (
        ('a', 'a'),
        ('b', 'b'),
        ('c', 'c'),
        ('d', 'd'),
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.TextField()
    img = models.ImageField(upload_to='quiz_images/', null=True, blank=True)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    ans = models.CharField(max_length=1, choices=ANSWER_CHOICES)

class Files(models.Model):
    FILE_TYPES = (
        ('Document', 'Document'),
        ('Image', 'Image'),
        ('Other', 'Other'),
    )

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file = models.FileField(upload_to='lesson_files/')

class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)

class QuizResult(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    completed_at = models.DateTimeField(auto_now_add=True)


class RegisterInfo(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    group_id = models.PositiveIntegerField()



