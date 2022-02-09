from django.urls import path
from django.contrib import admin

from hours import views

admin.autodiscover()
urlpatterns = [
    path('courselist/', views.CourseList.as_view(), name='course_list'),
    path('courseupload/', views.upload_course, name='course_upload'),
    path('contingentlist/', views.ContingentList.as_view(), name='contingent_list'),
    path('contingentupload', views.upload_contingent, name='contingent_upload'),
    path('editcontingent/<int:pk>/', views.ContingentUpdate.as_view(), name='edit_contingent'),
    path('employeelist/', views.EmployeeList.as_view(), name='employee_list'),
    path('editemployee/<int:pk>', views.EmployeeUpdate.as_view(), name='edit_employee'),
]