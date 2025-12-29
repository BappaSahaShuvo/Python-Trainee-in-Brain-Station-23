from django.contrib import admin
from .models import CustomUser, EmailOTP

admin.site.register(CustomUser)
admin.site.register(EmailOTP)
