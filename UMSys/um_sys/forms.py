from django import forms
from django.contrib.auth.models import User
from .models import Student, Department, Degree, Semester, Course, Lecturer, Department, Degree, ExamResult

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(),
        }
        help_texts = {
            'username': None,  
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['registration_no']
        widgets = {
            'avatar': forms.ClearableFileInput(),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'degree': forms.Select(attrs={'class': 'form-control'}),
        }


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'registration_no': forms.TextInput(attrs={'readonly': 'readonly'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'degree': forms.Select(attrs={'class': 'form-control'}),
        }


class SemesterCourseForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    degree = forms.ModelChoiceField(queryset=Degree.objects.all())
    semester = forms.ModelChoiceField(queryset=Semester.objects.all())


class LecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = ['avatar', 'name', 'contact_no', 'email', 'university_id', 'qualification']
        widgets = {
            'university_id': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class DepartmentCourseForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    degree = forms.ModelChoiceField(queryset=Degree.objects.all())


class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['student', 'course_id', 'course_name', 'result']