from django.db import models
from django.utils import timezone


class DashboardEntry(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Transcription(models.Model):
    audio_file = models.FileField(upload_to='audio/')
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Transcription {self.id}"


class MeetingNote(models.Model):
    meeting_title = models.CharField(max_length=255)
    transcription = models.TextField()          # Full transcript text
    generated_notes = models.TextField()        # AI-generated summary
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.meeting_title


class MeetingPDF(models.Model):
    meeting = models.ForeignKey(MeetingNote, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='pdfs/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"PDF for {self.meeting.meeting_title}"
