from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

from umo import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^teacher/', include(('umo.urls', 'umo'), namespace='teachers')),
    url(r'^disciplines/', include(('disciplines.urls', 'disciplines'), namespace='disciplines')),
    url(r'^nomenclature/', include(('nomenclature.urls', 'nomenclature'), namespace='nomenclatures')),
    url(r'^student/', include(('students.urls', 'students'), namespace='students')),
    url(r'^brspoints/(?P<pk>[0-9]+)/$', views.BRSPointsListView.as_view(), name='brs_studentlist'),
    url(r'^select2/', include('django_select2.urls')),
]
