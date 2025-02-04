from django.db import models
from users.models import *

# Course Model
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(Student, related_name='courses')
    
    def __str__(self):
        return self.name

