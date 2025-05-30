from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, VerificationCode
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin):
    # admin panelda ko'rsatiladigan maydonlar
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_verified')
    list_filter = ('is_staff', 'is_active', 'is_verified')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Shaxsiy ma\'lumotlar'), {'fields': ('first_name', 'last_name', 'phone', 'image')}),
        (_('Ruxsatlar'), {'fields': ('is_staff', 'is_active', 'is_verified', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Muhim sanalar'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1', 'password2', 'is_staff', 'is_active', 'is_verified'),
        }),
    )

admin.site.register(User, UserAdmin)


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'created_at')
    search_fields = ('email', 'code')
    readonly_fields = ('created_at',)
