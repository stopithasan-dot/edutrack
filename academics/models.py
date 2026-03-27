from django.db import models
from institutions.models import Institution
from django.conf import settings

class Class(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.section}" if self.section else self.name

class Subject(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    credits = models.IntegerField(default=0)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        limit_choices_to={'role': 'teacher'}
    )
    
    def __str__(self):
        return self.name
