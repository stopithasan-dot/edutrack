from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('inst_admin', 'Institution Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    institution = models.ForeignKey('institutions.Institution', null=True, blank=True, on_delete=models.CASCADE)
    class_ref = models.ForeignKey('academics.Class', null=True, blank=True, on_delete=models.SET_NULL, related_name='students')
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
