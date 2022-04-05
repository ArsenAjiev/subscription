import calendar
import datetime

from django.shortcuts import render, redirect

from web.models import *


# функция, которая добавляет месяц к указанной дате.
def add_months(main_date, months):
    month = main_date.month - 1 + months
    year = main_date.year + month // 12
    month = month % 12 + 1
    day = min(main_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


# пример работы
x = datetime.datetime.now()
print(datetime.datetime.now())
# 2022-04-05 09:15:20.929525

# плюс 3 месяца
print(add_months(x, 3))
# 2022-07-05

# минус 2 месяца
print(add_months(x, -2))
# 2022-02-05


def index(request):
    print(request.user.membership)
    item = Order.objects.all()
    context = {
        'item': item
    }
    return render(request, 'index.html', context)


def profile(request):
    membership = request.user.membership
    my_orders = Order.objects.filter(membership=membership)
    context = {
        'my_orders': my_orders
    }
    return render(request, 'profile.html', context)


def store(request):
    subscription = Subscription.objects.all()
    context = {
        "subscription": subscription
    }
    return render(request, 'store.html', context)


def add_membership(request, item_pk):
    membership = request.user.membership
    subscription = Subscription.objects.get(pk=item_pk)
    # если абонемент не лимитируемый, то кол-во посещений это первое число CHOIOSE "4t", преобразованное к int.
    if not subscription.is_limited:
        quantity = int(subscription.title[0])
    else:
        quantity = 0
    print(quantity)

    Order.objects.create(
        membership=membership,
        subscription=subscription,
        paid_until=None,
        quantity=quantity
    )
    return redirect('profile')


def activation(request, item_pk):
    # membership = request.user.membership
    order = Order.objects.get(pk=item_pk)
    date_now = datetime.date.today()
    # если абонемент лимитируемый, то к дате активации прибавляем количество месяцев -
    # это первое число CHOIOSE "3m", преобразованное к int.
    order.is_active = True
    order.date_activation = datetime.date.today()
    if order.is_limited:
        count_month = int(order.subscription.title[0])
        order.paid_until = add_months(date_now, count_month)
    order.save()
    print(order)
    return redirect('profile')


def deactivation(request, item_pk):
    # membership = request.user.membership
    order = Order.objects.get(pk=item_pk)
    print(order)
    order.is_active = False
    order.date_activation = None
    order.paid_until = None
    order.save()
    return redirect('profile')


def delete_membership(request, item_pk):
    # membership = request.user.membership
    order = Order.objects.get(pk=item_pk)
    print(order)
    order.delete()
    return redirect('profile')


def check_visit(request, item_pk):
    # membership = request.user.membership
    order = Order.objects.get(pk=item_pk)
    print(order)
    order.quantity = (order.quantity - 1)
    order.save()

    return redirect('profile')