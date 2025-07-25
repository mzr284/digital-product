from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from .models import User


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone_number", "email")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_('Important dates'), {"fields": ("last_login", "data_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "phone_number", "email", "password1", "password2", "is_staff"),
        }),
    )
    list_display = ["username", "phone_number", "email", "is_staff"]
    search_fields = ('username__exact', )
    ordering = ('-id', )


admin.site.unregister(Group)
admin.site.register(User, MyUserAdmin)
