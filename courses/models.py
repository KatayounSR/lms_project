from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField('users.CustomUser', related_name='enrolled_courses', blank=True)

    def __str__(self):
        return self.name

