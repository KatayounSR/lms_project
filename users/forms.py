from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'دانشجو'),
        ('professor', 'استاد'),
    ]

    username = forms.CharField(
        max_length=150, required=True, 
        label="نام کاربری",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}),
    )

    name = forms.CharField(
        max_length=100, 
        required=True, 
        label="نام و نام خانوادگی",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        label="ایمیل",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20, 
        required=True, 
        label="شماره تلفن",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        required=True, 
        label="نوع حساب",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'phone', 'role', 'password1', 'password2']

    def clean_email(self):
        """بررسی اینکه ایمیل تکراری نباشد"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً ثبت شده است.")
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

