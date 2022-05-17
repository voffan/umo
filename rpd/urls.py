from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

from rpd import views

admin.autodiscover()
urlpatterns = [
    url(r'^rpd/$', views.RPD.as_view(), name='rpd'),
]