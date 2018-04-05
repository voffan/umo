from django.conf.urls import url
from loginsys import views

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^register/$', views.register),
    url(r'^register_success/$', views.register_success),
]
