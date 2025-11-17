# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, OTP, AdminNotification

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email','name','is_staff','is_active')
    search_fields = ('email','name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Personal', {'fields': ('name','address','phone','nid_number','picture','gender','age','date_of_birth')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
    )
    add_fieldsets = ((None, {'classes':('wide',), 'fields': ('email','password1','password2')}),)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP)
admin.site.register(AdminNotification)
