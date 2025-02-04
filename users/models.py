from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)  # افزودن فیلد نام
    phone = models.CharField(max_length=20, unique=True)
    is_student = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)

    def __str__(self):
        return self.name if self.name else self.username


# Student Model
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    
    def __str__(self):
        return self.user.username

# Professor Model
class Professor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='professor_profile')
    
    def __str__(self):
        return self.user.username
