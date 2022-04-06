from django.test import TestCase, Client
from web.models import Membership, Subscription, Order
from django.contrib.auth.models import User
from datetime import timedelta, date



class TestOrderModel(TestCase):
    # setUp инструкция, выполняемая перед каждым тестом.
    def setUp(self):
        # Тестовый клиент – это класс Python, который умеет эмулировать запросы браузера.
        client = Client()
        # создаем экземпляр пользователя
        user = User.objects.create_user(username='jalll', email='jacob@mail.qw', password='top_secret')
        # Метод force_login() нужен, чтобы эмулировать авторизацию пользователя на сайте.
        # Используйте этот метод вместо login(), если необходимо авторизировать пользователя в тестах
        # и при этом не важен способ авторизации.
        client.force_login(user)
        # создаем экземпляр Membership
        Membership.objects.create(
            user_id=user.id,
            name='description',
            email='jacob@mail.qw'
        )
        membership_1 = Membership.objects.get(pk=1)
        # создаем экземпляр Subscription
        Subscription.objects.create(
            title='1m',
            description='1 month',
            is_limited=True,
            price=25
        )
        Subscription.objects.create(
            title='4t',
            description='4 times',
            is_limited=False,
            price=25
        )
        subscription_time = Subscription.objects.get(pk=1)
        subscription_quantity = Subscription.objects.get(pk=2)

        Order.objects.create(
            membership_id=membership_1.pk,
            subscription_id=subscription_time.pk,
            date_added="2022-06-04",
            activation=True,
            date_activation="2022-06-04",
            paid_until="2022-06-05",
         )
        Order.objects.create(
            membership_id=membership_1.pk,
            subscription_id=subscription_quantity.pk,
            date_added="2022-06-04",
            activation=True,
            date_activation="2022-06-04",
            quantity=4
         )
        order_time = Order.objects.get(pk=1)
        order_quantity = Order.objects.get(pk=2)

    def test_paid_limit_true(self):
        # экземпляр Order, оплаченный на период времени.
        order_time = Order.objects.get(pk=1)
        # устанавливаем текущую дату
        current_date = date(2022, 4, 10)
        _30_days = timedelta(days=30)
        # устанавливаем значение поля paid_until + 30 дней к текущей дате.
        order_time.paid_until = current_date + _30_days
        # ожидаем, что срок действия абонемента = True.
        print("paid_until: ", order_time.paid_until)
        self.assertTrue(order_time.paid_limit)

    def test_paid_limit_false(self):
        # экземпляр Order, оплаченный на период времени.
        order_time = Order.objects.get(pk=1)
        # устанавливаем текущую дату
        current_date = date(2022, 4, 10)
        _30_days = timedelta(days=30)
        # устанавливаем значение поля paid_until - 30 дней к текущей дате.
        order_time.paid_until = current_date - _30_days
        # ожидаем, что срок действия абонемента = False.
        print("paid_until2: ", order_time.paid_until)
        self.assertFalse(order_time.paid_limit)

    def test_paid_quantity_true(self):
        # экземпляр Order, оплаченный на количество раз.
        order_quantity = Order.objects.get(pk=2)
        # устанавливаем значение поля quantity (количество раз) 4 посещения.
        order_quantity.quantity = 4
        # ожидаем, что количество посещений больше нуля, paid_quantity = True.
        print("paid_quantity_true: ", order_quantity.paid_quantity)
        self.assertTrue(order_quantity.paid_quantity)

    def test_paid_quantity_false(self):
        # экземпляр Order, оплаченный на количество раз.
        order_quantity = Order.objects.get(pk=2)
        # устанавливаем значение поля quantity (количество раз) 0 посещений (посещения закончились).
        order_quantity.quantity = 0
        # ожидаем, что количество посещений равно нулю, paid_quantity = False.
        print("paid_quantity_false: ", order_quantity.paid_quantity)
        self.assertFalse(order_quantity.paid_quantity)


