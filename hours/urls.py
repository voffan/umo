from django.urls import path
from django.contrib import admin

from hours import views

admin.autodiscover()
urlpatterns = [
    path('courselist/', views.CourseList.as_view(), name='course_list'),
]