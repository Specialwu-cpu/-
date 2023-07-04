from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import EmployeeInfo


@csrf_exempt
def create_employee(request):
    if request.method == 'POST':
        # 获取请求中的参数
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        # 其他字段同理

        # 创建EmployeeInfo对象并保存到数据库
        employee = EmployeeInfo(
            username=username,
            gender=gender,
            phone=phone,
            # 其他字段同理
        )
        employee.save()

        return JsonResponse({'message': '工作人员信息录入成功'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def update_employee(request, employee_id):
    if request.method == 'PUT':
        try:
            employee = EmployeeInfo.objects.get(id=employee_id)

            if request.method == 'POST':
                # 获取请求中的参数
                username = request.POST.get('username')
                gender = request.POST.get('gender')
                phone = request.POST.get('phone')
                # 其他字段同理

                # 更新EmployeeInfo对象
                employee.username = username
                employee.gender = gender
                employee.phone = phone
                # 其他字段同理
                employee.save()

                return JsonResponse({'message': '工作人员信息更新成功'})

            return JsonResponse({'message': 'Method not allowed'}, status=405)

        except EmployeeInfo.DoesNotExist:
            return JsonResponse({'message': '工作人员信息不存在'})


def get_employee(request, employee_id):
    try:
        employee = EmployeeInfo.objects.get(id=employee_id)

        employee_data = {
            'id': employee.id,
            'username': employee.username,
            'gender': employee.gender,
            'phone': employee.phone,
            # 其他字段同理
        }

        return JsonResponse({'employee': employee_data})

    except EmployeeInfo.DoesNotExist:
        return JsonResponse({'message': '工作人员信息不存在'})


@csrf_exempt
def delete_employee(request, employee_id):
    if request.method == 'DELETE':
        try:
            employee = EmployeeInfo.objects.get(id=employee_id)

            if request.method == 'POST':
                employee.delete()
                return JsonResponse({'message': '工作人员信息删除成功'})

            return JsonResponse({'message': 'Method not allowed'}, status=405)

        except EmployeeInfo.DoesNotExist:
            return JsonResponse({'message': '工作人员信息不存在'})

# 图片上传等功能需要使用第三方库，例如Pillow、django-storages等。具体实现会有所不同，需要根据具体需求进行调整。统计分析功能也需要根据具体需求进行编写。
