from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

from umo import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^teacher/', include('umo.urls', namespace='teachers')),
    url(r'^student/$', views.StudentListView.as_view(), name='student_changelist'),
    url(r'^student/add/$', views.StudentCreateView.as_view(), name='student_add'),
    url(r'^student/delete/$', views.student_delete, name = 'student_delete'),
    url(r'^student/(?P<pk>[0-9]+)/$', views.StudentUpdateView.as_view(), name = 'student_edit'),
    url(r'^disciplines/', include('disciplines.urls', namespace='disciplines')),
    url(r'^nomenclature/', include('nomenclature.urls', namespace='nomenclatures')),
    url(r'^brspoints/(?P<pk>[0-9]+)/$', views.BRSPointsListView.as_view(), name='brs_studentlist'),
]
