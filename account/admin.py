from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'name', 'is_active',)
    list_filter = ('email', 'name', 'is_staff', 'is_active',)
    fieldsets = (
        ('Information', {'fields': ('email', 'name', 'password', 'date_joined', 'account_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        
    )
    readonly_fields = ['date_joined']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active',)}
        ),
    )
    search_fields = ['email', 'account_type']
    ordering = ('pk',)

admin.site.register(User, CustomUserAdmin)

