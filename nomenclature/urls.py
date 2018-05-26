from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

from nomenclature import views

admin.autodiscover()
urlpatterns = [
    url(r'^success/$', staff_member_required(views.rup_list), name='success' ),
    url(r'^upload_file/$', staff_member_required(views.upload_file), name='upload_file'),
    url(r'^select_semestr/$', staff_member_required(views.select_semestr), name='select_semestr'),
    url(r'^set_teachers/$', staff_member_required(views.vuborka), name='set_teachers'),
    url(r'^set_teachers/done/$', staff_member_required(views.subjects_save), name='set_teachers_done')
]