from django.urls import path
from django.contrib import admin

from umo import views

admin.autodiscover()
urlpatterns = [
    path('list/', views.TeacherList.as_view(), name='list_teachers'),
    path('create/',  views.TeacherCreate.as_view(), name='create_teacher'),
    path('delete/<int:pk>/', views.TeacherDelete.as_view(), name='delete_teacher'),
    path('edit/<int:pk>/', views.TeacherUpdate.as_view(), name='edit_teacher'),
]
