from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, DeliveryAddressModel
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
    search_fields = ['email']


admin.site.register(CustomUser, AdminCustomUser)


@admin.register(DeliveryAddressModel)
class AdminDeliveryAddressModel(admin.ModelAdmin):
    list_display = ['phone_number', 'postal_code', 'user', 'name_address']
