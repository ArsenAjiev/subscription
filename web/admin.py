from django.contrib import admin

from web.models import *


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "email",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "is_limited", "price")


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("membership", "subscription", "quantity", "is_limited", "date_added", "activation",  "date_activation",
                    "paid_until", "expired", "paid_limit", "paid_quantity", "diff_date")

