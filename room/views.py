from django.shortcuts import render, HttpResponse

import datetime
from json import dumps, loads

from room import models
from room.forms import LoginForm


def table_orders(request):
    if request.method == 'GET':
        today = datetime.datetime.today()
        orders = models.Order.objects.filter(schedule_date=today)
        rooms = models.MeetingRoom.objects.all()

        result_dict = {}
        for room in rooms:
            result_dict[room] = {}
            for order in orders:
                if order.room == room:
                    result_dict[room][order.period] = order
        return render(request, 'room_table.html', {
            "today": today.strftime('%Y-%m-%d'),
            "period_list": models.Order.period_list,
            "result_dict": result_dict
        })


def table_change(request, year=None, month=None, day=None):
    select_time = datetime.datetime(year=year, month=month, day=day)
    orders = models.Order.objects.filter(schedule_date=select_time)
    rooms = models.MeetingRoom.objects.all()

    result_dict = {}
    for room in rooms:
        result_dict[room] = {}
        for order in orders:
            if order.room == room:
                result_dict[room][order.period] = order
    return render(request, 'room_table.html', {
        "today": select_time.strftime('%Y-%m-%d'),
        "period_list": models.Order.period_list,
        "result_dict": result_dict
    })


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            auto_login = form.cleaned_data.pop('auto_login')
            user = models.User.objects.filter(**form.cleaned_data)
            if user:
                request.session['username'] = user[0].username
                request.session['id'] = user[0].id
                if auto_login:
                    request.session.set_expiry(60*60*24*30)
                data = {
                    "success": True,
                    "location_href": '/room/'
                }
                return HttpResponse(dumps(data))
            else:
                form.add_error(field='password', error='用户名或密码错误')
                data = {
                     "success": False,
                     "form_errors": form.errors
                }
                return HttpResponse(dumps(data))
        else:
            data = {
                "success": False,
                "form_errors": form.errors
            }
            return HttpResponse(dumps(data))


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
