from django.conf.urls import url,include
from django.contrib import admin
from umo import views
from django.contrib.auth.decorators import login_required

admin.autodiscover()
urlpatterns = [
    url(r'^$', login_required(views.list_teachers), name='list_teachers'),
    url(r'^create_teacher/$',  login_required(views.create_teacher), name='create_teacher'),
    # url(r'^(?P<pk>\d+)/update/$', views.TeacherUpdate.as_view(), name='teacher_update'),
    # url(r'^(?P<pk>\d+)/delete/$', views.TeacherDelete.as_view(), name='teacher_delete'),
]
