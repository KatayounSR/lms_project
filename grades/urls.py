from django.urls import path
from .views import *

urlpatterns = [
    path('professor-grades/', professor_grades, name='professor_grades'),
    path('student-grades/', student_grades, name='student_grades'),
    path('grade-student/<int:course_id>/<int:student_id>/', grade_student, name='grade_student'),
    path('download-grades/', download_grades, name='download_grades'),
]

