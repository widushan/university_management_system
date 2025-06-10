from django.contrib import admin
from .models import Department, Degree, Student

admin.site.register(Department)
admin.site.register(Degree)
admin.site.register(Student)