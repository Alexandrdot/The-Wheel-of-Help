from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        'username',
        'email',
        'admin_photo',
        'is_staff',
        'is_active',
        'date_joined',
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined', 'admin_photo_preview')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            'Профиль',
            {'fields': ('first_name', 'last_name', 'email', 'photo', 'admin_photo_preview', 'date_birth')},
        ),
        (
            'Права',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            'Служебное',
            {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2'),
            },
        ),
    )

    @admin.display(description='Фото')
    def admin_photo(self, obj):
        if obj is None or not obj.photo:
            return mark_safe('<span class="admin-muted">—</span>')
        return format_html(
            '<img src="{}" class="admin-thumb" width="36" height="36" alt="">',
            obj.photo.url,
        )

    @admin.display(description='Превью')
    def admin_photo_preview(self, obj):
        if obj is None or not obj.photo:
            return mark_safe('<span class="admin-muted">Фото не загружено</span>')
        return format_html(
            '<img src="{}" class="admin-thumb admin-thumb--lg" width="96" height="96" alt="">',
            obj.photo.url,
        )
