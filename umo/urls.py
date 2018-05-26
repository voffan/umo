from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

from umo import views

admin.autodiscover()
urlpatterns = [
    url(r'^list/$', staff_member_required(views.list_teachers), name='list_teachers'),
    url(r'^create_teacher/$',  staff_member_required(views.create_teacher), name='create_teacher'),
    url(r'^delete_teacher/$', staff_member_required(views.delete_teacher), name='delete_teacher'),
    url(r'(?P<pk>[0-9]+)/edit_teacher/$', staff_member_required(views.TeacherUpdate.as_view()), name='edit_teacher'),
]
