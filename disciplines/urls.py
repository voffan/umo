from django.conf.urls import url
from disciplines import views

urlpatterns = [
    url(r'^list/$', views.list),
    url(r'^add/$', views.add_discipline),
]
