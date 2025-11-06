# courses/models.py
from django.db import models
from django.urls import reverse

class Course(models.Model):
    # title: course name
    title = models.CharField(max_length=200)

    # description: optional longer text
    description = models.TextField(blank=True)

    # instructor: simple text field to store instructor name
    instructor = models.CharField(max_length=100)

    # start_date: optional date field
    start_date = models.DateField(null=True, blank=True)

    # seats: integer field for how many seats are available
    seats = models.PositiveIntegerField(default=0)

    # created_at: auto timestamp when record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # updated_at: auto timestamp updated on every save
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # human readable representation used in admin and shell
        return f"{self.title} - {self.instructor}"

    def get_absolute_url(self):
        # used to obtain canonical URL for an instance
        return reverse('courses:course_detail', args=[str(self.id)])
