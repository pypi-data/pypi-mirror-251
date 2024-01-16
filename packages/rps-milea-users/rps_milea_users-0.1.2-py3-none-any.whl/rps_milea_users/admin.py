from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BaseGroup
from django.utils.translation import gettext_lazy as _

from rps_milea_users.models import Group, User

# Remove the Default Group from the Default App and Register the Proxy
admin.site.unregister(BaseGroup)
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass

# Register New User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_login', 'is_active', 'is_staff')
    search_fields = ('email',)
    readonly_fields = ['last_login', 'date_joined']
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_("Personal info"), {'fields': ('first_name', 'last_name')}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        (_("Personal info"), {'fields': ('first_name', 'last_name')}),
    )
