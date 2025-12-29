from django.db import models
from django.conf import settings


class Meeting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_file = models.FileField(upload_to="uploads/")
    transcript = models.TextField(blank=True)
    summary = models.TextField(blank=True)

    # Auto-extracted decisions & action items
    decisions = models.TextField(blank=True)
    action_items = models.TextField(blank=True)

    # Timeline & speaker diarization
    timeline = models.JSONField(blank=True, null=True)
    speakers = models.JSONField(blank=True, null=True)

    # Downloadable files
    pdf = models.FileField(upload_to="pdfs/", blank=True, null=True)
    txt = models.FileField(upload_to="txts/", blank=True, null=True)
    docx = models.FileField(upload_to="docxs/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"
