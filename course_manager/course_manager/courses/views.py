# courses/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course
from .forms import CourseForm

# ListView shows a list of Course objects
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'  # template to render
    context_object_name = 'courses'             # name for list in template
    ordering = ['-created_at']                  # order newest first
    paginate_by = 10                            # optional pagination

# DetailView shows details for a single Course
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

# CreateView displays a form to create a new Course
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    # On successful creation, redirect to detail page via get_absolute_url()

# UpdateView displays a form to edit an existing Course
class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'

# DeleteView asks for confirmation and deletes
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:course_list')  # where to redirect after delete
