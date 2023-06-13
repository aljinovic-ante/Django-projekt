from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class Professor_form(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", 'first_name', 'last_name', "password1", "password2", "role", "status"]

    def __init__(self, *args, **kwargs):
        super(Professor_form, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['role'].queryset = Role.objects.filter(role=Role.PROFESSOR)
        self.fields['status'].choices = (('none', 'None'),)

class Student_form(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", 'first_name', 'last_name', "password1", "password2", "role", "status"]

    def __init__(self, *args, **kwargs):
        super(Student_form, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['status'].choices = (('redovni student', 'redovni student'), ('izvanredni student', 'izvanredni student'), )
        self.fields['role'].queryset = Role.objects.filter(role=Role.STUDENT)

class Course_form(ModelForm):
    class Meta:
        model=Course
        fields=['name', 'code', 'program', 'ects', 'semester_ft', 'semester_pt', 'elective', 'professor']
        labels = {
            'name':'Name',
            'code':'Code',
            'program':'Program',
            'ects': ('ECTS'),
            'semester_ft': ('Semester (Full-time student)'), 
            'semester_pt': ('Semester (part-time student)'),
            'elective':'Elective',
            'professor':'Professor'
        }

    def __init__(self,*args,**kwargs):
        super(Course_form,self).__init__(*args,**kwargs)
        self.fields['professor'].queryset = User.objects.filter(role_id__role=Role.PROFESSOR)
        self.fields['professor'].required = False
        self.fields['program'].required = False

class Edit_user_form(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", 'first_name', 'last_name', "role", "status"]
        exclude = ["password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(Edit_user_form, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

class Course_status_form(ModelForm):
    class Meta:
        model = Enrollment_list
        fields = ['status']