import json
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from event_info.models import EventInfo


# Create your views here.

# 传入参数: event_type, event_date(now), event_location,event_desc, oldperson_id
# 要在算法中调用用来插入活动到数据库中，不从前端url插入
# 传出参数: success
def insert_event(event_type, event_date, event_location, event_desc, oldperson_id):
    event = EventInfo(
        event_type=event_type,
        event_date=event_date,
        event_location=event_location,
        event_desc=event_desc,
        oldperson_id=oldperson_id
    )
    event.save()
    return True


@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        event_type = data.get('event_type')
        event_date = data.get('event_date')
        event_location = data.get('event_location')
        event_desc = data.get('event_desc')
        oldperson_id = data.get('oldperson_id')
        insert_event(event_type, event_date, event_location, event_desc, oldperson_id)
        # event = EventInfo(
        #     event_type=event_type,
        #     event_date=event_date,
        #     event_location=event_location,
        #     event_desc=event_desc,
        #     oldperson_id=oldperson_id
        # )
        # event.save()
        return JsonResponse({'message': '事件信息录入成功'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def get_all_events(request):
    if request.method == 'GET':
        events = EventInfo.objects.all()
        events_list = []
        for event in events:
            events_list.append({
                'id': event.id,
                'event_type': event.event_type,
                'event_date': event.event_date,
                'event_location': event.event_location,
                'event_desc': event.event_desc,
                'oldperson_id': event.oldperson_id
            })
        return JsonResponse({'events': events_list}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def get_event_by_oldperson_id(request, oldperson_id):
    if request.method == 'GET':
        events = EventInfo.objects.filter(oldperson_id=oldperson_id)
        events_list = []
        for event in events:
            events_list.append({
                'id': event.id,
                'event_type': event.event_type,
                'event_date': event.event_date,
                'event_location': event.event_location,
                'event_desc': event.event_desc,
                'oldperson_id': event.oldperson_id
            })
        return JsonResponse({'events': events_list}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def get_event_by_event_type(request, event_type):
    if request.method == 'GET':
        events = EventInfo.objects.filter(event_type=event_type)
        events_list = []
        for event in events:
            events_list.append({
                'id': event.id,
                'event_type': event.event_type,
                'event_date': event.event_date,
                'event_location': event.event_location,
                'event_desc': event.event_desc,
                'oldperson_id': event.oldperson_id
            })
        return JsonResponse({'events': events_list}, status=200)


@csrf_exempt
def get_event_by_event_type_and_oldperson_id(request, event_type, oldperson_id):
    if request.method == 'GET':
        events = EventInfo.objects.filter(event_type=event_type, oldperson_id=oldperson_id)
        events_list = []
        for event in events:
            events_list.append({
                'id': event.id,
                'event_type': event.event_type,
                'event_date': event.event_date,
                'event_location': event.event_location,
                'event_desc': event.event_desc,
                'oldperson_id': event.oldperson_id
            })
        return JsonResponse({'events': events_list}, status=200)


@csrf_exempt
def get_event_by_event_date(request, event_date):
    if request.method == 'GET':
        events = EventInfo.objects.filter(event_date=event_date)
        events_list = []
        for event in events:
            events_list.append({
                'id': event.id,
                'event_type': event.event_type,
                'event_date': event.event_date,
                'event_location': event.event_location,
                'event_desc': event.event_desc,
                'oldperson_id': event.oldperson_id
            })
        return JsonResponse({'events': events_list}, status=200)


@csrf_exempt
def get_event(request, event_id):
    if request.method == 'GET':
        try:
            event = EventInfo.objects.get(id=event_id)
            return JsonResponse({
                'id': event.id,
                'event_type': event.event_type,
                'event_date': event.event_date,
                'event_location': event.event_location,
                'event_desc': event.event_desc,
                'oldperson_id': event.oldperson_id
            }, status=200)
        except EventInfo.DoesNotExist:
            return JsonResponse({'message': '事件信息不存在'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def update_event(request, event_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            event = EventInfo.objects.get(id=event_id)
            if data.get('event_type'):
                event.event_type = data.get('event_type')
            if data.get('event_date'):
                event.event_date = data.get('event_date')
            if data.get('event_location'):
                event.event_location = data.get('event_location')
            if data.get('event_desc'):
                event.event_desc = data.get('event_desc')
            if data.get('oldperson_id'):
                event.oldperson_id = data.get('oldperson_id')
            event.save()
            return JsonResponse({'message': '事件信息更新成功'})
        except EventInfo.DoesNotExist:
            return JsonResponse({'message': '事件信息不存在'})
    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_event(request, event_id):
    if request.method == 'DELETE':
        try:
            event = EventInfo.objects.get(id=event_id)
            event.delete()
            return JsonResponse({'message': '事件信息删除成功'})
        except EventInfo.DoesNotExist:
            return JsonResponse({'message': '事件信息不存在'})
    return JsonResponse({'message': 'Method not allowed'}, status=405)


def get_number(request):
    # （开心、摔倒、义工交互、陌生人闯入等等）按日期分类统计次数
    if request.method == 'GET':
        happy_events = EventInfo.objects.filter(event_type='老人笑了')
        fall_events = EventInfo.objects.filter(event_type='摔倒')
        volunteer_events = EventInfo.objects.filter(event_type='义工交互')
        stranger_events = EventInfo.objects.filter(event_type='陌生人')
        # 统计最近三天的数据，分为第一天、第二天、第三天，分为三天三个字典，每一项下面都有每个事件的次数
        current_date = datetime.today().date()
        previous_day = current_date - timedelta(days=1)
        two_days_ago = current_date - timedelta(days=2)
        dates = {
            current_date.strftime('%Y-%m-%d'): 0,
            previous_day.strftime('%Y-%m-%d'): 0,
            two_days_ago.strftime('%Y-%m-%d'): 0
        }

        happy_events_list = {
            current_date.strftime('%Y-%m-%d'): 0,
            previous_day.strftime('%Y-%m-%d'): 0,
            two_days_ago.strftime('%Y-%m-%d'): 0
        }
        fall_events_list = {
            current_date.strftime('%Y-%m-%d'): 0,
            previous_day.strftime('%Y-%m-%d'): 0,
            two_days_ago.strftime('%Y-%m-%d'): 0
        }
        volunteer_events_list = {
            current_date.strftime('%Y-%m-%d'): 0,
            previous_day.strftime('%Y-%m-%d'): 0,
            two_days_ago.strftime('%Y-%m-%d'): 0
        }
        stranger_events_list = {
            current_date.strftime('%Y-%m-%d'): 0,
            previous_day.strftime('%Y-%m-%d'): 0,
            two_days_ago.strftime('%Y-%m-%d'): 0
        }

        for event in happy_events:
            if event.event_date.date() == current_date:
                happy_events_list[current_date.strftime('%Y-%m-%d')] += 1
            elif event.event_date.date() == previous_day:
                happy_events_list[previous_day.strftime('%Y-%m-%d')] += 1
            elif event.event_date.date() == two_days_ago:
                happy_events_list[two_days_ago.strftime('%Y-%m-%d')] += 1
        for event in fall_events:
            if event.event_date.date() == current_date:
                fall_events_list[current_date.strftime('%Y-%m-%d')] += 1
            elif event.event_date.date() == previous_day:
                fall_events_list[previous_day.strftime('%Y-%m-%d')] += 1
            elif event.event_date.date() == two_days_ago:
                fall_events_list[two_days_ago.strftime('%Y-%m-%d')] += 1
        for event in volunteer_events:
            if event.event_date.date() == current_date:
                volunteer_events_list[current_date.strftime('%Y-%m-%d')] += 1
            elif event.event_date.date() == previous_day:
                volunteer_events_list[previous_day.strftime('%Y-%m-%d')] += 1
            elif event.event_date.date() == two_days_ago:
                volunteer_events_list[two_days_ago.strftime('%Y-%m-%d')] += 1
        for event in stranger_events:
            if event.event_date.date() == current_date:
                stranger_events_list[current_date.strftime('%Y-%m-%d')] += 1
            elif event.event_date.date() == previous_day:
                stranger_events_list[previous_day.strftime('%Y-%m-%d')] += 1
            elif event.event_date.date() == two_days_ago:
                stranger_events_list[two_days_ago.strftime('%Y-%m-%d')] += 1
        print(happy_events_list)
        dates[current_date.strftime('%Y-%m-%d')] = {
            '老人笑了': happy_events_list[current_date.strftime('%Y-%m-%d')],
            '摔倒': fall_events_list[current_date.strftime('%Y-%m-%d')],
            '义工交互': volunteer_events_list[current_date.strftime('%Y-%m-%d')],
            '陌生人': stranger_events_list[current_date.strftime('%Y-%m-%d')]
        }
        dates[previous_day.strftime('%Y-%m-%d')] = {
            '老人笑了': happy_events_list[previous_day.strftime('%Y-%m-%d')],
            '摔倒': fall_events_list[previous_day.strftime('%Y-%m-%d')],
            '义工交互': volunteer_events_list[previous_day.strftime('%Y-%m-%d')],
            '陌生人': stranger_events_list[previous_day.strftime('%Y-%m-%d')]
        }
        dates[two_days_ago.strftime('%Y-%m-%d')] = {
            '老人笑了': happy_events_list[two_days_ago.strftime('%Y-%m-%d')],
            '摔倒': fall_events_list[two_days_ago.strftime('%Y-%m-%d')],
            '义工交互': volunteer_events_list[two_days_ago.strftime('%Y-%m-%d')],
            '陌生人': stranger_events_list[two_days_ago.strftime('%Y-%m-%d')]
        }
        return JsonResponse(dates, status=200)


def get_newest_event(request):
    # 获取最新的事件
    if request.method == 'GET':
        try:
            newest_event = EventInfo.objects.latest('event_date')
            newest_event_dict = {
                'event_type': newest_event.event_type,
                'event_date': newest_event.event_date.strftime('%Y-%m-%d %H:%M:%S'),
                'event_location': newest_event.event_location,
                'event_description': newest_event.event_desc,
                'old_person_id': newest_event.oldperson_id,
            }
            return JsonResponse(newest_event_dict, status=200)
        except EventInfo.DoesNotExist:
            return JsonResponse({'message': '事件信息不存在'}, status=404)
    return JsonResponse({'message': 'Method not allowed'}, status=405)
