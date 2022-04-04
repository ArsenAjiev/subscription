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
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    # поле активацию абонемента
    is_active = models.BooleanField(default=False)
    # дата активации абонемента
    date_activation = models.DateField(blank=True, null=True)
    # поле для абонементов со сроком действия paid_until - дата до которой оплачен абонемент
    paid_until = models.DateField(null=True, blank=True)
    # поле для всех типов абонементов
    # поле будет менять значение при истечении срока действия абонемента или количества посещений
    # expired = models.BooleanField(default=False)
    # поле для абонементов с количеством посещений - quantity=8 - (8 посещений)
    quantity = models.IntegerField(default=0, blank=True, null=True)

    @property
    # ссылается на дату покупки, возвращает False когда срок действия закончился
    def paid_limit(self, current_date=datetime.date.today()):
        if self.paid_until is None:
            return False
        if not self.is_limited:
            return False
        if self.is_limited:
            return current_date < self.paid_until

    @property
    # ссылается на поле quantity, возвращает False когда количество посещений == 0
    def paid_quantity(self):
        if self.is_limited:
            return False
        else:
            return self.quantity > 0

    @property
    # выводит информацию об истечении срока действия абонемента
    def expired(self):
        if self.paid_limit == 0 and self.paid_quantity == 0:
            return True
        else:
            return False

    @property
    # выводит информацию об истечении срока действия абонемента
    def is_limited(self):
        return self.subscription.is_limited

    def __str__(self):
        return f" № {self.pk}"
