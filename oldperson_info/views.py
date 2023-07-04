import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
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
                # 其他字段同理
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

        # 更新字段
        old_person.username = username
        old_person.gender = gender
        old_person.phone = phone
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
            # 其他字段同理
        }

        return JsonResponse({'old_person': old_person_data})

    except OldPersonInfo.DoesNotExist:
        return JsonResponse({'message': '老人信息不存在'})

    # 处理其他HTTP方法
    return JsonResponse({'message': 'Method not allowed'}, status=405)


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
