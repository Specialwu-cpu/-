import json

import jwt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .models import SysUser


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        # 获取前端传递的参数
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        # 在数据库中查找用户
        try:
            user = SysUser.objects.get(UserName=username)
        except SysUser.DoesNotExist:
            return JsonResponse({'message': '账户不存在'})

        # 比对密码
        if user.Password == password:
            # 密码匹配
            payload = {'user_id': user.id, 'username': user.UserName}
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            print(token)  # 打印 Token 值
            return JsonResponse({'message': '登陆成功', 'data': {'token': token}})
        else:
            # 密码不匹配
            return JsonResponse({'message': '密码错误'})

    # 处理其他HTTP方法
    return JsonResponse({'message': 'Method not allowed'}, status=405)
    # return JsonResponse({'username': username})


def get_all_users(request):
    users = SysUser.objects.all()
    user_list = [{'id': user.id, 'username': user.UserName} for user in users]
    return JsonResponse({'users': user_list})


@csrf_exempt
def change_password(request):
    if request.method == 'POST':

        # 从请求中获取 JWT token
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]

        try:
            # 解码 JWT token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']

            # 根据 user_id 获取用户对象
            user = SysUser.objects.get(id=user_id)
        except Exception as e:
            return JsonResponse({'message': 'Token invalid'}, status=401)

        # 根据 user_id 获取用户对象
        data = json.loads(request.body.decode('utf-8'))
        # 获取旧密码、新密码和确认密码
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # 检查旧密码是否匹配
        if user.Password != old_password:
            return JsonResponse({'message': '旧密码错误'})

        # 检查新密码和确认密码是否一致
        if new_password != confirm_password:
            return JsonResponse({'message': '新密码和确认密码不一致'})

        # 更新密码
        user.Password = new_password
        user.save()

        return JsonResponse({'message': '密码修改成功'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)
