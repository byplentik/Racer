from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser
from .forms import UserCreationForm, UserChangeForm


class AdminCustomUser(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        (('Разрешения'), {
            'fields': ('is_staff', 'is_superuser'),
        })
    )
    list_display = ('email', 'username', 'slug')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(CustomUser, AdminCustomUser)
