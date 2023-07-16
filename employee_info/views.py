import json
import os
from datetime import timedelta, datetime

from django.core.paginator import EmptyPage, Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django_project import settings
from .models import EmployeeInfo


# 仿照老人信息的视图函数，完成工作人员信息的增删改查
def get_all_employees(request):
    # 定义每页显示的记录数量
    per_page = 10

    # 获取当前页码，默认为第1页
    page_number = request.GET.get('page', 1)
    try:
        # 获取指定页码的员工信息对象，并按照id字段排序
        employees = EmployeeInfo.objects.order_by('id')
        paginator = Paginator(employees, per_page)
        page = paginator.page(page_number)
        employee_data = []
        for employee in page:
            employee_dict = {
                'id': employee.id,
                'username': employee.username,
                'gender': employee.gender,
                'phone': employee.phone,
                'id_card': employee.id_card,
                'birthday': employee.birthday,
                'hire_date': employee.hire_date,
                'resign_date': employee.resign_date,
                'imgset_dir': employee.imgset_dir,
                'profile_photo': employee.profile_photo,
                'DESCRIPTION': employee.DESCRIPTION,
                'ISACTIVE': employee.ISACTIVE,
                'CREATED': employee.CREATED,
                'CREATEBY': employee.CREATEBY,
                'UPDATED': employee.UPDATED,
                'UPDATEBY': employee.UPDATEBY,
                'REMOVE': employee.REMOVE,
            }
            employee_data.append(employee_dict)

        # 构建返回的 JSON 数据
        response_data = {
            'total': paginator.count,
            'per_page': per_page,
            'current_page': page.number,
            'last_page': paginator.num_pages,
            'data': employee_data,
        }

        return JsonResponse(response_data)

    except EmptyPage:
        return JsonResponse({'message': '无效的页码'}, status=400)


@csrf_exempt
def create_employee(request):
    if request.method == 'POST':
        # 获取请求中的参数
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        id_card = request.POST.get('id_card')
        birthday = request.POST.get('birthday')
        hire_date = request.POST.get('hire_date')
        resign_date = request.POST.get('resign_date')
        DESCRIPTION = request.POST.get('DESCRIPTION')
        ISACTIVE = request.POST.get('ISACTIVE')
        CREATED = request.POST.get('CREATED')
        CREATEBY = request.POST.get('CREATEBY')
        UPDATED = request.POST.get('UPDATED')
        UPDATEBY = request.POST.get('UPDATEBY')
        REMOVE = request.POST.get('REMOVE')
        # data = json.loads(request.body.decode('utf-8'))
        # username = data.get('username')
        # gender = data.get('gender')
        # phone = data.get('phone')
        # id_card = data.get('id_card')
        # birthday = data.get('birthday')
        # hire_date = data.get('hire_date')
        # resign_date = data.get('resign_date')
        # DESCRIPTION = data.get('DESCRIPTION')
        # ISACTIVE = data.get('ISACTIVE')
        # CREATED = data.get('CREATED')
        # CREATEBY = data.get('CREATEBY')
        # UPDATED = data.get('UPDATED')
        # UPDATEBY = data.get('UPDATEBY')
        # REMOVE = data.get('REMOVE')
        # 如果imgset_dir和profile_photo没有传入，则设置默认值
        imgset_dir_path = os.path.join(settings.BASE_DIR, 'static', 'imgset_dir/default.jpg')
        profile_photo_path = os.path.join(settings.BASE_DIR, 'static', 'profile_photo/default.jpg')
        imgset_dir_whole_path = os.path.join('imgset_dir', 'default.jpg')
        profile_photo_whole_path = os.path.join('profile_photo', 'default.jpg')
        # 如果传入的imgset_dir和profile_photo是文件，需要使用request.FILES.get()方法获取
        # 传的imgset_dir是一个文件，传的profile_photo是一个文件
        if request.FILES.get('imgset_dir'):
            imgset_dir = request.FILES.get('imgset_dir')
            # 将文件保存到..static/imgset_dir
            # 保存文件的路径
            imgset_dir_path = os.path.join(settings.BASE_DIR, 'static', 'imgset_dir')
            imgset_dir_whole_path = os.path.join('imgset_dir', imgset_dir.name)
            # 保存文件
            if not os.path.exists(imgset_dir_path):
                os.makedirs(imgset_dir_path)
            with open(os.path.join(imgset_dir_path, imgset_dir.name), 'wb') as f:
                for chunk in imgset_dir.chunks():
                    f.write(chunk)
        if request.FILES.get('profile_photo'):
            profile_photo = request.FILES.get('profile_photo')
            # 将文件保存到..static/profile_photo
            # 保存文件的路径
            profile_photo_path = os.path.join(settings.BASE_DIR, 'static', 'profile_photo')
            profile_photo_whole_path = os.path.join('profile_photo', profile_photo.name)
            # 保存文件
            if not os.path.exists(profile_photo_path):
                os.makedirs(profile_photo_path)
            with open(os.path.join(profile_photo_path, profile_photo.name), 'wb') as f:
                for chunk in profile_photo.chunks():
                    f.write(chunk)
        # 打印出来看看
        print(imgset_dir_whole_path)
        print(profile_photo_whole_path)

        # 创建EmployeeInfo对象并保存到数据库
        employee = EmployeeInfo(
            username=username,
            gender=gender,
            phone=phone,
            id_card=id_card,
            birthday=birthday,
            hire_date=hire_date,
            resign_date=resign_date,
            imgset_dir=imgset_dir_whole_path,
            profile_photo=profile_photo_whole_path,
            DESCRIPTION=DESCRIPTION,
            ISACTIVE=ISACTIVE,
            CREATED=CREATED,
            CREATEBY=CREATEBY,
            UPDATED=UPDATED,
            UPDATEBY=UPDATEBY,
            REMOVE=REMOVE
        )
        employee.save()

        return JsonResponse({'message': '工作人员信息录入成功'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def update_employee(request, employee_id):
    if request.method == 'PUT':
        try:
            # 获取要更新的义工信息对象
            data = json.loads(request.body.decode('utf-8'))
            employee = EmployeeInfo.objects.get(id=employee_id)

            # 更新义工信息
            if data.get('name'):
                employee.name = data.get('name')
            if data.get('gender'):
                employee.gender = data.get('gender')
            if data.get('phone'):
                employee.phone = data.get('phone')
            if data.get('id_card'):
                employee.id_card = data.get('id_card')
            if data.get('birthday'):
                employee.birthday = data.get('birthday')
            if data.get('hire_date'):
                employee.hire_date = data.get('hire_date')
            if data.get('resign_date'):
                employee.resign_date = data.get('resign_date')
            if data.get('imgset_dir'):
                employee.imgset_dir = data.get('imgset_dir')
            if data.get('profile_photo'):
                employee.profile_photo = data.get('profile_photo')
            if data.get('DESCRIPTION'):
                employee.DESCRIPTION = data.get('DESCRIPTION')
            if data.get('ISACTIVE'):
                employee.ISACTIVE = data.get('ISACTIVE')
            if data.get('CREATED'):
                employee.CREATED = data.get('CREATED')
            if data.get('CREATEBY'):
                employee.CREATEBY = data.get('CREATEBY')
            if data.get('UPDATED'):
                employee.UPDATED = data.get('UPDATED')
            if data.get('UPDATEBY'):
                employee.UPDATEBY = data.get('UPDATEBY')
            if data.get('REMOVE'):
                employee.REMOVE = data.get('REMOVE')

            # 保存更新后的义工信息
            employee.save()

            return JsonResponse({'message': '义工信息更新成功'})

        except EmployeeInfo.DoesNotExist:
            return JsonResponse({'message': '义工信息不存在'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)


def get_employee(request, employee_id):
    try:
        employee = EmployeeInfo.objects.get(id=employee_id)

        employee_data = {
            'id': employee.id,
            'username': employee.username,
            'gender': employee.gender,
            'phone': employee.phone,
            'id_card': employee.id_card,
            'birthday': employee.birthday,
            'hire_date': employee.hire_date,
            'resign_date': employee.resign_date,
            'imgset_dir': employee.imgset_dir,
            'profile_photo': employee.profile_photo,
            'DESCRIPTION': employee.DESCRIPTION,
            'ISACTIVE': employee.ISACTIVE,
            'CREATED': employee.CREATED,
            'CREATEBY': employee.CREATEBY,
            'UPDATED': employee.UPDATED,
            'UPDATEBY': employee.UPDATEBY,
            'REMOVE': employee.REMOVE
        }

        return JsonResponse({'employee': employee_data})

    except EmployeeInfo.DoesNotExist:
        return JsonResponse({'message': '工作人员信息不存在'})


@csrf_exempt
def delete_employee(request, employee_id):
    if request.method == 'DELETE':
        try:
            employee = EmployeeInfo.objects.get(id=employee_id)
            employee.delete()
            return JsonResponse({'message': '工作人员信息删除成功'})
        except EmployeeInfo.DoesNotExist:
            return JsonResponse({'message': '工作人员信息不存在'})
    return JsonResponse({'message': 'Method not allowed'}, status=405)


# 图片上传等功能需要使用第三方库，例如Pillow、django-storages等。具体实现会有所不同，需要根据具体需求进行调整。统计分析功能也需要根据具体需求进行编写。

# 入职离职按时间统计人数
def get_number(request):
    if request.method == 'GET':
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
                # 获取入职时间在该月份的人数
                checkin_month = EmployeeInfo.objects.filter(hire_date__year=year, hire_date__month=month).count()
                # 获取离职时间在该月份的人数
                checkout_month = EmployeeInfo.objects.filter(resign_date__year=year, resign_date__month=month).count()
                response_data.append({
                    'month': month,
                    'checkin_month': checkin_month,
                    'checkout_month': checkout_month,
                })
            return JsonResponse({'response_data': response_data})

        # # 获取所有入职离职时间
        # hire_date = EmployeeInfo.objects.values_list('hire_date', flat=True)
        # resign_date = EmployeeInfo.objects.values_list('resign_date', flat=True)
        # # 将时间转换为字符串
        # hire_date = [str(i) for i in hire_date]
        # resign_date = [str(i) for i in resign_date]
        # # 统计每个时间出现的次数
        # hire_date_dict = {}
        # for i in hire_date:
        #     hire_date_dict[i] = hire_date.count(i)
        # resign_date_dict = {}
        # for i in resign_date:
        #     resign_date_dict[i] = resign_date.count(i)
        # # 将字典转换为列表
        # hire_date_list = []
        # for k, v in hire_date_dict.items():
        #     hire_date_list.append([k, v])
        # resign_date_list = []
        # for k, v in resign_date_dict.items():
        #     resign_date_list.append([k, v])
        # # 将列表按时间排序
        # hire_date_list.sort(key=lambda x: x[0])
        # resign_date_list.sort(key=lambda x: x[0])
        # # 将列表转换为字典
        # hire_date_dict = dict(hire_date_list)
        # resign_date_dict = dict(resign_date_list)
        # # 将字典转换为列表
        # hire_date_list = []
        # for k, v in hire_date_dict.items():
        #     hire_date_list.append([k, v])
        # resign_date_list = []
        # for k, v in resign_date_dict.items():
        #     resign_date_list.append([k, v])
        # # 将列表转换为json
        # hire_date_json = json.dumps(hire_date_list)
        # resign_date_json = json.dumps(resign_date_list)
        # # 返回json
        # return JsonResponse({'hire_date': hire_date_json, 'resign_date': resign_date_json})
