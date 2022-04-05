"""subscription URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web.views import index, profile, store, add_membership, activation, deactivation, delete_membership, check_visit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('profile/', profile, name='profile'),
    path('store/', store, name='store'),
    path('add_membership/<item_pk>/', add_membership, name='add_membership'),
    path('activation/<item_pk>/', activation, name='activation'),
    path('deactivation/<item_pk>/', deactivation, name='deactivation'),
    path('delete_membership/<item_pk>/', delete_membership, name='delete_membership'),
    path('check_visit/<item_pk>/', check_visit, name='check_visit'),
]
