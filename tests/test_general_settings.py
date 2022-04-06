from django.test import TestCase, Client
from web.models import Membership, Subscription, Order
from django.contrib.auth.models import User


class TestGeneralSettings(TestCase):
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

    def test_user_exist(self):
        user_count = User.objects.all().count()  # int
        print('test_user_exist', end=' - ')
        print("user_count: ", user_count)
        self.assertEqual(user_count, 1)  # ==

    def test_membership_exist(self):
        membership_count = Membership.objects.all().count()  # int
        print('test_membership_exist', end=' - ')
        print("membership_count: ", membership_count)
        self.assertEqual(membership_count, 1)  # ==

    def test_subscription_exist(self):
        subscription_count = Subscription.objects.all().count()  # int
        print('test_subscription_exist', end=' - ')
        print("subscription_count: ", subscription_count)
        subscription_time = Subscription.objects.get(pk=1)
        subscription_quantity = Subscription.objects.get(pk=2)
        print("subscription_time :", subscription_time)
        print("subscription_quantity:", subscription_quantity)
        self.assertEqual(subscription_count, 2)  # ==

    def test_order_exist(self):
        subscription_count = Order.objects.all().count()  # int
        print('test_order_exist', end=' - ')
        print("order_count: ", subscription_count)
        order_time = Order.objects.get(pk=1)
        order_quantity = Order.objects.get(pk=2)
        print("order_time :", order_time.paid_until)
        print("order_quantity:", order_quantity.quantity)
        self.assertEqual(subscription_count, 2)  # ==
