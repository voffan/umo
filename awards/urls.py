from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from awards import views

urlpatterns = [
    path('', views.EmployeeAwardsList.as_view(), name='list_employee_awards'),
    path('create/',  views.EmployeeAwardsCreate.as_view(), name='create_employee_award'),
    path('delete/<int:pk>/', views.EmployeeAwardsDelete.as_view(), name='delete_employee_award'),
    path('edit/<int:pk>/', views.EmployeeAwardsUpdate.as_view(), name='edit_employee_award'),
    path('award_list', views.AwardsList.as_view(), name='list_awards'),
    path('create_award/',  views.AwardsCreate.as_view(), name='create_award'),
    path('delete_award/<int:pk>/', views.AwardsDelete.as_view(), name='delete_award'),
    path('edit_award/<int:pk>/', views.AwardsUpdate.as_view(), name='edit_award'),
    path('issuer_list', views.IssuersList.as_view(), name='list_issuers'),
    path('create_issuer/', views.IssuerCreate.as_view(), name='create_issuer'),
    path('delete_issuer/<int:pk>/', views.IssuerDelete.as_view(), name='delete_issuer'),
    path('edit_issuer/<int:pk>/', views.IssuerUpdate.as_view(), name='edit_issuer'),
]