from django.conf.urls import url
from django.contrib import admin
from nomenclature import views

admin.autodiscover()
urlpatterns = [
    url(r'^list/$', views.rup_list, name='rup_list' ),
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^select_semestr/$', views.select_semestr, name='select_semestr'),
    url(r'^setteachers/$', views.vuborka, name='setteachers')
]