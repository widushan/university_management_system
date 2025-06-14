from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, StudentForm, StudentEditForm, SemesterCourseForm, LecturerForm, DepartmentCourseForm, ExamResultForm
from .models import Student, Course, Lecturer, LectureModule, DepartmentCourse, ExamResult
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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




def manage_semester_courses(request):
    courses = []
    selected_department = None
    selected_degree = None
    selected_semester = None
    message = ''

    if request.method == 'POST':
        form = SemesterCourseForm(request.POST)
        course_ids = request.POST.getlist('course_id')
        course_names = request.POST.getlist('course_name')
        if form.is_valid():
            department = form.cleaned_data['department']
            degree = form.cleaned_data['degree']
            semester = form.cleaned_data['semester']

            # Delete all existing courses for this combination
            Course.objects.filter(department=department, degree=degree, semester=semester).delete()

            # Save new/edited courses
            for cid, cname in zip(course_ids, course_names):
                if cid.strip() and cname.strip():
                    Course.objects.create(
                        department=department,
                        degree=degree,
                        semester=semester,
                        course_id=cid.strip(),
                        course_name=cname.strip()
                    )
            # Reload courses for display
            courses = Course.objects.filter(department=department, degree=degree, semester=semester)
            selected_department = department
            selected_degree = degree
            selected_semester = semester
            message = "Updated successfully!"
    else:
        form = SemesterCourseForm(request.GET or None)
        if form.is_valid():
            department = form.cleaned_data['department']
            degree = form.cleaned_data['degree']
            semester = form.cleaned_data['semester']
            courses = Course.objects.filter(department=department, degree=degree, semester=semester)
            selected_department = department
            selected_degree = degree
            selected_semester = semester

    return render(request, 'main/manage_semester_courses.html', {
        'form': form,
        'courses': courses,
        'selected_department': selected_department,
        'selected_degree': selected_degree,
        'selected_semester': selected_semester,
        'message': message,
    })



def get_next_lecturer_id():
    last = Lecturer.objects.order_by('-id').first()
    if last and last.university_id.startswith('Lec'):
        num = int(last.university_id[3:])
        return f"Lec{num+1:03d}"
    return "Lec001"

def add_lecturer(request):
    message = ''
    if request.method == 'POST':
        form = LecturerForm(request.POST, request.FILES)
        course_ids = request.POST.getlist('course_id')
        course_names = request.POST.getlist('course_name')
        if form.is_valid():
            lecturer = form.save(commit=False)
            lecturer.university_id = get_next_lecturer_id()
            lecturer.save()
            # Save modules
            for cid, cname in zip(course_ids, course_names):
                if cid.strip() and cname.strip():
                    LectureModule.objects.create(
                        lecturer=lecturer,
                        course_id=cid.strip(),
                        course_name=cname.strip()
                    )
            message = "Lecturer Added Successfully"
            # Prepare a fresh form with incremented university_id
            form = LecturerForm(initial={'university_id': get_next_lecturer_id()})
        else:
            message = "Please correct the errors below."
    else:
        form = LecturerForm(initial={'university_id': get_next_lecturer_id()})
    return render(request, 'main/add_lecturer.html', {'form': form, 'message': message})




def manage_lecturer(request):
    lecturer = None
    modules = []
    message = ''
    university_id_query = request.GET.get('university_id', '')

    if university_id_query:
        try:
            lecturer = Lecturer.objects.get(university_id=university_id_query)
            modules = list(lecturer.modules.all())
        except Lecturer.DoesNotExist:
            lecturer = None
            modules = []

    if request.method == 'POST':
        university_id = request.POST.get('university_id')
        try:
            lecturer = Lecturer.objects.get(university_id=university_id)
        except Lecturer.DoesNotExist:
            lecturer = None

        if lecturer:
            form = LecturerForm(request.POST, request.FILES, instance=lecturer)
            course_ids = request.POST.getlist('course_id')
            course_names = request.POST.getlist('course_name')
            if form.is_valid():
                form.save()
                # Remove old modules
                lecturer.modules.all().delete()
                # Add new/edited modules
                for cid, cname in zip(course_ids, course_names):
                    if cid.strip() and cname.strip():
                        LectureModule.objects.create(
                            lecturer=lecturer,
                            course_id=cid.strip(),
                            course_name=cname.strip()
                        )
                message = "Data Updated Successfully"
                modules = list(lecturer.modules.all())
            else:
                message = "Please correct the errors below."
        else:
            form = None
            message = "Lecturer not found."
    else:
        form = LecturerForm(instance=lecturer) if lecturer else None

    return render(request, 'main/manage_lecturer.html', {
        'form': form,
        'lecturer': lecturer,
        'modules': modules,
        'university_id_query': university_id_query,
        'message': message,
    })



def add_departments_courses(request):
    message = ''
    if request.method == 'POST':
        form = DepartmentCourseForm(request.POST)
        course_ids = request.POST.getlist('course_id')
        course_names = request.POST.getlist('course_name')
        if form.is_valid():
            department = form.cleaned_data['department']
            degree = form.cleaned_data['degree']
            # Optionally, delete old courses for this department/degree
            # DepartmentCourse.objects.filter(department=department, degree=degree).delete()
            for cid, cname in zip(course_ids, course_names):
                if cid.strip() and cname.strip():
                    DepartmentCourse.objects.create(
                        department=department,
                        degree=degree,
                        course_id=cid.strip(),
                        course_name=cname.strip()
                    )
            message = "Modules Added Successfully"
            form = DepartmentCourseForm()  # Clear form after submit
    else:
        form = DepartmentCourseForm()
    return render(request, 'main/add_departments_courses.html', {'form': form, 'message': message})




def manage_departments_courses(request):
    courses = []
    selected_department = None
    selected_degree = None
    message = ''

    if request.method == 'POST':
        form = DepartmentCourseForm(request.POST)
        course_ids = request.POST.getlist('course_id')
        course_names = request.POST.getlist('course_name')
        if form.is_valid():
            department = form.cleaned_data['department']
            degree = form.cleaned_data['degree']
            # Delete all existing courses for this combination
            DepartmentCourse.objects.filter(department=department, degree=degree).delete()
            # Save new/edited courses
            for cid, cname in zip(course_ids, course_names):
                if cid.strip() and cname.strip():
                    DepartmentCourse.objects.create(
                        department=department,
                        degree=degree,
                        course_id=cid.strip(),
                        course_name=cname.strip()
                    )
            courses = DepartmentCourse.objects.filter(department=department, degree=degree)
            # Deduplicate by course_id and course_name
            seen = set()
            unique_courses = []
            for course in courses:
                key = (course.course_id, course.course_name)
                if key not in seen:
                    seen.add(key)
                    unique_courses.append(course)
            courses = unique_courses
            selected_department = department
            selected_degree = degree
            message = "Data Updated Successfully"
    else:
        form = DepartmentCourseForm(request.GET or None)
        if form.is_valid():
            department = form.cleaned_data['department']
            degree = form.cleaned_data['degree']
            courses = DepartmentCourse.objects.filter(department=department, degree=degree)
            # Deduplicate by course_id and course_name
            seen = set()
            unique_courses = []
            for course in courses:
                key = (course.course_id, course.course_name)
                if key not in seen:
                    seen.add(key)
                    unique_courses.append(course)
            courses = unique_courses
            selected_department = department
            selected_degree = degree

    return render(request, 'main/manage_departments_courses.html', {
        'form': form,
        'courses': courses,
        'selected_department': selected_department,
        'selected_degree': selected_degree,
        'message': message,
    })



def add_exam_results(request):
    student = None
    reg_no = request.GET.get('reg_no', '')
    message = ''
    if reg_no:
        try:
            student = Student.objects.get(registration_no=reg_no)
        except Student.DoesNotExist:
            student = None
            message = 'Student not found.'
    if request.method == 'POST':
        reg_no = request.POST.get('reg_no') or request.GET.get('reg_no')
        try:
            student = Student.objects.get(registration_no=reg_no)
        except Student.DoesNotExist:
            student = None
        if student:
            # Remove old results if you want to overwrite, or skip this if you want to append
            # ExamResult.objects.filter(student=student).delete()
            course_ids = request.POST.getlist('course_id')
            course_names = request.POST.getlist('course_name')
            results = request.POST.getlist('result')
            for cid, cname, res in zip(course_ids, course_names, results):
                if cid.strip() and cname.strip() and res.strip():
                    ExamResult.objects.create(
                        student=student,
                        course_id=cid.strip(),
                        course_name=cname.strip(),
                        result=res.strip()
                    )
            message = 'Results Added Successfully'
        else:
            message = 'Student not found.'
    return render(request, 'main/add_exam_results.html', {
        'student': student,
        'reg_no': reg_no,
        'message': message,
    })



def manage_exam_results(request):
    student = None
    results = []
    reg_no = request.GET.get('reg_no', '')
    message = ''

    if reg_no:
        try:
            student = Student.objects.get(registration_no=reg_no)
            results = list(ExamResult.objects.filter(student=student))
        except Student.DoesNotExist:
            student = None
            message = 'Student not found.'

    if request.method == 'POST':
        reg_no = request.POST.get('reg_no')
        try:
            student = Student.objects.get(registration_no=reg_no)
        except Student.DoesNotExist:
            return render(request, 'main/manage_exam_results.html', {
                'student': None,
                'reg_no': reg_no,
                'results': [],
                'message': 'Student not found.'
            })

        # Handle deletions
        deleted_ids = [i for i in request.POST.getlist('deleted_ids[]') if i.strip()]
        if deleted_ids:
            ExamResult.objects.filter(id__in=deleted_ids, student=student).delete()
        # Handle updates/adds
        course_ids = request.POST.getlist('course_id[]')
        course_names = request.POST.getlist('course_name[]')
        result_vals = request.POST.getlist('result[]')
        row_ids = request.POST.getlist('row_id[]')

        for idx in range(len(course_ids)):
            cid = course_ids[idx].strip()
            cname = course_names[idx].strip()
            res = result_vals[idx].strip()
            row_id = row_ids[idx].strip() if idx < len(row_ids) else ''

            if not cid or not cname or not res:
                continue

            if row_id and row_id != 'new':
                try:
                    er = ExamResult.objects.get(id=row_id, student=student)
                    er.course_id = cid
                    er.course_name = cname
                    er.result = res
                    er.save()
                except (ExamResult.DoesNotExist, ValueError):
                    # ValueError will catch the case where row_id is not a valid integer
                    pass
            elif row_id == 'new' or not row_id:
                ExamResult.objects.create(
                    student=student,
                    course_id=cid,
                    course_name=cname,
                    result=res
                )

        message = 'Results updated successfully.'
        results = list(ExamResult.objects.filter(student=student))

    return render(request, 'main/manage_exam_results.html', {
        'student': student,
        'reg_no': reg_no,
        'results': results,
        'message': message,
    })











@login_required
def my_profile(request):
    student = get_object_or_404(Student, registration_no=request.user.username)
    return render(request, 'main/my_profile.html', {'student': student})

@login_required
def add_modules(request):
    student = get_object_or_404(Student, registration_no=request.user.username)
    return render(request, 'main/add_modules.html', {'student': student})