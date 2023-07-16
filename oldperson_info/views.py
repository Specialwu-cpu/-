import json
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse

from sys_user.models import SysUser
from .models import OldPersonInfo


def get_all_old_persons(request):
    # 定义每页显示的记录数量
    per_page = 10

    # 获取当前页码，默认为第1页
    page_number = request.GET.get('page', 1)

    try:
        # 获取指定页码的老人信息对象
        old_persons = OldPersonInfo.objects.all()
        paginator = Paginator(old_persons, per_page)
        page = paginator.page(page_number)
        old_persons_data = []

        # 将每个老人信息对象转换为字典形式
        for old_person in page:
            old_person_data = {
                'ID': old_person.ID,
                'username': old_person.username,
                'gender': old_person.gender,
                'phone': old_person.phone,
                'id_card': old_person.id_card,
                'birthday': old_person.birthday,
                'checkin_date': old_person.checkin_date,
                'checkout_date': old_person.checkout_date,
                'imgset_dir': old_person.imgset_dir,
                'profile_photo': old_person.profile_photo,
                'room_number': old_person.room_number,
                'firstguardian_name': old_person.firstguardian_name,
                'firstguardian_relationship': old_person.firstguardian_relationship,
                'firstguardian_phone': old_person.firstguardian_phone,
                'firstguardian_wechat': old_person.firstguardian_wechat,
                'secondguardian_name': old_person.secondguardian_name,
                'secondguardian_relationship': old_person.secondguardian_relationship,
                'secondguardian_phone': old_person.secondguardian_phone,
                'secondguardian_wechat': old_person.secondguardian_wechat,
                'health_state': old_person.health_state,
                'DESCRIPTION': old_person.DESCRIPTION,
                'ISACTIVE': old_person.ISACTIVE,
                'CREATED': old_person.CREATED,
                'CREATEBY': old_person.CREATEBY,
                'UPDATED': old_person.UPDATED,
                'UPDATEBY': old_person.UPDATEBY,
                'REMOVE': old_person.REMOVE,
            }
            old_persons_data.append(old_person_data)

        # 构建返回的 JSON 数据
        response_data = {
            'total': paginator.count,
            'per_page': per_page,
            'current_page': page.number,
            'last_page': paginator.num_pages,
            'data': old_persons_data,
        }

        return JsonResponse(response_data)

    except EmptyPage:
        return JsonResponse({'message': '无效的页码'}, status=400)


@csrf_exempt
def create_old_person(request):
    if request.method == 'POST':
        # 从请求中获取表单数据
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        gender = data.get('gender')
        phone = data.get('phone')
        id_card = data.get('id_card')
        birthday = data.get('birthday')
        checkin_date = data.get('checkin_date')
        checkout_date = data.get('checkout_date')
        imgset_dir = data.get('imgset_dir')
        profile_photo = data.get('profile_photo')
        room_number = data.get('room_number')
        firstguardian_name = data.get('firstguardian_name')
        firstguardian_relationship = data.get('firstguardian_relationship')
        firstguardian_phone = data.get('firstguardian_phone')
        firstguardian_wechat = data.get('firstguardian_wechat')
        secondguardian_name = data.get('secondguardian_name')
        secondguardian_relationship = data.get('secondguardian_relationship')
        secondguardian_phone = data.get('secondguardian_phone')
        secondguardian_wechat = data.get('secondguardian_wechat')
        health_state = data.get('health_state')
        DESCRIPTION = data.get('description')
        ISACTIVE = data.get('is_active')
        CREATED = data.get('created')
        CREATEBY = data.get('create_by')
        UPDATED = data.get('updated')
        UPDATEBY = data.get('update_by')
        REMOVE = data.get('remove')
        # 创建老人信息对象
        old_person = OldPersonInfo(username=username,
                                   gender=gender,
                                   phone=phone,
                                   id_card=id_card,
                                   birthday=birthday,
                                   checkin_date=checkin_date,
                                   checkout_date=checkout_date,
                                   imgset_dir=imgset_dir,
                                   profile_photo=profile_photo,
                                   room_number=room_number,
                                   firstguardian_name=firstguardian_name,
                                   firstguardian_relationship=firstguardian_relationship,
                                   firstguardian_phone=firstguardian_phone,
                                   firstguardian_wechat=firstguardian_wechat,
                                   secondguardian_name=secondguardian_name,
                                   secondguardian_relationship=secondguardian_relationship,
                                   secondguardian_phone=secondguardian_phone,
                                   secondguardian_wechat=secondguardian_wechat,
                                   health_state=health_state,
                                   DESCRIPTION=DESCRIPTION,
                                   ISACTIVE=ISACTIVE,
                                   CREATED=CREATED,
                                   CREATEBY=CREATEBY,
                                   UPDATED=UPDATED,
                                   UPDATEBY=UPDATEBY,
                                   REMOVE=REMOVE)
        old_person.save()

        return JsonResponse({'message': '老人信息录入成功'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def update_old_person(request, old_person_id):
    if request.method == 'PUT':
        # 从请求中获取表单数据
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        gender = data.get('gender')
        phone = data.get('phone')
        id_card = data.get('id_card')
        birthday = data.get('birthday')
        checkin_date = data.get('checkin_date')
        checkout_date = data.get('checkout_date')
        imgset_dir = data.get('imgset_dir')
        profile_photo = data.get('profile_photo')
        room_number = data.get('room_number')
        firstguardian_name = data.get('firstguardian_name')
        firstguardian_relationship = data.get('firstguardian_relationship')
        firstguardian_phone = data.get('firstguardian_phone')
        firstguardian_wechat = data.get('firstguardian_wechat')
        secondguardian_name = data.get('secondguardian_name')
        secondguardian_relationship = data.get('secondguardian_relationship')
        secondguardian_phone = data.get('secondguardian_phone')
        secondguardian_wechat = data.get('secondguardian_wechat')
        health_state = data.get('health_state')
        DESCRIPTION = data.get('description')
        ISACTIVE = data.get('is_active')
        CREATED = data.get('created')
        CREATEBY = data.get('create_by')
        UPDATED = data.get('updated')
        UPDATEBY = data.get('update_by')
        REMOVE = data.get('remove')

        # 获取老人信息对象
        old_person = OldPersonInfo.objects.get(ID=old_person_id)

        # 只更新不为空的传入的字段
        if username:
            old_person.username = username
        if gender:
            old_person.gender = gender
        if phone:
            old_person.phone = phone
        if id_card:
            old_person.id_card = id_card
        if birthday:
            old_person.birthday = birthday
        if checkin_date:
            old_person.checkin_date = checkin_date
        if checkout_date:
            old_person.checkout_date = checkout_date
        if imgset_dir:
            old_person.imgset_dir = imgset_dir
        if profile_photo:
            old_person.profile_photo = profile_photo
        if room_number:
            old_person.room_number = room_number
        if firstguardian_name:
            old_person.firstguardian_name = firstguardian_name
        if firstguardian_relationship:
            old_person.firstguardian_relationship = firstguardian_relationship
        if firstguardian_phone:
            old_person.firstguardian_phone = firstguardian_phone
        if firstguardian_wechat:
            old_person.firstguardian_wechat = firstguardian_wechat
        if secondguardian_name:
            old_person.secondguardian_name = secondguardian_name
        if secondguardian_relationship:
            old_person.secondguardian_relationship = secondguardian_relationship
        if secondguardian_phone:
            old_person.secondguardian_phone = secondguardian_phone
        if secondguardian_wechat:
            old_person.secondguardian_wechat = secondguardian_wechat
        if health_state:
            old_person.health_state = health_state
        if DESCRIPTION:
            old_person.DESCRIPTION = DESCRIPTION
        if ISACTIVE:
            old_person.ISACTIVE = ISACTIVE
        if CREATED:
            old_person.CREATED = CREATED
        if CREATEBY:
            old_person.CREATEBY = CREATEBY
        if UPDATED:
            old_person.UPDATED = UPDATED
        if UPDATEBY:
            old_person.UPDATEBY = UPDATEBY
        if REMOVE:
            old_person.REMOVE = REMOVE
        # 其他字段同理

        # 保存更新
        old_person.save()

        return JsonResponse({'message': '老人信息修改成功'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def get_old_person(request, old_person_id):
    try:
        # 获取老人信息对象
        old_person = OldPersonInfo.objects.get(ID=old_person_id)

        # 将对象转换为字典形式
        old_person_data = {
            'ID': old_person.ID,
            'username': old_person.username,
            'gender': old_person.gender,
            'phone': old_person.phone,
            'id_card': old_person.id_card,
            'birthday': old_person.birthday,
            'checkin_date': old_person.checkin_date,
            'checkout_date': old_person.checkout_date,
            'imgset_dir': old_person.imgset_dir,
            'profile_photo': old_person.profile_photo,
            'room_number': old_person.room_number,
            'firstguardian_name': old_person.firstguardian_name,
            'firstguardian_relationship': old_person.firstguardian_relationship,
            'firstguardian_phone': old_person.firstguardian_phone,
            'firstguardian_wechat': old_person.firstguardian_wechat,
            'secondguardian_name': old_person.secondguardian_name,
            'secondguardian_relationship': old_person.secondguardian_relationship,
            'secondguardian_phone': old_person.secondguardian_phone,
            'secondguardian_wechat': old_person.secondguardian_wechat,
            'health_state': old_person.health_state,
            'DESCRIPTION': old_person.DESCRIPTION,
            'ISACTIVE': old_person.ISACTIVE,
            'CREATED': old_person.CREATED,
            'CREATEBY': old_person.CREATEBY,
            'UPDATED': old_person.UPDATED,
            'UPDATEBY': old_person.UPDATEBY,
            'REMOVE': old_person.REMOVE,
        }

        return JsonResponse({'old_person': old_person_data})

    except OldPersonInfo.DoesNotExist:
        return JsonResponse({'message': '老人信息不存在'})


@csrf_exempt
def delete_old_person(request, old_person_id):
    if request.method == 'DELETE':
        try:
            # 获取老人信息对象
            old_person = OldPersonInfo.objects.get(ID=old_person_id)

            # 删除对象
            old_person.delete()

            return JsonResponse({'message': '老人信息删除成功'})

        except OldPersonInfo.DoesNotExist:
            return JsonResponse({'message': '老人信息不存在'})

    # 处理其他HTTP方法
    return JsonResponse({'message': 'Method not allowed'}, status=405)


def get_age(birthday):
    # 获取当前日期
    current_date = datetime.now()

    # 如果生日为空，则返回0
    if not birthday:
        return 0

    # 计算年龄
    age = current_date.year - birthday.year

    # 检查是否已过生日，如果未过生日则减去一年
    if current_date.month < birthday.month or (
            current_date.month == birthday.month and current_date.day < birthday.day):
        age -= 1
    return age


def get_number(request):
    if request.method == 'GET':
        # 获取老人生日，计算所有人年龄
        old_persons = OldPersonInfo.objects.all()
        old_persons_age = []
        for old_person in old_persons:
            old_person_age = get_age(old_person.birthday)
            old_persons_age.append(old_person_age)
        # 根据年龄段计算老人数量，每十岁一个年龄段
        old_person_age_stage = {}
        for i in range(0, 10):
            # 标注具体年龄段
            age_stage = str(i * 10) + '-' + str((i + 1) * 10)
            # 计算该年龄段的老人数量
            old_person_age_stage[age_stage] = 0
            old_person_age_stage['>= 100 ages'] = 0
        for old_person_age in old_persons_age:
            for i in range(0, 10):
                if old_person_age >= i * 10 and old_person_age < (i + 1) * 10:
                    old_person_age_stage[str(i * 10) + '-' + str((i + 1) * 10)] += 1
                if old_person_age >= 100:
                    old_person_age_stage['> 100 ages'] += 1
        return JsonResponse({'old_person_age_stage': old_person_age_stage})

