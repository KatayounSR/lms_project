from django.urls import path
from .views import (
    manage_courses, student_courses, create_course, edit_course, 
    delete_course, course_detail, enroll_in_course
)

urlpatterns = [
    path('manage-courses/', manage_courses, name='manage_courses'),
    path('student-courses/', student_courses, name='student_courses'),
    path('course/create/', create_course, name='create_course'),
    path('course/<int:course_id>/edit/', edit_course, name='edit_course'),
    path('course/<int:course_id>/delete/', delete_course, name='delete_course'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', enroll_in_course, name='enroll_in_course'),
]