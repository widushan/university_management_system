from django.contrib import admin
from .models import Department, Degree, Student, Semester, Course, Lecturer, ExamResult

admin.site.register(Department)
admin.site.register(Degree)
admin.site.register(Student)
admin.site.register(Semester) 
admin.site.register(Course)
admin.site.register(Lecturer)
admin.site.register(ExamResult)