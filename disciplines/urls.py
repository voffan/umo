from django.conf.urls import url
from disciplines import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^list/$', login_required(views.list)),
    url(r'^add/$', login_required(views.add_discipline)),
    url(r'^$', login_required(views.list))
]
