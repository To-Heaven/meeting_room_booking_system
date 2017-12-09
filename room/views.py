from django.shortcuts import render, HttpResponse

import datetime
from json import dumps, loads

from room import models


def table_orders(request):
    if request.method == 'GET':
        today = datetime.datetime.today()
        orders = models.Order.objects.filter(schedule_date=today)
        rooms = models.MeetingRoom.objects.all()
        order_list = [(order, order.room) for order in orders]
        #
        temp = {
            'room_obj': {
                'period': 'order_obj'   # 当天的记录对象
            }
        }

        result_dict = {}
        for room in rooms:
            result_dict[room] = {}
            for order in orders:
                if order.room == room:
                    result_dict[room][order.period] = order
        print(result_dict)
        return render(request, 'room_table.html', {
            "today": today.strftime('%Y-%m-%d'),
            "period_list": models.Order.period_list,
            "result_dict": result_dict
        })

        # return render(request, 'room_table.html', {
        #     "rooms": rooms,
        #     "order_list": order_list,
        #     "period_list": models.Order.period_list,
        #     'today': today.strftime('%Y-%m-%d'),
        # })


def table_change(request, year=None, month=None, day=None):
    select_time = datetime.datetime(year=year, month=month, day=day)
    orders = models.Order.objects.filter(schedule_date=select_time)
    rooms = models.MeetingRoom.objects.all()
    order_list = [(order, order.room) for order in orders]
    return render(request, 'room_table.html', {
        "rooms": rooms,
        "order_list": order_list,
        "period_list": models.Order.period_list,
        'today': select_time.strftime('%Y-%m-%d'),
    })


def login(request):
    user = models.User.objects.get(username='ziawang', password='123')
    request.session['id'] = user.id
    request.session['username'] = user.username
    return HttpResponse('login successful')

def commit_choice(request):
    data = loads(request.body.decode('utf-8'))
    user_id = request.session.get('id')
    schedule_date = data['schedule_date']
    del data['schedule_date']

    order_list = []
    for room_id, periods in data.items():
        for period in periods:
            order_list.append(models.Order(
                period=period,
                room_id=room_id,
                user_id=user_id,
                schedule_date=schedule_date
            ))
    models.Order.objects.bulk_create(order_list)
    response_data = {"success": True, "message": '预订成功'}
    return HttpResponse(dumps(response_data))






def checkout(request, order_id=None):
    user_id = request.session.get('id')
    order = models.Order.objects.filter(user__id=user_id, id=order_id)
    if not order:
        data = {"success": False}
        return HttpResponse(dumps(data))
    else:
        order.delete()
        data = {"success": True}
        return HttpResponse(dumps(data))
