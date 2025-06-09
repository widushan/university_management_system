from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistrationForm, LoginForm

def home_view(request):
    return render(request, 'main/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request, user_type):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            prefix = {'admin': 'admin', 'lecturer': 'lec', 'student': 'st'}[user_type]
            if not username.startswith(prefix):
                messages.error(request, f"Username must start with '{prefix}'")
            else:
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect(f'dashboard_{user_type}')
                else:
                    messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, f'main/login_{user_type}.html', {'form': form})

def dashboard_admin(request):
    return render(request, 'main/dashboard_admin.html')

def dashboard_lecturer(request):
    return render(request, 'main/dashboard_lecturer.html')

def dashboard_student(request):
    return render(request, 'main/dashboard_student.html')