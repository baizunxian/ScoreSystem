from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from score.models import Student, Teacher, AdminUser


# Create your views here.


def welcome(request):
    """
    欢迎页
    :param request:
    :return:
    """
    return render(request, 'welcome.html')


def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == "POST":
        number = request.POST.get('number', None)
        pwd = request.POST.get('pwd', None)
        user_type = request.POST.get('user_type', None)
        # 判断有没有类型，根据类型来判断是查学生表，还是老师表
        if user_type:
            # 如果类型等于老师的话，走老师的逻辑
            if user_type == 'Teacher':
                # 判断数据库有没有当前用户
                if Teacher.objects.filter(TStaff_number=number).exists():
                    # 如果有，看用户名和密码匹不匹配
                    t_info = Teacher.objects.filter(TStaff_number=number, TPwd=pwd)
                    if t_info.exists():
                        # 记录session
                        request.session['TStaff_number'] = number
                        request.session['Teacher_id'] = t_info[0].id
                        data = {
                            'code': 0,
                            'msg': '登录成功！',
                            'url': '/TeacherPage/'
                        }
                        return JsonResponse(data)
                    else:
                        data = {
                            'code': 1,
                            'msg': '职工号或密码错误！',
                        }
                        return JsonResponse(data)
                else:
                    data = {
                        'code': 2,
                        'msg': '账号不存在！',
                    }
                    return JsonResponse(data)
            elif user_type == 'Student':
                if Student.objects.filter(Student_id=number).exists():
                    s_info = Student.objects.filter(Student_id=number, SPwd=pwd)
                    if s_info.exists():
                        request.session['Student_number'] = number
                        request.session['Student_id'] = s_info[0].id
                        data = {
                            'code': 0,
                            'msg': '登录成功！',
                            'url': '/StudentPage/'
                        }
                        return JsonResponse(data)
                    else:
                        data = {
                            'code': 1,
                            'msg': '账号或密码错误！',
                        }
                        return JsonResponse(data)
                else:
                    data = {
                        'code': 2,
                        'msg': '账号不存在！',
                    }
                    return JsonResponse(data)
        else:
            data = {
                'code': 3,
                'msg': '用户类型不能为空！',
            }
            return JsonResponse(data)
    else:
        return render(request, 'login.html')


def student_loginout(request):
    """
    退出登录
    :param request:
    :return:
    """
    if request.method == "GET":
        try:
            del request.session['Student_name']
            del request.session['Student_id']
        except KeyError as e:
            print(e)
        return redirect('/login/')


def teacher_loginout(request):
    """
    退出登录
    :param request:
    :return:
    """
    if request.method == "GET":
        try:
            del request.session['Teacher_name']
            del request.session['Teacher_id']
        except KeyError as e:
            print(e)
        return redirect('/login/')


def admin_login(request):
    admin_name = request.POST.get('admin_name')
    admin_pwd = request.POST.get('admin_pwd')
    if AdminUser.objects.filter(admin_name=admin_name, admin_pwd=admin_pwd).exists():
        admin_info = AdminUser.objects.filter(admin_name=admin_name, admin_pwd=admin_pwd)[0]
        request.session['admin_name'] = admin_info.admin_name
        request.session['admin_id'] = admin_info.id
        return JsonResponse("OK", safe=False)
    else:
        return JsonResponse({"error_msg": "用户名或者密码错误！"})


def admin(request):
    return render(request, 'admin_login.html')


def admin_login_out(request):
    """
    管理员退出
    :param request:
    :return:
    """
    if request.method == "GET":
        try:
            del request.session['admin_name']
            del request.session['admin_id']
        except KeyError as e:
            print(e)
        return redirect('/admin/')
