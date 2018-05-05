from django.conf.urls import url

from disciplines import views

urlpatterns = [
    url(r'^add/$', views.DisciplineCreate.as_view(), name='disciplines_add'),
    url(r'(?P<pk>[0-9]+)/update/$', views.DisciplineUpdate.as_view(), name='update'),
    url(r'^delete/$', views.discipline_delete, name='delete'),
    url(r'^export/$', views.export_to_excel, name='export'),
    url(r'^excel/$', views.excel, name='excel'),
    url(r'(?P<pk>[0-9]+)/$', views.discipline_detail, name='detail'),
    url(r'^add_details/$', views.DetailsCreate.as_view(), name='details_add'),
    url(r'^$', views.DisciplineList.as_view(), name='disciplines_list'),
]
