"""umo_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from umo import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^teacher/', include('umo.urls')),
    url(r'^student/', views.list_students, name='list_students'),
    #url(r'^create/$', views.StudentCreate.as_view(), name='student_create'),
    #url(r'^(?P<pk>\d+)/update/$', views.StudentUpdate.as_view(), name='student_update'),
    #url(r'^(?P<pk>\d+)/delete/$', views.StudentDelete.as_view(), name='student_delete')
]
