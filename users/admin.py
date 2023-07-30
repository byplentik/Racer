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
        (None, {'fields': ('email', 'password')}),
        (('Личная Информация'), {'fields': ('name', 'last_name', 'last_login')}),
        (('Разрешения'), {
            'fields': ('is_staff', 'is_superuser'),
        })
    )
    list_display = ('email', 'name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(CustomUser, AdminCustomUser)
