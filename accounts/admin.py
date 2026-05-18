from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'email', 'username',
                    'fullname', 'is_staff', 'is_superuser']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('fullname',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + \
        ((None, {'fields': ('fullname',)}),)


admin.site.register(CustomUser, CustomUserAdmin)
