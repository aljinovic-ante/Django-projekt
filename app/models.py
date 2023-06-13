from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    ADMIN = 'ADMIN'
    PROFESSOR = 'PROFESSOR'
    STUDENT = 'STUDENT'
    role_choices = [
        (ADMIN, 'admin'),
        (PROFESSOR, 'professor'),
        (STUDENT, 'student')
    ]
    role = models.CharField(max_length=32, choices=role_choices)

    def __str__(self):
        return self.role

class User(AbstractUser):
    user_status = (
        ('none', 'none'),
        ('redovni student', 'redovni student'),
        ('izvanredni student', 'izvanredni student')
    )

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=32, choices=user_status)



class Course(models.Model):
    name=models.CharField(max_length=255)
    code=models.CharField(max_length=16)
    program=models.CharField(max_length=255)
    ects=models.IntegerField()
    semester_ft=models.IntegerField()
    semester_pt=models.IntegerField()
    elective_choice=(('da','da'),('ne','ne'))
    elective=models.CharField(max_length=2,choices=elective_choice)
    professor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Enrollment_list(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    status_ch=(('upisan','upisan'),('polozen','polozen'),('nepolozen','nepolozen'))
    status=models.CharField(max_length=32,choices=status_ch,default='upisan')
