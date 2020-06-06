from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from score.models import Bonus, Teacher, Application


def TeacherPage(request):
    """
    老师，主页
    :param request:
    :return:
    """
    return render(request, 'TeacherPage.html')


def add_Scholarship(request):
    """
    老师添加添加奖学金
    :param request:
    :return:
    """
    print(request.POST)
    if request.method == "POST":
        bonus_name = request.POST.get('bonus_name', None)
        startup_time = request.POST.get('startup_time', None)
        credit_and_GPA = request.POST.get('credit_and_GPA', None)
        dormitory_standard = request.POST.get('dormitory_standard', None)
        volunteer_hours = request.POST.get('volunteer_hours', None)
        credit = request.POST.get('credit', None)
        bonus_type = request.POST.get('bonus_type', None)
        Teacher_id = request.POST.get('Teacher_id', None)
        # 查询数据有没有相同名字的项目
        if Bonus.objects.filter(bonus_name=bonus_name):
            data = {
                'code': 1,
                'msg': '添加失败，项目名称重复！'
            }
            return JsonResponse(data)
        else:
            # 新增项目
            prize = Bonus()
            prize.bonus_name = bonus_name
            prize.start_time = startup_time.split(' ~ ')[0]
            prize.end_time = startup_time.split(' ~ ')[1]
            prize.credit_and_GPA = credit_and_GPA
            prize.dormitory_standard = dormitory_standard
            prize.volunteer_hours = volunteer_hours
            prize.credit = credit
            prize.bonus_type = bonus_type
            prize.Tuser_id = Teacher_id
            prize.save()
            data = {
                'code': 0,
                'msg': '添加成功！'
            }
            return JsonResponse(data)
    else:
        return render(request, 'add_Bonus.html')


def bonus_delete(request):
    """
    删除奖项接口
    :param request:
    :return:
    """
    bonus_id = request.POST.get('id')
    Bonus.objects.get(id=bonus_id).delete()
    data = {
        'code': 0,
        'msg': '删除成功！'
    }
    return JsonResponse(data)


def toEditbonusPage(request):
    """
    老师编辑奖项页面
    :param request:
    :return:
    """
    if request.method == "POST":
        bonus_id = request.POST.get('bonus_id', None)
        bonus_name = request.POST.get('bonus_name', None)
        startup_time = request.POST.get('startup_time', None)
        credit_and_GPA = request.POST.get('credit_and_GPA', None)
        dormitory_standard = request.POST.get('dormitory_standard', None)
        volunteer_hours = request.POST.get('volunteer_hours', None)
        credit = request.POST.get('credit', None)
        bonus_type = request.POST.get('bonus_type', None)
        bonus_info = Bonus.objects.get(id=bonus_id)
        bonus_info.bonus_name = bonus_name
        bonus_info.start_time = startup_time.split(' ~ ')[0]
        bonus_info.end_time = startup_time.split(' ~ ')[1]
        bonus_info.credit_and_GPA = credit_and_GPA
        bonus_info.dormitory_standard = dormitory_standard
        bonus_info.volunteer_hours = volunteer_hours
        bonus_info.credit = credit
        bonus_info.bonus_type = bonus_type
        bonus_info.save()
        data = {
            'code': 0,
            'msg': '修改成功！'
        }
        return JsonResponse(data)
    else:
        bonus_id = request.GET.get('id')
        bonus_info = Bonus.objects.get(id=bonus_id)
        return render(request, 'edit_bonus.html', {'bonus_info': bonus_info})


def update_teacher_pwd(request):
    # 更新老师密码
    if request.method == "POST":
        # 从session 中获取 老师id 登录的时候写入的session ->Teacher_id
        teacher_id = request.session.get('Teacher_id')
        old_pwd = request.POST.get('oldPwd')
        new_pwd = request.POST.get('newPwd')
        if old_pwd and new_pwd:
            teacher_info = Teacher.objects.get(id=teacher_id)
            if old_pwd == teacher_info.TPwd:
                teacher_info.TPwd = new_pwd
                teacher_info.save()
                return JsonResponse('OK', safe=False)
            else:
                return JsonResponse('ERROR', safe=False)
        else:
            return JsonResponse('False', safe=False)
    else:
        return render(request, 'update_teacher_pwd.html')


def approval_application_page(request):
    """
    老师审批页面
    :param request:
    :return:
    """
    if request.method == "POST":
        Tid = request.POST.get('Tid')
        Aid = request.POST.get('Aid')
        approval_remarks = request.POST.get('approval_remarks', None)
        country_fraction = request.POST.get('country_fraction', None)
        province_fraction = request.POST.get('province_fraction', None)
        school_fraction = request.POST.get('school_fraction', None)
        application_state = request.POST.get('application_state', None)
        application_info = Application.objects.get(id=Aid)
        application_info.Tuser_id = Tid
        application_info.approval_remarks = approval_remarks
        application_info.country_fraction = country_fraction
        application_info.province_fraction = province_fraction
        application_info.school_fraction = school_fraction
        if application_state and application_state == "1":
            application_info.application_state = 1
        else:
            application_info.application_state = 2
        application_info.save()
        data = {
            'code': 0,
            'msg': '审批成功！'
        }
        return JsonResponse(data)
    else:
        Aid = request.GET.get('Aid')
        application_info = Application.objects.get(id=Aid)
        return render(request, 'approval_application.html', {'application_info': application_info})


def teacher_college_application_page(request):
    """
    老师-我的学院申请页面
    :param request:
    :return:
    """
    return render(request, 'teacher_college_application.html')


def teacher_college_application_list(request):
    """
    我学院的审批数据组装
    :param request:
    :return:
    """
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    start = (int(page) - 1) * int(limit)
    end = start + int(limit)
    Tuser_id = request.session.get('Teacher_id')
    TCollege = Teacher.objects.get(id=Tuser_id).TCollege
    print(TCollege)
    all_application = Application.objects.filter(college_id=TCollege, application_state=0)[start:end]
    all_application_count = Application.objects.filter(college_id=TCollege, application_state=0).count()
    data = list()
    for application in all_application:
        application_dict = dict()
        application_dict['id'] = application.id
        application_dict['school_year'] = application.school_year
        application_dict['college'] = application.college.college_name
        application_dict['major'] = application.major.major_name
        application_dict['year_shift'] = application.year_shift
        application_dict['credit_and_GPA'] = application.credit_and_GPA
        application_dict['dormitory_standard'] = application.dormitory_standard
        application_dict['volunteer_hours'] = application.volunteer_hours
        application_dict['comprehensive_results'] = application.comprehensive_results
        application_dict['activity_quantification'] = application.activity_quantification
        application_dict['Suser'] = application.Suser.SName
        data.append(application_dict)
    respe = {
        "msg": "success",
        "code": "0",
        "count": all_application_count,
        "data": data
    }
    return JsonResponse(respe)


def teacher_Approved_page(request):
    """
    老师查看我以审批的页面
    :param request:
    :return:
    """
    return render(request, 'teacher_Approved_page.html')


def teacher_Approved_page_list(request):
    """
    老师，我的审批数据组装
    :param request:
    :return:
    """
    Tuser_id = request.session.get('Teacher_id')
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    start = (int(page) - 1) * int(limit)
    end = start + int(limit)
    teacher_Approved = Application.objects.filter(~Q(application_state=0), Tuser_id=Tuser_id)[start:end]
    teacher_Approved_count = Application.objects.filter(~Q(application_state=0), Tuser_id=Tuser_id).count()
    data = list()
    for application in teacher_Approved:
        application_dict = dict()
        application_dict['id'] = application.id
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
        data.append(application_dict)
    respe = {
        "msg": "success",
        "code": "0",
        "count": teacher_Approved_count,
        "data": data
    }
    return JsonResponse(respe)
