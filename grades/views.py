from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Grade
from courses.models import Course
from users.models import Professor, Student
from django import forms
import csv
import json

@login_required
def student_grades(request):
    """نمایش نمرات دانشجو"""
    if not request.user.is_student:
        return redirect('student_dashboard')

    student_profile = request.user.student_profile
    grades = Grade.objects.filter(student=student_profile)

    course_names = [grade.course.name for grade in grades]
    scores = [grade.score for grade in grades]

    #print("Course Names:", course_names)
    #print("Scores:", scores)

    return render(request, 'student_grades.html', {
        'grades': grades,
        'course_names': json.dumps(course_names),  # تبدیل لیست به JSON
        'scores': json.dumps(scores)  # تبدیل لیست به JSON
    })


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
    """دانلود نمرات به‌صورت فایل CSV"""
    if not request.user.is_student:
        return redirect('student_dashboard')

    student_profile = request.user.student_profile
    grades = Grade.objects.filter(student=student_profile)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="grades.csv"'

    writer = csv.writer(response)
    writer.writerow(['درس', 'نمره'])

    for grade in grades:
        writer.writerow([grade.course.name, grade.score])

    return response


@login_required
def submit_grade(request, course_id):
    """دانشجو نمره خود را ثبت می‌کند"""
    if not request.user.is_student:
        return redirect('panel')

    student = request.user.student_profile
    course = get_object_or_404(Course, id=course_id)

    if student not in course.students.all():
        #messages.error(request, "شما در این دوره ثبت‌نام نکرده‌اید.")
        return redirect('course_detail', course_id=course_id)

    if request.method == "POST":
        score = request.POST.get('score')

        if score and score.strip():  # بررسی اینکه مقدار `score` خالی نباشد
            score = float(score)  # تبدیل مقدار ورودی به عدد
            grade, created = Grade.objects.get_or_create(student=student, course=course, defaults={'score': score})

            if not created:  # اگر قبلاً وجود داشته باشد، مقدار نمره را آپدیت می‌کنیم
                grade.score = score
                grade.save()

        #    messages.success(request, "نمره شما با موفقیت ثبت شد!")
        #else:
        #    messages.error(request, "لطفاً نمره‌ای معتبر وارد کنید.")

    return redirect('course_detail', course_id=course_id)