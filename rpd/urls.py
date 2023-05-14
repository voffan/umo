from django.contrib import admin
from django.urls import path

from rpd import views

admin.autodiscover()
urlpatterns = [
    path('rpd/<int:rpddiscipline_id>', views.rpd_create, name='rpd'),
    path('list/', views.RPDList.as_view(), name='rpd_list'),
    path('list/empty/', views.empty_rpd_create, name='rpd_list'),
    path('list/delete/<int:id>/', views.rpd_delete, name='rpd_list'),
    path('export/<int:rpddiscipline_id>', views.export_docx, name='rpd_export'),
]
