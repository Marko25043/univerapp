"""
URL configuration for projekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login_user,name='login'),
    path('main/',views.hello,name='main'),
    path('student/',views.student,name='student'),
    path('professor/',views.professor,name='professor'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('add_subject/',views.add_subject, name = 'add_subject'),
    path('add_professor/',views.add_professor, name = 'add_professor'),
    path('add_student/',views.add_student, name = 'add_student'),
    path('student_add_subject/',views.student_add_subject, name = 'student_add_subject'),
    path('add_enrollment_form/',views.add_enrollment_form, name = 'add_enrollment_form'),

    path('enrolled_students/<int:pk>',views.enrolled_students, name = 'enrolled_students'),
    path('professor_enrolled_student/<int:pk>',views.professor_enrolled_student, name = 'professor_enrolled_student'),
    
    path('student_statistics_by_subject/<int:pk>',views.student_statistics_by_subject, name = 'student_statistics_by_subject'),

    path('update_professor/<str:pk>',views.update_professor, name = 'update_professor'),
    path('update_student/<str:pk>',views.update_student, name = 'update_student'),
    path('update_subject/<str:pk>',views.update_subject, name = 'update_subject'),
    path('update_enrollment_form/<str:pk>',views.update_enrollment_form, name = 'update_enrollment_form'),

    path('update_student_status/<str:pk>/', views.update_student_status, name='update_student_status'),
    path('admin_update_student_status/<str:pk>/', views.admin_update_student_status, name='admin_update_student_status'),

    path('delete_professor/<str:pk>',views.delete_professor, name = 'delete_professor'),
    path('delete_student/<str:pk>',views.delete_student, name = 'delete_student'),
    path('delete_subject/<str:pk>',views.delete_subject, name = 'delete_subject'),
    path('delete_enrollment_form/<str:pk>',views.delete_enrollment_form, name = 'delete_enrollment_form'),

]
