# course_manager/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),         # admin site
    path('', include('courses.urls')),       # include our app urls at root
]
