from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_TEACHER = 'teacher'
    ROLE_STUDENT = 'student'
    ROLE_CHOICES = [
        (ROLE_TEACHER, 'Teacher'),
        (ROLE_STUDENT, 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_STUDENT)

    def is_teacher(self):
        return self.role == self.ROLE_TEACHER

    def is_student(self):
        return self.role == self.ROLE_STUDENT

    def __str__(self):
        return f"{self.username} ({self.role})"
