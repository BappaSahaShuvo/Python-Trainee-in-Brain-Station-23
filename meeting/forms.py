from django import forms


class UploadMeetingForm(forms.Form):
    file = forms.FileField()
