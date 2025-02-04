from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Grade
from courses.models import Course
from users.models import Professor, Student
import csv

@login_required
def student_grades(request):
    """نمایش نمرات دانشجو"""
    if not request.user.is_student:
        return redirect('student_dashboard')

    student_profile = request.user.student_profile
    grades = Grade.objects.filter(student=student_profile)

    return render(request, 'student_grades.html', {'grades': grades})

login_required
def professor_grades(request):
    """نمایش نمرات تمام دانشجویان برای استاد"""
    if not request.user.is_professor:
        return redirect('student_dashboard')

    professor_profile = request.user.professor_profile
    courses = Course.objects.filter(instructor=professor_profile)
    grades_by_course = {course: Grade.objects.filter(course=course) for course in courses}

    return render(request, 'professor_grades.html', {'grades_by_course': grades_by_course})

@login_required
def grade_student(request, course_id, student_id):
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        score = request.POST.get('score')
        grade, created = Grade.objects.update_or_create(
            student=student,
            course=course,
            defaults={'score': score}
        )
        return redirect('professor_dashboard')  # بازگشت به صفحه‌ی داشبورد استاد

    return render(request, 'grade_student.html', {'course': course, 'student': student})

@login_required
def download_grades(request):
    """دانلود لیست نمرات به صورت CSV"""
    grades = Grade.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=grades.csv'
    writer = csv.writer(response)
    writer.writerow(['Student', 'Course', 'Score'])
    for grade in grades:
        writer.writerow([grade.student.user.username, grade.course.name, grade.score])
    return response