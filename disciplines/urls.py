from django.conf.urls import url
from disciplines import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^list/$', views.list),
    url(r'^add/$', views.add_discipline),
    url(r'^$', views.list)
]
