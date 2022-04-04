from django.shortcuts import render
from web.models import *
import datetime


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
    Order.objects.create(
        membership=membership,
        subscription=subscription,
        paid_until=datetime.date.today() + datetime.timedelta(30),
        quantity=4
    )
    context = {
        "subscription": subscription,
        "all done": 'all done'
    }
    return render(request, 'add_membership.html', context)


