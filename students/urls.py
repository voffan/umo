from django.urls import path

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

from students import views

urlpatterns = [
    url(r'^$', views.StudentListView.as_view(), name='student_changelist'),
    url(r'^list$', views.StudentsList.as_view(), name='student_list'),
    url(r'^add$', views.StudentCreateView.as_view(), name='student_add'),
    url(r'^delete$', views.student_delete, name='student_delete'),
    url(r'^(?P<pk>[0-9]+)$', views.StudentUpdateView.as_view(), name='student_edit'),
    url(r'^group_points$', views.group_points, name='group_points'),
    url(r'^subjects$', views.subjects, name='subjects'),
    url(r'^group_list/(?P<pk>[0-9]+)/$', views.group_list, name='group_list'),
    url(r'^access_student/(?P<pk>[0-9]+)/$', views.give_access_student, name='give_access_student'),
    path('profile', views.student_profile, name='student_profile'),
    url(r'^group_access/(?P<pk>[0-9]+)/$', views.group_access_excel, name='group_access_excel')
]
