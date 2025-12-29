from django.urls import path
from .views import dashboard, history, profile, summary_avatar

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("history/", history, name="history"),
    path("profile/", profile, name="profile"),
    path("summary-avatar/<int:meeting_id>/", summary_avatar, name="summary_avatar"),
]
