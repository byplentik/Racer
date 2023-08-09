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
                'fields': ('phone_number', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password', 'delivery_address', 'delivery_index')}),
        (('Личная Информация'), {'fields': ('name', 'last_name', 'last_login')}),
        (('Разрешения'), {
            'fields': ('is_staff', 'is_superuser'),
        })
    )
    list_display = ('phone_number', 'name', 'last_name', 'email', 'delivery_index', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'name', 'last_name', 'phone_number')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(CustomUser, AdminCustomUser)
