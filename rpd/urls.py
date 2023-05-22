from django.contrib import admin
from django.urls import path

from rpd import views, views_api

admin.autodiscover()

api = ([
    path('rpd/deleteResult/', views_api.delete_result, name='delete_result'),
], 'api')

urlpatterns = [
    path('rpd/<int:rpddiscipline_id>', views.rpd_create, name='rpd'),
    path('list/', views.RPDList.as_view(), name='rpd_list'),
    path('list/empty/', views.empty_rpd_create, name='rpd_list'),
    path('list/delete/<int:id>/', views.rpd_delete, name='rpd_list'),
    path('export/<int:rpddiscipline_id>', views.export_docx, name='rpd_export'),
    path('disciplines/create/<int:discipline_id>', views.create_rpd_from_discipline, name='create_rpd_from_disciplines'),
    path('rpd/paragraph1/<int:rpddiscipline_id>', views.rpd_paragraph1_create, name='create_rpd_paragraph1'),
    path('rpd/paragraph2/<int:rpddiscipline_id>', views.rpd_paragraph2_create, name='create_rpd_paragraph2'),
    path('rpd/paragraph3/<int:rpddiscipline_id>', views.rpd_paragraph3_create, name='create_rpd_paragraph3'),
    path('rpd/paragraph4/<int:rpddiscipline_id>', views.rpd_paragraph4_create, name='create_rpd_paragraph4'),
    path('rpd/paragraph5/<int:rpddiscipline_id>', views.rpd_paragraph5_create, name='create_rpd_paragraph5'),
    path('rpd/paragraph6/<int:rpddiscipline_id>', views.rpd_paragraph6_create, name='create_rpd_paragraph6'),
    path('rpd/paragraph7/<int:rpddiscipline_id>', views.rpd_paragraph7_create, name='create_rpd_paragraph7'),
    path('rpd/paragraph8/<int:rpddiscipline_id>', views.rpd_paragraph8_create, name='create_rpd_paragraph8'),
    path('rpd/paragraph9/<int:rpddiscipline_id>', views.rpd_paragraph9_create, name='create_rpd_paragraph9'),
    path('rpd/paragraph10/<int:rpddiscipline_id>', views.rpd_paragraph10_create, name='create_rpd_paragraph10'),

    path('rpd/deleteResult/', views_api.delete_result, name='delete_result'),
    path('rpd/deleteBasement/', views_api.delete_basement, name='delete_basement'),
    path('rpd/deleteTheme/', views_api.delete_theme, name='delete_theme'),
]
