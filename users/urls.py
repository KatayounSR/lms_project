from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('professor-dashboard/', professor_dashboard, name='professor_dashboard'),
    path('student-list/', student_list, name='student_list'),
]