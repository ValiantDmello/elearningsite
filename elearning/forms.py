from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


from .models import *

# SignUpForm
class SignUpForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ('username','email','first_name','last_name')
        widgets = {
            'username':forms.TextInput(attrs={
                'name' :"Username",'class':"form-control",'id':"floatingInput",'placeholder':"Username"}),
            'email': forms.EmailInput(attrs={
                'name': "Email", 'class': "form-control", 'id': "floatingInput", 'placeholder': "Email",'type':'second'}),
            'first_name': forms.TextInput(attrs={
                'name': "First_name", 'class': "form-control", 'id': "floatingInput", 'placeholder': "First name"}),
            'last_name': forms.TextInput(attrs={
                'name': "Last_name", 'class': "form-control", 'id': "floatingPassword", 'placeholder': "Last name",'type':'second'}),
        }
    # Password verification special fields
    password1 = forms.CharField(

        widget=forms.PasswordInput(
            attrs={'name':'Password','class': 'form-control', 'type': 'password', 'id':"floatingPassword1",'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(
            attrs={'name':'Confirm password','class': 'form-control', 'type': 'password', 'id': "floatingPassword2",'placeholder': 'Confirm password'}),
    )
    agreement = forms.BooleanField(required=True,widget=forms.CheckboxInput(attrs={'class':"form-check-input",'value':'agreement','id':"flexCheckDefault"}))


# User form and Profile form is for updating profile
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')
        widgets ={
            'email': forms.EmailInput(attrs={
                'class': "form-control", 'placeholder': "Your_email@email.com", }),
            'first_name': forms.TextInput(attrs={
                'class': "form-control", 'placeholder': "First name", }),
            'last_name': forms.TextInput(attrs={
                'class': "form-control", 'placeholder': "Last name", }),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('avatar','bios','billing_address','phone_number',)
        widgets = {


            'bios': forms.Textarea(attrs={
                'class': "form-control",'placeholder':"Introduce your self", 'rows':3}),
            'billing_address': forms.TextInput(attrs={
                'class': "form-control",'placeholder':"Your address", }),
            'phone_number': forms.TextInput(attrs={
                'class': "form-control", 'placeholder':"Your phone number",}),
        }

# Search Bar Form
class SearchForm(forms.Form):
    name = forms.CharField(max_length=100)


class EnrollForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = ('student', 'course', 'enrollment_type')

class LessionForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['lesson_no','title','description','video']#,'quiz']
        # widgets = {
        #     'description': forms.Textarea(attrs={
        #         'class': 'my-input',
        #         'placeholder': 'Enter your description',
        #         'rows': 4,
        #     }),
        # }

# class AddCourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ['name', 'description', 'image', 'category', 'price']
#         widgets = {'category': forms.TextInput}



class AddCourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'category': forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddCourseForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
