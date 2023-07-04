from django.shortcuts import render
from django.http import JsonResponse
from .models import VolunteerInfo


def create_volunteer(request):
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        id_card = request.POST.get('id_card')
        birthday = request.POST.get('birthday')
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        imgset_dir = request.POST.get('imgset_dir')
        profile_photo = request.POST.get('profile_photo')
        DESCRIPTION = request.POST.get('DESCRIPTION')
        ISACTIVE = request.POST.get('ISACTIVE')
        CREATED = request.POST.get('CREATED')
        CREATEBY = request.POST.get('CREATEBY')
        UPDATED = request.POST.get('UPDATED')
        UPDATEBY = request.POST.get('UPDATEBY')
        REMOVE = request.POST.get('REMOVE')

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


def update_volunteer(request, volunteer_id):
    if request.method == 'POST':
        try:
            # 获取要更新的义工信息对象
            volunteer = VolunteerInfo.objects.get(id=volunteer_id)

            # 更新义工信息
            volunteer.name = request.POST.get('name')
            volunteer.gender = request.POST.get('gender')
            volunteer.phone = request.POST.get('phone')
            volunteer.id_card = request.POST.get('id_card')
            volunteer.birthday = request.POST.get('birthday')
            volunteer.checkin_date = request.POST.get('checkin_date')
            volunteer.checkout_date = request.POST.get('checkout_date')
            volunteer.imgset_dir = request.POST.get('imgset_dir')
            volunteer.profile_photo = request.POST.get('profile_photo')
            volunteer.DESCRIPTION = request.POST.get('DESCRIPTION')
            volunteer.ISACTIVE = request.POST.get('ISACTIVE')
            volunteer.CREATED = request.POST.get('CREATED')
            volunteer.CREATEBY = request.POST.get('CREATEBY')
            volunteer.UPDATED = request.POST.get('UPDATED')
            volunteer.UPDATEBY = request.POST.get('UPDATEBY')
            volunteer.REMOVE = request.POST.get('REMOVE')

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
            # 其他字段同理
        }

        return JsonResponse({'volunteer': volunteer_data})

    except VolunteerInfo.DoesNotExist:
        return JsonResponse({'message': '义工信息不存在'})


def delete_volunteer(request, volunteer_id):
    try:
        # 获取要删除的义工信息对象
        volunteer = VolunteerInfo.objects.get(id=volunteer_id)

        # 删除义工信息
        volunteer.delete()

        return JsonResponse({'message': '义工信息删除成功'})

    except VolunteerInfo.DoesNotExist:
        return JsonResponse({'message': '义工信息不存在'})
