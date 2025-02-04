from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CourseForm
from users.models import Student, Professor

@login_required
def enroll_in_course(request, course_id):
    """ثبت‌نام در دوره"""
    course = Course.objects.get(id=course_id)
    student_profile = request.user.student_profile

    # بررسی که آیا دانشجو قبلاً در این دوره ثبت‌نام کرده است
    if course not in student_profile.courses.all():
        student_profile.courses.add(course)
        student_profile.save()

    return redirect('student_dashboard')

@login_required
def manage_courses(request):
    """نمایش دوره‌هایی که استاد تدریس می‌کند"""
    if not request.user.is_professor:
        return redirect('panel')

    # بررسی و ایجاد پروفایل در صورت عدم وجود
    professor_profile, created = Professor.objects.get_or_create(user=request.user)

    courses = professor_profile.courses.all()  # دوره‌هایی که استاد تدریس می‌کند
    return render(request, 'manage_courses.html', {'courses': courses})


@login_required
def student_courses(request):
    """نمایش دوره‌های دانشجویی"""
    if not request.user.is_student:
        return redirect('panel')

    # بررسی و ایجاد پروفایل در صورت عدم وجود
    student_profile, created = Student.objects.get_or_create(user=request.user)

    courses = student_profile.courses.all()  # دوره‌هایی که دانشجو در آن‌ها ثبت‌نام کرده است
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




