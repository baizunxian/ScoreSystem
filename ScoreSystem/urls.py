"""ScoreSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from score import views, teacher_view, student_view, admin_view
urlpatterns = [
    path('login/', views.login),
    path('welcome/', views.welcome),
    path('teacher_loginout/', views.teacher_loginout),
    path('student_loginout/', views.student_loginout),
    path('admin_login/', views.admin_login),
    path('admin/', views.admin),

    # 老师相关url
    path('TeacherPage/', teacher_view.TeacherPage),
    path('add_Scholarship/', teacher_view.add_Scholarship),
    path('bonus_delete/', teacher_view.bonus_delete),
    path('toEditbonusPage/', teacher_view.toEditbonusPage),
    path('update_teacher_pwd/', teacher_view.update_teacher_pwd),
    path('approval_application/', teacher_view.approval_application_page),
    path('teacher_college_application_page/', teacher_view.teacher_college_application_page),
    path('teacher_college_application_list/', teacher_view.teacher_college_application_list),
    path('teacher_Approved_page/', teacher_view.teacher_Approved_page),
    path('teacher_Approved_page_list/', teacher_view.teacher_Approved_page_list),

    # 学生相关url
    path('StudentPage/', student_view.StudentPage),
    path('add_application/', student_view.add_application),
    path('allproject/', student_view.allproject),
    path('all_bonus_student/', student_view.all_bonus_student),
    path('my_application/', student_view.my_application),
    path('my_application_list/', student_view.my_application_list),
    path('details_application/', student_view.details_application_page),
    path('get_major/', student_view.get_major),
    path('update_student_pwd/', student_view.update_student_pwd),

    # 管理员相关url
    path('all_student_page/', admin_view.all_student_page),
    path('all_student_list/', admin_view.all_student_list),
    path('all_teacher_page/', admin_view.all_teacher_page),
    path('all_teacher_list/', admin_view.all_teacher_list),
    path('edit_student_page/', admin_view.edit_student_page),
    path('edit_teacher_page/', admin_view.edit_teacher_page),
    path('delete_student/', admin_view.delete_student),
    path('delete_teacher/', admin_view.delete_teacher),
    path('all_application/', admin_view.all_application_page),
    path('all_application_list/', admin_view.all_application_list),
    path('admin_home/', admin_view.admin_home),
    path('update_admin_pwd/', admin_view.update_admin_pwd),
    path('admin_login_out/', views.admin_login_out),
    path('allprojectlist/', admin_view.allprojectlist),
    path('application_delete/', admin_view.application_delete),
    path('add_student/', admin_view.add_student),
    path('add_teacher/', admin_view.add_teacher),

]

