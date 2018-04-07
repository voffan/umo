from django.conf.urls import url,include
from django.contrib import admin
from umo import views

admin.autodiscover()
urlpatterns = [
    url(r'^$', views.list_teachers, name='list_teachers'),
    url(r'^create_teacher/$',  views.create_teacher, name='create_teacher'),
    url(r'^delete_teacher/$', views.delete_teacher, name='delete_teacher')
    #url(r'^(?P<pk>\d+)/update/$', views.TeacherUpdate.as_view(), name='teacher_update'),
    #url(r'^(?P<pk>\d+)/delete/$', views.TeacherDelete.as_view(), name='teacher_delete'),
]
