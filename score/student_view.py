import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from score.models import Bonus, Student, Application, College, Major


def StudentPage(request):
    """
    学生主页
    :param request:
    :return:
    """
    return render(request, 'StudentPage.html')


def allproject(request):
    """
    所有项目页面, 学生查看
    :param request:
    :return:
    """
    return render(request, 'all_bonus.html')


def update_student_pwd(request):
    """
    根据学生密码
    :param request:
    :return:
    """
    if request.method == "POST":
        # 从session 中获取学生id 登录的时候写入的session ->Student_id
        student_id = request.session.get('Student_id')
        old_pwd = request.POST.get('oldPwd')
        new_pwd = request.POST.get('newPwd')
        if old_pwd and new_pwd:
            student_info = Student.objects.get(id=student_id)
            if old_pwd == student_info.SPwd:
                student_info.SPwd = new_pwd
                student_info.save()
                return JsonResponse('OK', safe=False)
            else:
                return JsonResponse('ERROR', safe=False)
        else:
            return JsonResponse('False', safe=False)
    else:
        return render(request, 'update_student_pwd.html')


def add_application(request):
    """
    学生提交申请
    :param request:
    :return:
    """
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        new_date = datetime.datetime.now()
        Sid = request.POST.get('Sid')
        Bid = request.POST.get('Bid')
        bonus_info = Bonus.objects.get(id=Bid)
        bonus_start_time = bonus_info.start_time
        bonus_end_time = bonus_info.end_time
        if new_date >= bonus_start_time and new_date <= bonus_end_time:
            school_year = request.POST.get('school_year')
            college = request.POST.get('college')
            major = request.POST.get('major')
            year_shift = request.POST.get('year_shift')
            credit_and_GPA = request.POST.get('credit_and_GPA')
            dormitory_standard = request.POST.get('dormitory_standard')
            volunteer_hours = request.POST.get('volunteer_hours')
            comprehensive_results = request.POST.get('comprehensive_results')
            activity_quantification = request.POST.get('activity_quantification')
            research_project = request.POST.get('research_project')
            remarks = request.POST.get('remarks')
            country_image = request.FILES.get('country_image')
            province_image = request.FILES.get('province_image')
            school_image = request.FILES.get('school_image')
            application_info = Application()
            application_info.school_year = school_year
            application_info.Suser_id = Sid
            application_info.bonus_id = Bid
            application_info.college_id = college
            application_info.major_id = major
            application_info.year_shift = year_shift
            application_info.credit_and_GPA = credit_and_GPA
            application_info.dormitory_standard = dormitory_standard
            application_info.volunteer_hours = volunteer_hours
            application_info.comprehensive_results = comprehensive_results
            application_info.activity_quantification = activity_quantification
            application_info.research_project = research_project
            application_info.remarks = remarks
            application_info.country_image = country_image
            application_info.province_image = province_image
            application_info.school_image = school_image
            application_info.save()
            return HttpResponse("提交申请成功！")
        else:
            return HttpResponse("当前申请时间不在申请时间范围内！")
    else:
        Bid = request.GET.get('Bid')
        Sid = request.session.get('Student_id')
        student_info = Student.objects.get(id=Sid)
        bonus_info = Bonus.objects.get(id=Bid)
        all_college = College.objects.all()
        data = {
            'student_info': student_info,
            'bonus_info': bonus_info,
            'all_college': all_college
        }
        return render(request, 'add_application.html', data)


def get_major(request):
    """
    根据学院获取专业，接口
    :param request:
    :return:
    """
    major_list = list()
    Cid = request.POST.get('Cid', None)
    if Cid and Cid != '':
        all_major = Major.objects.filter(college_id=Cid)
    else:
        return JsonResponse(major_list, safe=False)
    if all_major:
        for major in all_major:
            major_dict = dict()
            major_dict['id'] = major.id
            major_dict['major_name'] = major.major_name
            major_list.append(major_dict)
    else:
        return JsonResponse(major_list, safe=False)
    return JsonResponse(major_list, safe=False)


def all_bonus_student(request):
    """
    学生展示所有奖项页面
    :param request:
    :return:
    """
    return render(request, 'all_bonus_student.html')


def my_application(request):
    """
    学生，查看我的申请
    :param request:
    :return:
    """
    return render(request, 'my_application.html')


def my_application_list(request):
    """
    学生，我的申请数据组装
    :param request:
    :return:
    """
    Suser_id  = request.session.get('Student_id')
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    start = (int(page) - 1) * int(limit)
    end = start + int(limit)
    my_application = Application.objects.filter(Suser_id=Suser_id)[start:end]
    my_application_count = Application.objects.filter(Suser_id=Suser_id).count()
    data = list()
    for application in my_application:
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
        "count": my_application_count,
        "data": data
    }
    return JsonResponse(respe)


def details_application_page(request):
    """
    学生查看我的申请详情
    :param request:
    :return:
    """
    Aid = request.GET.get('Aid')
    application_info = Application.objects.get(id=Aid)
    return render(request, 'details_application.html', {'application_info': application_info})