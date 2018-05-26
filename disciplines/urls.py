from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from disciplines import views

urlpatterns = [
    url(r'^add/$', staff_member_required(views.DisciplineCreate.as_view()), name='disciplines_add'),
    url(r'(?P<pk>[0-9]+)/update/$', staff_member_required(views.DisciplineUpdate.as_view()), name='update'),
    url(r'^delete/$', staff_member_required(views.discipline_delete), name='delete'),
    url(r'(?P<pk>[0-9]+)/$', views.discipline_detail, name='detail'),
    url(r'^details_list/$', staff_member_required(views.DisciplineDetailsList.as_view()), name='details_list'),
    url(r'^add_details/$', staff_member_required(views.DetailsCreate.as_view()), name='details_add'),
    url(r'(?P<pk>[0-9]+)/update_details/$', staff_member_required(views.DisciplineDetailsUpdate.as_view()), name='update_details'),
    url(r'^export/$', staff_member_required(views.export_to_excel), name='export'),
    url(r'^excel/$', staff_member_required(views.excel), name='excel'),
    url(r'(?P<pk>[0-9]+)/disciplines_list/$', views.list_disc, name='disciplines'),
    url(r'^all_disciplines/$', staff_member_required(views.DisciplineList.as_view()), name='disciplines_list'),
    url(r'^dataforekran/$', staff_member_required(views.get_data_for_ekran), name='dataforekran'),
    url(r'^subjects/$', staff_member_required(views.subjects), name='subjects'),
    url(r'^$', views.list_teachers, name='disc_teachers'),
]
