from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users app
    path('', include('users.urls')),  # Home, signup, login, OTP

    # Meeting app
    path('', include('meeting.urls')),  # dashboard, history, profile
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
