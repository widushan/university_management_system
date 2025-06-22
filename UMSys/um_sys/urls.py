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
    path('add_modules/', views.add_modules, name='add_modules'),
    path('view_dashboard/', views.view_dashboard, name='view_dashboard'),
    path('exam_results/', views.exam_results, name='exam_results'),
    path('lec_profile/', views.lec_profile, name='lec_profile'),
    path('add_resources/', views.add_resources, name='add_resources'),
    path('view_resources/', views.view_resources, name='view_resources'),
    path('delete_material/<int:material_id>/', views.delete_material, name='delete_material'),
    path('edit_material/<int:material_id>/', views.edit_material, name='edit_material'),
    path('add_announcements/', views.add_announcements, name='add_announcements'),
    path('view_announcements/', views.view_announcements, name='view_announcements'),
    path('edit_announcement/<int:announcement_id>/', views.edit_announcement, name='edit_announcement'),
    path('delete_announcement/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
    path('attendance/', views.attendance, name='attendance'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)