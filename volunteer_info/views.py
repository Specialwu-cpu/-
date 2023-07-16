import json
from datetime import datetime

from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import VolunteerInfo


def get_all_volunteers(request):
    # 定义每页显示的记录数量
    per_page = 10

    # 获取当前页码，默认为第1页
    page_number = request.GET.get('page', 1)
    try:
        # 获取指定页码的老人信息对象
        volunteers = VolunteerInfo.objects.order_by('id')
        paginator = Paginator(volunteers, per_page)
        page = paginator.page(page_number)
        volunteer_data = []

        # 将每个老人信息对象转换为字典形式
        for volunteer in page:
            volunteer_dict = {
                'id': volunteer.id,
                'name': volunteer.name,
                'gender': volunteer.gender,
                'phone': volunteer.phone,
                'id_card': volunteer.id_card,
                'birthday': volunteer.birthday,
                'checkin_date': volunteer.checkin_date,
                'checkout_date': volunteer.checkout_date,
                'imgset_dir': volunteer.imgset_dir,
                'profile_photo': volunteer.profile_photo,
                'DESCRIPTION': volunteer.DESCRIPTION,
                'ISACTIVE': volunteer.ISACTIVE,
                'CREATED': volunteer.CREATED,
                'CREATEBY': volunteer.CREATEBY,
                'UPDATED': volunteer.UPDATED,
                'UPDATEBY': volunteer.UPDATEBY,
                'REMOVE': volunteer.REMOVE,
            }
            volunteer_data.append(volunteer_dict)

        # 构建返回的 JSON 数据
        response_data = {
            'total': paginator.count,
            'per_page': per_page,
            'current_page': page.number,
            'last_page': paginator.num_pages,
            'data': volunteer_data,
        }

        return JsonResponse(response_data)

    except EmptyPage:
        return JsonResponse({'message': '无效的页码'}, status=400)


@csrf_exempt
def create_volunteer(request):
    if request.method == 'POST':
        # 获取表单数据
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        gender = data.get('gender')
        phone = data.get('phone')
        id_card = data.get('id_card')
        birthday = data.get('birthday')
        checkin_date = data.get('checkin_date')
        checkout_date = data.get('checkout_date')
        imgset_dir = data.get('imgset_dir')
        profile_photo = data.get('profile_photo')
        DESCRIPTION = data.get('DESCRIPTION')
        ISACTIVE = data.get('ISACTIVE')
        CREATED = data.get('CREATED')
        CREATEBY = data.get('CREATEBY')
        UPDATED = data.get('UPDATED')
        UPDATEBY = data.get('UPDATEBY')
        REMOVE = data.get('REMOVE')

        # 创建义工信息对象
        volunteer = VolunteerInfo(
            name=name,
            gender=gender,
            phone=phone,
            id_card=id_card,
            birthday=birthday,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            imgset_dir=imgset_dir,
            profile_photo=profile_photo,
            DESCRIPTION=DESCRIPTION,
            ISACTIVE=ISACTIVE,
            CREATED=CREATED,
            CREATEBY=CREATEBY,
            UPDATED=UPDATED,
            UPDATEBY=UPDATEBY,
            REMOVE=REMOVE
        )

        # 保存义工信息
        volunteer.save()

        return JsonResponse({'message': '义工信息创建成功'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def update_volunteer(request, volunteer_id):
    if request.method == 'PUT':
        try:
            # 获取要更新的义工信息对象
            data = json.loads(request.body.decode('utf-8'))
            volunteer = VolunteerInfo.objects.get(id=volunteer_id)

            # 更新义工信息
            if data.get('name'):
                volunteer.name = data.get('name')
            if data.get('gender'):
                volunteer.gender = data.get('gender')
            if data.get('phone'):
                volunteer.phone = data.get('phone')
            if data.get('id_card'):
                volunteer.id_card = data.get('id_card')
            if data.get('birthday'):
                volunteer.birthday = data.get('birthday')
            if data.get('checkin_date'):
                volunteer.checkin_date = data.get('checkin_date')
            if data.get('checkout_date'):
                volunteer.checkout_date = data.get('checkout_date')
            if data.get('imgset_dir'):
                volunteer.imgset_dir = data.get('imgset_dir')
            if data.get('profile_photo'):
                volunteer.profile_photo = data.get('profile_photo')
            if data.get('DESCRIPTION'):
                volunteer.DESCRIPTION = data.get('DESCRIPTION')
            if data.get('ISACTIVE'):
                volunteer.ISACTIVE = data.get('ISACTIVE')
            if data.get('CREATED'):
                volunteer.CREATED = data.get('CREATED')
            if data.get('CREATEBY'):
                volunteer.CREATEBY = data.get('CREATEBY')
            if data.get('UPDATED'):
                volunteer.UPDATED = data.get('UPDATED')
            if data.get('UPDATEBY'):
                volunteer.UPDATEBY = data.get('UPDATEBY')
            if data.get('REMOVE'):
                volunteer.REMOVE = data.get('REMOVE')

            # 保存更新后的义工信息
            volunteer.save()

            return JsonResponse({'message': '义工信息更新成功'})

        except VolunteerInfo.DoesNotExist:
            return JsonResponse({'message': '义工信息不存在'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)


def get_volunteer(request, volunteer_id):
    try:
        # 获取义工信息对象
        volunteer = VolunteerInfo.objects.get(id=volunteer_id)

        # 将对象转换为字典形式
        volunteer_data = {
            'id': volunteer.id,
            'name': volunteer.name,
            'gender': volunteer.gender,
            'phone': volunteer.phone,
            'id_card': volunteer.id_card,
            'birthday': volunteer.birthday,
            'checkin_date': volunteer.checkin_date,
            'checkout_date': volunteer.checkout_date,
            'imgset_dir': volunteer.imgset_dir,
            'profile_photo': volunteer.profile_photo,
            'DESCRIPTION': volunteer.DESCRIPTION,
            'ISACTIVE': volunteer.ISACTIVE,
            'CREATED': volunteer.CREATED,
            'CREATEBY': volunteer.CREATEBY,
            'UPDATED': volunteer.UPDATED,
            'UPDATEBY': volunteer.UPDATEBY,
            'REMOVE': volunteer.REMOVE,
        }

        return JsonResponse({'volunteer': volunteer_data})

    except VolunteerInfo.DoesNotExist:
        return JsonResponse({'message': '义工信息不存在'})


@csrf_exempt
def delete_volunteer(request, volunteer_id):
    if request.method == 'DELETE':
        try:
            # 获取要删除的义工信息对象
            volunteer = VolunteerInfo.objects.get(id=volunteer_id)

            # 删除义工信息
            volunteer.delete()

            return JsonResponse({'message': '义工信息删除成功'})

        except VolunteerInfo.DoesNotExist:
            return JsonResponse({'message': '义工信息不存在'})
    return JsonResponse({'message': 'Method not allowed'}, status=405)


# 入职离职按时间统计人数，数据库中只有checkin_date和checkout_date两个字段，格式为datetime
def get_number(request):
    if request.method == 'GET':
        # 获取里当前月份最近的12个月份
        # 获取当前时间
        now = datetime.now()
        # 获取当前年份
        year = now.year
        # 获取当前月份
        month = now.month
        months = []
        for i in range(12):
            # 将月份添加到列表中
            months.append(str(year) + '-' + str(month))
            # 计算出当前月份的上一个月份
            if month == 1:
                month = 12
                year -= 1
            else:
                month -= 1

        print(months)
        # 按照月份统计入职人数
        response_data = []
        for month in months:
            # 获取年份和月份
            year = int(month.split('-')[0])
            month = int(month.split('-')[1])
            # 按照月份统计入职人数
            checkin_month = VolunteerInfo.objects.filter(checkin_date__year=year, checkin_date__month=month).count()
            # 按照月份统计离职人数
            checkout_month = VolunteerInfo.objects.filter(checkout_date__year=year, checkout_date__month=month).count()
            response_data.append({
                'month': month,
                'checkin_month': checkin_month,
                'checkout_month': checkout_month,
            })
        return JsonResponse({'response_data': response_data})

        # this_year_checkin = VolunteerInfo.objects.filter(checkin_date__year=year).count()
        # # 获取今年离职人数
        # this_year_checkout = VolunteerInfo.objects.filter(checkout_date__year=year).count()
        # # 获取去年入职人数
        # last_year_checkin = VolunteerInfo.objects.filter(checkin_date__year=year - 1).count()
        # # 获取去年离职人数
        # last_year_checkout = VolunteerInfo.objects.filter(checkout_date__year=year - 1).count()
        # # 获取去年以前入职人数
        # before_last_year_checkin = VolunteerInfo.objects.filter(checkin_date__year__lt=year - 1).count()
        # # 获取去年以前离职人数
        # before_last_year_checkout = VolunteerInfo.objects.filter(checkout_date__year__lt=year - 1).count()
        #
        # response_data = {
        #     'this_year_checkin': this_year_checkin,
        #     'this_year_checkout': this_year_checkout,
        #     'last_year_checkin': last_year_checkin,
        #     'last_year_checkout': last_year_checkout,
        #     'before_last_year_checkin': before_last_year_checkin,
        #     'before_last_year_checkout': before_last_year_checkout
        # }

        return JsonResponse(response_data)
