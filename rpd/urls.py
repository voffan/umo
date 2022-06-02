from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from disciplines import views

from rpd import views
from .views import *

admin.autodiscover()
urlpatterns = [
    path('rpd/<int:rpddiscipline_id>', views.rpd_create, name='rpd'),
    path('list/', views.RPDList.as_view(), name='rpd_list')
]
