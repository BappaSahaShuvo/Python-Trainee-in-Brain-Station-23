# courses/forms.py
from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        # fields that will be in the form
        fields = ['title', 'description', 'instructor', 'start_date', 'seats']
        # optional: widgets or labels can be customized here
