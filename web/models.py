import datetime
from django.db import models
from django.contrib.auth.models import User


class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    CHOICES = (
        ("1m", 'Subscription for 1 month'),
        ("2m", 'Subscription for 2 month'),
        ("3m", 'Subscription for 3 month'),
        ("4t", 'Subscription for 4 times'),
        ("8t", 'Subscription for 8 times'),
        ("12t", 'Subscription for 12 times'),
    )
    title = models.CharField(max_length=100, choices=CHOICES)
    description = models.CharField(max_length=255)
    # поле выбора типа абонементов: is_limited=True - для абонементов со сроком действия
    # поле выбора типа абонементов: is_limited=False - для абонементов с количеством посещений.
    is_limited = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title


class Order(models.Model):
    # зарегистрированный пользователь
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    # тип абонемента
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    # дата покупки абонемента (в момент покупки абонемент не активен)
    date_added = models.DateTimeField(auto_now_add=True)
    # поле активации абонемента, отмена активации невозможна (заранее оговоренное условие)!
    # следующее состояние абонемента после активации - это использование (expired)
    activation = models.BooleanField(default=False)
    # дата активации абонемента
    date_activation = models.DateField(blank=True, null=True)
    # поле для абонементов со сроком действия paid_until - дата до которой оплачен абонемент
    # рассчитывается автоматически при активации в зависимости от оплаченного периода
    # функция - def activation(request, item_pk):
    # строка в функции -  order.paid_until = add_months(date_now, count_month)
    paid_until = models.DateField(null=True, blank=True)
    # поле для абонементов с количеством посещений - например quantity=8 - (8 посещений)
    quantity = models.IntegerField(default=0, blank=True, null=True)

    # paid_limit - сведения об оплаченном периоде за пользование абонементом, учитывает поле paid_until.
    # Возвращает:
    # True - когда абонемент на определенный период времени оплачен,
    # False - когда:
    # - срок оплаченного периода закончен
    # - поле paid_until пустое
    # - поле is_limited != False. (is_limited=False - для абонементов с количеством посещений)
    # При значении False абонемент считается использованным.
    @property
    def paid_limit(self, current_date=datetime.date.today()):
        if self.paid_until is None:
            return False
        if not self.is_limited:
            return False
        if self.is_limited:
            return current_date < self.paid_until

    # paid_quantity - сведения об оплаченных количествах посещений учитывает поле quantity.
    # Возвращает:
    # True - когда оставшееся количество посещений больше нуля,
    # False - когда:
    # - количество посещений == 0
    # - поле is_limited = True. (is_limited=True - для абонементов со сроком действия)
    # При значении False абонемент считается использованным.
    @property
    def paid_quantity(self):
        if self.is_limited:
            return False
        else:
            return self.quantity > 0

    # Поле expired - сведения об использовании абонемента.
    # Возвращает:
    # True - когда абонемент использован,
    # False - когда абонемент не использован:
    @property
    def expired(self):
        if self.paid_limit == 0 and self.paid_quantity == 0:
            return True
        else:
            return False

    # Поле is_limited -  дублирует информацию из модели subscription поля is_limited.
    # поле is_limited=True - для абонементов со сроком действия
    # поле is_limited=False - для абонементов с количеством посещений.
    @property
    def is_limited(self):
        return self.subscription.is_limited

    # Поле diff_date - рассчитывает количество оставшихся дней между paid_until и сегодняшней датой.
    @property
    def diff_date(self):
        if self.is_limited and self.activation and self.paid_limit:
            return self.paid_until - datetime.date.today()

    def __str__(self):
        return f" id {self.pk}"
