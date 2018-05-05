from django.conf.urls import url
from django.contrib import admin
from nomenclature import views

admin.autodiscover()
urlpatterns = [
    url(r'^list/$', views.rup_list, name='rup_list' ),
    url(r'^upload_file/$', views.upload_file, name='upload_file')
]