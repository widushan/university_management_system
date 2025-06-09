from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/admin/', lambda r: views.login_view(r, 'admin'), name='login_admin'),
    path('login/lecturer/', lambda r: views.login_view(r, 'lecturer'), name='login_lecturer'),
    path('login/student/', lambda r: views.login_view(r, 'student'), name='login_student'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/lecturer/', views.dashboard_lecturer, name='dashboard_lecturer'),
    path('dashboard/student/', views.dashboard_student, name='dashboard_student'),
]