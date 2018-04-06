from django.conf.urls import url
from disciplines import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^list/$', views.list, name='disciplines_list'),
    url(r'^add/$', views.add_discipline, name='disciplines_add'),
    url(r'^$', views.list)
]
