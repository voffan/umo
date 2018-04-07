from django.conf.urls import url,include
from django.contrib import admin
from umo import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^teacher/', include('umo.urls', namespace='teachers')),
    url(r'^student/$', views.StudentListView.as_view(), name='student_changelist'),
    url(r'^student/add/$', views.StudentCreateView.as_view(), name='student_add'),
    url(r'^student/delete/$', views.student_delete, name='student_delete'),
    url(r'^disciplines/', include('disciplines.urls', namespace='disciplines')),
    url(r'^$', include('loginsys.urls')),
]
