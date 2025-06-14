from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/admin/', lambda r: views.login_view(r, 'admin'), name='login_admin'),
    path('login/lecturer/', lambda r: views.login_view(r, 'lecturer'), name='login_lecturer'),
    path('login/student/', lambda r: views.login_view(r, 'student'), name='login_student'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/lecturer/', views.dashboard_lecturer, name='dashboard_lecturer'),
    path('dashboard/student/', views.dashboard_student, name='dashboard_student'),
    path('add_student/', views.add_student, name='add_student'),
    path('manage_student/', views.manage_student, name='manage_student'),
    path('add_semester_courses/', views.add_semester_courses, name='add_semester_courses'),
    path('manage_semester_courses/', views.manage_semester_courses, name='manage_semester_courses'),
    path('add_lecturer/', views.add_lecturer, name='add_lecturer'),
    path('manage_lecturer/', views.manage_lecturer, name='manage_lecturer'),
    path('add_departments_courses/', views.add_departments_courses, name='add_departments_courses'),
    path('manage_departments_courses/', views.manage_departments_courses, name='manage_departments_courses'),
    path('add_exam_results/', views.add_exam_results, name='add_exam_results'),
    path('manage_exam_results/', views.manage_exam_results, name='manage_exam_results'),
    path('my_profile/', views.my_profile, name='my_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)