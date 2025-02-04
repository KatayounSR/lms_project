from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from courses.models import *
from grades.models import *

def index(request):
    return render(request, 'index.html')

@login_required
def student_dashboard(request):
    """پنل دانشجویی - مشاهده دوره‌ها و نمرات"""
    if not request.user.is_student:
        return redirect('professor_dashboard')  # اگر کاربر استاد باشد، به پنل استاد ریدایرکت می‌شود.

    student_profile = request.user.student_profile
    courses = student_profile.courses.all()  # دریافت دوره‌های دانشجو
    grades = Grade.objects.filter(student=student_profile)  # دریافت نمرات دانشجو

    return render(request, 'users/student_dashboard.html', {'courses': courses, 'grades': grades})


def student_list(request):
    """نمایش لیست تمامی دانشجویان"""
    students = Student.objects.all()  # دریافت تمامی دانشجویان
    return render(request, 'users/student_list.html', {'students': students})

@login_required
def professor_dashboard(request):
    """پنل استاد - مدیریت دوره‌ها و نمرات"""
    if not request.user.is_professor:
        return redirect('student_dashboard')  # اگر کاربر دانشجو باشد، به پنل دانشجویی ریدایرکت می‌شود.

    professor_profile = request.user.professor_profile
    courses = professor_profile.courses.all()  # دریافت دوره‌های استاد
    students = Student.objects.all()  # دریافت لیست تمام دانشجویان
    grades = Grade.objects.all()  # دریافت لیست تمام نمرات

    return render(request, 'users/professor_dashboard.html', {'courses': courses, 'students': students, 'grades': grades})

def user_register(request):
    """ثبت‌نام کاربر (استاد یا دانشجو)"""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')

            if role == 'student':
                user.is_student = True
            elif role == 'professor':
                user.is_professor = True

            user.save()
            login(request, user)
            #messages.success(request, "ثبت‌نام با موفقیت انجام شد!")

            if role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('professor_dashboard')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    """ورود کاربر (استاد یا دانشجو)"""
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"خوش آمدید {user.name}!")

                if user.is_student == 'student':
                    return redirect('student_dashboard')
                else:
                    return redirect('professor_dashboard')
            else:
                messages.error(request, "نام کاربری یا رمز عبور نادرست است.")
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    """خروج از سیستم"""
    logout(request)
    messages.success(request, "با موفقیت خارج شدید!")
    return redirect('index')
