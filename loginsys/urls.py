from django.conf.urls import url
from loginsys import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^logout/$', login_required(views.logout)),
    url(r'^register/$', views.register),
    url(r'^register_success/$', login_required(views.register_success)),
    url(r'^$', views.login),
]
