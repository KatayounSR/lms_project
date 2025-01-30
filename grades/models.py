from django.db import models

class Grade(models.Model):
    student = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.student.username} - {self.course.name}: {self.score}"
