from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, StudentForm, StudentEditForm, SemesterCourseForm
from .models import Student, Course

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
            prefix = {'admin': 'Admin', 'lecturer': 'Lec', 'student': 'St'}[user_type]
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

def get_next_registration_no():
    last_student = Student.objects.order_by('-id').first()
    if last_student and last_student.registration_no.startswith('St'):
        last_no = int(last_student.registration_no[2:])
        return f"St{last_no + 1:07d}"
    return "St2025001"

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.registration_no = get_next_registration_no()
            student.save()
            return redirect('add_student')  # Redirect to clear the form and increment reg no
    else:
        form = StudentForm()
    reg_no = get_next_registration_no()
    return render(request, 'main/add_student.html', {'form': form, 'reg_no': reg_no})


def manage_student(request):
    student = None
    form = None
    reg_no_query = request.GET.get('reg_no', '')
    message = ''
    if reg_no_query:
        try:
            student = Student.objects.get(registration_no=reg_no_query)
            form = StudentEditForm(instance=student)
        except Student.DoesNotExist:
            form = None
            student = None

    if request.method == 'POST':
        reg_no = request.POST.get('registration_no')
        try:
            student = Student.objects.get(registration_no=reg_no)
        except Student.DoesNotExist:
            student = None
        if student:
            form = StudentEditForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                form.save()
                message = "Student updated successfully!"
            else:
                message = "Please correct the errors below."
        else:
            form = None
            message = "Student not found."

    return render(request, 'main/manage_student.html', {
        'form': form,
        'student': student,
        'reg_no_query': reg_no_query,
        'message': message
    })


def add_semester_courses(request):
    if request.method == 'POST':
        form = SemesterCourseForm(request.POST)
        course_ids = request.POST.getlist('course_id')
        course_names = request.POST.getlist('course_name')
        if form.is_valid():
            department = form.cleaned_data['department']
            degree = form.cleaned_data['degree']
            semester = form.cleaned_data['semester']
            # Save each course
            for cid, cname in zip(course_ids, course_names):
                if cid.strip() and cname.strip():
                    Course.objects.create(
                        department=department,
                        degree=degree,
                        semester=semester,
                        course_id=cid.strip(),
                        course_name=cname.strip()
                    )
            return redirect('add_semester_courses')
    else:
        form = SemesterCourseForm()
    return render(request, 'main/add_semester_courses.html', {'form': form})