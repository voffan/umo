from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include
from hours import views

admin.autodiscover()

api = ([
    url('get_courselist$', views.get_courselist, name='get_courselist'),
    url('get_contingentlist$', views.get_contingentlist, name='get_contingentlist'),
    url('get_employeelist$', views.get_employeelist, name='get_employeelist'),
    url('get_supervision_hours', views.get_supervision_hours, name='get_supervision_hours'),
    url('save_courselist', views.save_courselist, name='save_courselist'),
    url('save_contingentlist', views.save_contingent, name='save_contingent'),
    url('save_employeelist', views.save_employeelist, name='save_employeelist'),
    url('save_supervision_hours', views.save_supervision_hours, name='save_supervision_hours'),
], 'api')

urlpatterns = [
    path(r'courselist/', views.CourseList.as_view(), name='course_list'),
    path(r'courseupload/', views.upload_course, name='course_upload'),
    path(r'contingentlist/', views.ContingentList.as_view(), name='contingent_list'),
    path(r'supervisionhours', views.SupervisionHoursList.as_view(), name='supervision_hours'),
    path(r'contingentupload', views.upload_contingent, name='contingent_upload'),
    path(r'contingentdelete/<int:pk>', views.ContingentDelete.as_view(), name='delete_contingent'),
    path(r'editcontingent/<int:pk>/', views.ContingentUpdate.as_view(), name='edit_contingent'),
    path(r'employeelist/', views.EmployeeList.as_view(), name='employee_list'),
    path(r'createemployee/', views.EmployeeCreate.as_view(), name='create_employee'),
    path(r'editemployee/<int:pk>', views.EmployeeUpdate.as_view(), name='edit_employee'),
    path(r'supervisionedit/<int:pk>', views.SupervisionUpdate.as_view(), name='edit_supervision'),
    url(r'^export_kup/(?P<pk>[0-9]+)/$', views.export_kup, name='export_kup'),
    url(r'^api/', include(api, namespace='api'))
]
