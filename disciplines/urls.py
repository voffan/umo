from django.conf.urls import url, include

from disciplines import views, views_api, view_excel

api = ([
    url(r'^brs_scores$', views_api.brs_scores, name='brs_scores'),
    url(r'^set_max_points$', views_api.set_max_points, name='set_max_points'),
    url(r'^get_max_points$', views_api.get_max_points, name='get_max_points'),
    url(r'^add_course_to_teacher$', views_api.add_course_to_teacher, name='add_course_to_teacher'),
    url(r'^delete_course_teacher$', views_api.delete_course_teacher, name='delete_course_teacher'),
    url(r'^exam_scores$', views_api.exam_scores, name='exam_scores'),
    url(r'^finish_exam$', views_api.finish_exam, name='finish_exam')
], 'api')

excel = ([
    url(r'^brs_scores$', views.export_brs_points, name='brs_scores'),
    url(r'^exam_scores', views.exam_report, name='exam_scores')
], 'excel')

urlpatterns = [
    url(r'^add/$', views.DisciplineCreate.as_view(), name='disciplines_add'),
    #url(r'(?P<pk>[0-9]+)/update/$', views.DisciplineUpdate.as_view(), name='update'),
    url(r'^delete/$', views.discipline_delete, name='delete'),
    url(r'^(?P<pk>[0-9]+)/$', views.discipline_detail, name='detail'),
    url(r'^details_list/$', views.DisciplineDetailsList.as_view(), name='details_list'),
    url(r'^add_details/$', views.DetailsCreate.as_view(), name='details_add'),
    #url(r'(?P<pk>[0-9]+)/update_details/$', views.DisciplineDetailsUpdate.as_view(), name='update_details'),
    url(r'^export/$', views.export_to_excel, name='export'),
    url(r'^excel/$', views.excel, name='excel'),
    url(r'^list/(?P<pk>[0-9]+)/$', views.list_disc, name='disciplines'),
    url(r'^all_disciplines/$', views.DisciplineList.as_view(), name='disciplines_list'),
    url(r'^dataforekran/$', views.get_data_for_ekran, name='dataforekran'),
    url(r'^subjects/$', views.subjects, name='subjects'),
    url(r'^scores/(?P<pk>[0-9]+)/$', views.StudentsScoresView.as_view(), name='brs_scores'),
    url(r'^$', views.teachers_subjects, name='mysubjects'),
    url(r'^api/',include(api, namespace='api')),
    url(r'^excel/',include(excel, namespace='excel')),
    url(r'^exam_points/(?P<pk>[0-9]+)/(?P<control_id>[0-9]+)$', views.ExamPointsListView.as_view(), name='brs_student_list')
]
