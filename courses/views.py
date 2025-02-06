from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CourseForm
from users.models import Student, Professor


@login_required
def available_courses(request):
    """نمایش دوره‌های موجود برای ثبت‌نام"""
    student_profile = get_object_or_404(Student, user=request.user)
    
    # دریافت دوره‌هایی که دانشجو هنوز ثبت‌نام نکرده است
    courses = Course.objects.exclude(students=student_profile)
    
    return render(request, 'student_available_courses.html', {'courses': courses})

@login_required
def enroll_course(request, course_id):
    """ثبت‌نام دانشجو در دوره"""
    course = get_object_or_404(Course, id=course_id)
    student_profile = get_object_or_404(Student, user=request.user)

    if student_profile not in course.students.all():
        course.students.add(student_profile)

    return redirect('student_courses')


@login_required
def manage_courses(request):
    """نمایش دوره‌هایی که استاد تدریس می‌کند"""
    if not request.user.is_professor:
        return redirect('panel')

    # بررسی و ایجاد پروفایل در صورت عدم وجود
    professor_profile, created = Professor.objects.get_or_create(user=request.user)

    courses = professor_profile.courses.all()  # دوره‌هایی که استاد تدریس می‌کند
    return render(request, 'manage_courses.html', {'courses': courses})


def student_courses(request):
    """نمایش دوره‌های دانشجو"""
    if not request.user.is_student:
        return redirect('professor_dashboard')

    student_profile = request.user.student_profile
    courses = student_profile.courses.all()

    return render(request, 'student_courses.html', {'courses': courses})

@login_required
def create_course(request):
    """ایجاد دوره جدید توسط استاد"""
    if not request.user.is_professor:
        return redirect('panel')

    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user.professor_profile
            course.save()
            return redirect('manage_courses')
    else:
        form = CourseForm()

    return render(request, 'create_course.html', {'form': form})


@login_required
def edit_course(request, course_id):
    """ویرایش دوره توسط استاد"""
    course = get_object_or_404(Course, id=course_id, instructor=request.user.professor_profile)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('manage_courses')
    else:
        form = CourseForm(instance=course)

    return render(request, 'edit_course.html', {'form': form})


@login_required
def delete_course(request, course_id):
    """حذف دوره توسط استاد"""
    course = get_object_or_404(Course, id=course_id, professor=request.user.professor_profile)

    if request.method == "POST":
        course.delete()
        return redirect('manage_courses')

    return render(request, 'delete_course.html', {'course': course})


@login_required
def course_detail(request, course_id):
    """نمایش جزئیات دوره"""
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})




