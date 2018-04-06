from django.conf.urls import url,include
from django.contrib import admin
from umo import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^teacher/', include('umo.urls', namespace="teachers")),
    url(r'^student/$', login_required(views.StudentListView.as_view()), name='student_changelist'),
    url(r'^student/add/$', login_required(views.StudentCreateView.as_view()), name='student_add'),
    url(r'^student/delete/$', login_required(views.student_delete), name = 'student_delete'),
    url(r'^disciplines/', include('disciplines.urls')),
    url(r'^$', include('loginsys.urls')),
]
