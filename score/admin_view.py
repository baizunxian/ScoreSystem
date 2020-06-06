from django.http import JsonResponse
from django.shortcuts import render
from django.db import transaction

from score.modelsJson import BonusSerializers
from score.tasks import delete_user

from score.models import Student, Application, Teacher, College, AdminUser, Bonus


def admin_home(request):
    return render(request, 'adminhome.html')


def update_admin_pwd(request):
    if request.method == 'POST':
        admin_id = request.session.get('admin_id')
        oldPwd = request.POST.get('oldPwd')
        newPwd = request.POST.get('newPwd')
        if oldPwd and newPwd:
            admin_info = AdminUser.objects.get(id=admin_id)
            if oldPwd == admin_info.admin_pwd:
                admin_info.admin_pwd = newPwd
                admin_info.save()
                return JsonResponse('OK', safe=False)
            else:
                return JsonResponse('ERROR', safe=False)
        else:
            return JsonResponse('False', safe=False)
    else:
        return render(request, 'update_admin_pwd.html')


def all_student_page(request):
    """
    所有学生页面
    :param request:
    :return:
    """
    return render(request, 'all_student_page.html')


def all_teacher_page(request):
    """
    所有学生页面
    :param request:
    :return:
    """
    return render(request, 'all_teacher_page.html')


def all_student_list(request):
    """
    所有学生，数据组装
    :param request:
    :return:
    """
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    Student_id = request.GET.get('Student_id', None)
    start = (int(page) - 1) * int(limit)
    end = start + int(limit)
    all_student = Student.get_student_by_id(Student_id)[start:end]
    all_student_count = Student.get_student_by_id(Student_id).count()
    data = list()
    for student in all_student:
        student_dict = dict()
        student_dict['id'] = student.id
        student_dict['SName'] = student.SName
        student_dict['SPwd'] = student.SPwd
        student_dict['SCollege'] = student.SCollege.college_name
        student_dict['SMajor'] = student.SMajor.major_name
        student_dict['Student_id'] = student.Student_id
        student_dict['SSex'] = student.SSex
        student_dict['SPhoneNumber'] = student.SPhoneNumber
        student_dict['SIDCard'] = student.SIDCard
        data.append(student_dict)
    respe = {
        "msg": "success",
        "code": "0",
        "count": all_student_count,
        "data": data
    }
    return JsonResponse(respe)


def all_teacher_list(request):
    """
    所有老师，数据组装
    :param request:
    :return:
    """
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    TStaff_number = request.GET.get('TStaff_number')
    start = (int(page) - 1) * int(limit)
    end = start + int(limit)
    all_teacher = Teacher.get_teacher_by_id(TStaff_number)[start:end]
    all_teacher_count = Teacher.get_teacher_by_id(TStaff_number).count()
    data = list()
    for teacher in all_teacher:
        teacher_dict = dict()
        teacher_dict['id'] = teacher.id
        teacher_dict['TName'] = teacher.TName
        teacher_dict['TPwd'] = teacher.TPwd
        teacher_dict['TCollege'] = teacher.TCollege.college_name
        teacher_dict['TStaff_number'] = teacher.TStaff_number
        teacher_dict['TSex'] = teacher.TSex
        teacher_dict['TPhoneNumber'] = teacher.TPhoneNumber
        teacher_dict['TIDCard'] = teacher.TIDCard
        data.append(teacher_dict)
    respe = {
        "msg": "success",
        "code": "0",
        "count": all_teacher_count,
        "data": data
    }
    return JsonResponse(respe)


def edit_student_page(request):
    """
    学生修改页面，以及修改
    :param request:
    :return:
    """
    # post 请求修改学生信息
    if request.method == "POST":
        print(request.POST)
        Sid = request.POST.get('Sid')
        SName = request.POST.get('SName')
        SPwd = request.POST.get('SPwd')
        Student_id = request.POST.get('Student_id')
        SPhoneNumber = request.POST.get('SPhoneNumber')
        SIDCard = request.POST.get('SIDCard')
        SSex = request.POST.get('SSex')
        college = request.POST.get('college')
        major = request.POST.get('major')
        student_info = Student.objects.get(id=Sid)
        student_info.SName = SName
        student_info.SPwd = SPwd
        student_info.Student_id = Student_id
        student_info.SPhoneNumber = SPhoneNumber
        student_info.SIDCard = SIDCard
        student_info.SSex = SSex
        student_info.SCollege_id = college
        student_info.SMajor_id = major
        student_info.save()
        data = {
            'code': 0,
            'msg': '修改成功！'
        }
        return JsonResponse(data)
    # get请求 返回修改页面
    else:
        sid = request.GET.get('id')
        student_info = Student.objects.get(id=sid)
        all_college = College.objects.all()
        data = {
            "student_info": student_info,
            "all_college": all_college
        }
        return render(request, 'edit_student.html', data)


def edit_teacher_page(request):
    """
    老师修改页面，以及修改
    :param request:
    :return:
    """
    # post 请求修改老师信息
    if request.method == "POST":
        Tid = request.POST.get('Tid')
        TName = request.POST.get('TName')
        TPwd = request.POST.get('TPwd')
        TStaff_number = request.POST.get('TStaff_number')
        TPhoneNumber = request.POST.get('TPhoneNumber')
        TIDCard = request.POST.get('TIDCard')
        TSex = request.POST.get('TSex')
        college = request.POST.get('college')
        teacher_info = Teacher.objects.get(id=Tid)
        teacher_info.TName = TName
        teacher_info.TPwd = TPwd
        teacher_info.TStaff_number = TStaff_number
        teacher_info.TPhoneNumber = TPhoneNumber
        teacher_info.TIDCard = TIDCard
        teacher_info.TSex = TSex
        teacher_info.TCollege_id = college
        teacher_info.save()
        data = {
            'code': 0,
            'msg': '修改成功！'
        }
        return JsonResponse(data)
    # get请求 返回修改页面
    else:
        Tid = request.GET.get('id')
        teacher_info = Teacher.objects.get(id=Tid)
        all_college = College.objects.all()
        data = {
            "teacher_info": teacher_info,
            "all_college": all_college
        }
        return render(request, 'edit_teacher.html', data)


def delete_student(request):
    """
    删除学生
    :param request:
    :return:
    """
    Sid = request.POST.get('Sid')
    # 异步执行
    delete_user.delay(Sid)
    # Student.objects.get(id=Sid).delete()
    data = {
        'code': 0,
        'msg': '删除成功！'
    }
    return JsonResponse(data)


def delete_teacher(request):
    """
    删除老师
    :param request:
    :return:
    """
    Tid = request.POST.get('Tid')
    Teacher.objects.get(id=Tid).delete()
    data = {
        'code': 0,
        'msg': '删除成功！'
    }
    return JsonResponse(data)


def all_application_page(request):
    all_college = College.objects.all()
    return render(request, 'all_application.html', {'all_college': all_college})


def all_application_list(request):
    """
    全部申请 查看
    :param request:
    :return:
    """
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    bonus_name = request.GET.get('bonus_name', None)
    SName = request.GET.get('SName', None)
    college = request.GET.get('college', None)
    major = request.GET.get('major', None)
    start = (int(page) - 1) * int(limit)
    end = start + int(limit)
    all_application = Application.get_search(bonus_name, SName, college, major)[start:end]
    all_application_count = Application.get_search(bonus_name, SName, college, major).count()
    data = list()
    for application in all_application:
        application_dict = dict()
        application_dict['id'] = application.id
        application_dict['bonus'] = application.bonus.bonus_name
        application_dict['school_year'] = application.school_year
        application_dict['college'] = application.college.college_name
        application_dict['major'] = application.major.major_name
        application_dict['year_shift'] = application.year_shift
        application_dict['credit_and_GPA'] = application.credit_and_GPA
        application_dict['dormitory_standard'] = application.dormitory_standard
        application_dict['volunteer_hours'] = application.volunteer_hours
        application_dict['comprehensive_results'] = application.comprehensive_results
        application_dict['activity_quantification'] = application.activity_quantification
        application_dict['application_state'] = application.application_state
        application_dict['Suser'] = application.Suser.SName
        if application.Tuser:
            application_dict['Tuser'] = application.Tuser.TName
        else:
            application_dict['Tuser'] = ''

        # 学分绩点+量化+赋值
        if application.country_fraction:
            country_fraction = application.country_fraction
        else:
            country_fraction = 0
        if application.province_fraction:
            province_fraction = application.province_fraction
        else:
            province_fraction = 0
        if application.school_fraction:
            school_fraction = application.school_fraction
        else:
            school_fraction = 0

        # 判断，知否为空
        if application.comprehensive_results:
            comprehensive_results = application.comprehensive_results
        else:
            comprehensive_results = 0
        if application.activity_quantification:
            activity_quantification = application.activity_quantification
        else:
            activity_quantification = 0

        # 总赋值分
        total_fraction = country_fraction + province_fraction + school_fraction
        application_dict['total_fraction'] = total_fraction
        # 总分
        application_dict['total_score'] = comprehensive_results + activity_quantification + total_fraction
        data.append(application_dict)
    respe = {
        "msg": "success",
        "code": "0",
        "count": all_application_count,
        "data": data
    }
    return JsonResponse(respe)


def allprojectlist(request):
    """
    学生查看所有项目，数据组装
    :param request:
    :return:
    """
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    bonus_name = request.GET.get('bonus_name', None)
    start = (int(page) - 1) * int(limit)
    end = start + int(limit)
    all_bonus = Bonus.get_bonus_by_name(bonus_name)[start:end]
    all_bonus_count = Bonus.get_bonus_by_name(bonus_name).count()
    data = BonusSerializers(all_bonus, many=True)
    respe = {
        "msg": "success",
        "code": "0",
        "count": all_bonus_count,
        "data": data.data
    }
    return JsonResponse(respe)


def application_delete(request):
    Aid = request.POST.get('Aid')
    Application.objects.get(id=Aid).delete()
    data = {
        'code': 0,
        'msg': '删除成功！'
    }
    return JsonResponse(data)


def add_teacher(request):
    """
    新增老师
    :param request:
    :return:
    """
    if request.method == "POST":
        TName = request.POST.get('TName')
        TPwd = request.POST.get('TPwd')
        TStaff_number = request.POST.get('TStaff_number')
        college = request.POST.get('college')
        TPhoneNumber = request.POST.get('TPhoneNumber')
        TIDCard = request.POST.get('TIDCard')
        TSex = request.POST.get('TSex')
        # 判断职工号有没有被注册
        if Teacher.objects.filter(TStaff_number=TStaff_number).exists():
            data = {
                'code': 1,
                'msg': '当前职工号以注册！'
            }
            return JsonResponse(data)
        else:
            T_info = Teacher()
            T_info.TName = TName
            T_info.TPwd = TPwd
            T_info.TStaff_number = TStaff_number
            T_info.TCollege_id = college
            T_info.TPhoneNumber = TPhoneNumber
            T_info.TIDCard = TIDCard
            T_info.TSex = TSex
            T_info.save()
            data = {
                'code': 0,
                'msg': '新增成功！'
            }
            return JsonResponse(data)
    else:
        all_college = College.objects.all()
        return render(request, 'add_teacher.html', {'all_college': all_college})


@transaction.atomic()
def add_student(request):
    """
    新增学生
    :param request:
    :return:
    """
    print(request.POST)
    if request.method == "POST":
        SName = request.POST.get('SName')
        SPwd = request.POST.get('SPwd')
        Student_id = request.POST.get('Student_id')
        college = request.POST.get('college')
        major = request.POST.get('major')
        SPhoneNumber = request.POST.get('SPhoneNumber')
        SIDCard = request.POST.get('SIDCard')
        SSex = request.POST.get('SSex')
        if Student.objects.filter(Student_id=Student_id).exists():
            data = {
                'code': 1,
                'msg': '当前学号以注册！'
            }
            return JsonResponse(data)
        else:
            try:
                S_info = Student()
                S_info.SName = SName
                S_info.SPwd = SPwd
                S_info.Student_id = Student_id
                S_info.SCollege_id = college
                S_info.major_id = major
                S_info.SPhoneNumber = SPhoneNumber
                S_info.SIDCard = SIDCard
                S_info.SSex = SSex
                S_info.save()
                data = {
                    'code': 0,
                    'msg': '新增成功！'
                }
                return JsonResponse(data)
            except Exception as e:
                data = {
                    'code': 1,
                    'msg': '新增失败%s！' % e
                }
                return JsonResponse(data)

    else:
        all_college = College.objects.all()
        return render(request, 'add_student.html', {'all_college': all_college})
