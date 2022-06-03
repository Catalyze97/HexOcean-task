"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User
from tiers.models import (
    Tier,
    CustomImages,
)


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name', 'account_plan']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name')}),
        (
            _('Permissions'),
            {
                'fields': (

                    'account_plan',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'account_plan',
                'is_active',
                'is_staff',
                'is_superuser',

            )
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Tier)
admin.site.register(CustomImages)
