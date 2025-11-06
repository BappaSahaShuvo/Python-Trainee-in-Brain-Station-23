# courses/urls.py
from django.urls import path
from . import views

app_name = 'courses'  # namespacing URLs

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),         # list all courses
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),  # detail
    path('course/add/', views.CourseCreateView.as_view(), name='course_add'),         # create
    path('course/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'), # update
    path('course/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'), # delete
]
