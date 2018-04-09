from django.conf.urls import url
from disciplines import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', views.DisciplineList.as_view(), name='disciplines_list'),
    url(r'add/$', views.DisciplineCreate.as_view(), name='disciplines_add'),
    url(r'(?P<pk>[0-9]+)/update/$', views.DisciplineUpdate.as_view(), name='update'),
    url(r'(?P<pk>[0-9]+)/delete/$', views.DisciplineDelete.as_view(), name='delete'),
    url(r'(?P<pk>[0-9]+)/$', views.discipline_detail, name='detail'),
    url(r'(?P<pk>[0-9]+)/details/$', views.DetailsList.as_view(), name='details'),
]
