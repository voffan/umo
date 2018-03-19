from django.conf.urls import url,include
from django.contrib import admin
from umo import views

urlpatterns = [
    url(r'', views.list_teachers, name='list_teachers'),
    url(r'^create/$', views.TeacherCreate.as_view(), name='teacher_create'),
    url(r'^(?P<pk>\d+)/update/$', views.TeacherUpdate.as_view(), name='teacher_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.TeacherDelete.as_view(), name='teacher_delete'),
]
