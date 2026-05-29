from django.contrib import admin, messages
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from .admin_display import (
    published_badge,
    rating_stars,
    reaction_badge,
    service_target_link,
    truncate_text,
)
from .admin_display import admin_thumbnail
from .models import (
    CarService,
    Category,
    Comment,
    ContactInfo,
    ServiceReaction,
    Status,
    Tag,
    TireService,
    TowTruck,
)

admin.site.site_header = 'Колесо помощи — панель управления'
admin.site.site_title = 'Колесо помощи'
admin.site.index_title = 'Управление контентом сайта'


class RatingRangeFilter(admin.SimpleListFilter):
    title = _('Диапазон рейтинга')
    parameter_name = 'rating_range'

    def lookups(self, request, model_admin):
        return (
            ('excellent', 'Отлично (4.5 – 5.0)'),
            ('good', 'Хорошо (4.0 – 4.5)'),
            ('normal', 'Нормально (3.0 – 4.0)'),
            ('low', 'Низкий (менее 3.0)'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'excellent':
            return queryset.filter(rating__gte=4.5, rating__lte=5.0)
        if value == 'good':
            return queryset.filter(rating__gte=4.0, rating__lt=4.5)
        if value == 'normal':
            return queryset.filter(rating__gte=3.0, rating__lt=4.0)
        if value == 'low':
            return queryset.filter(rating__lt=3.0)
        return queryset


class BaseServiceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'published_badge',
        'rating',
        'rating_stars',
        'author',
        'phone',
        'time_create',
    )
    list_display_links = ('title',)
    list_editable = ('rating',)
    list_per_page = 15
    ordering = ('-time_create',)
    date_hierarchy = 'time_create'
    list_select_related = ('category', 'author')
    autocomplete_fields = ('category', 'author', 'contact_info')
    filter_horizontal = ('tags',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug', 'address', 'phone', 'description', 'category__name')
    list_filter = ('category', 'is_published', RatingRangeFilter, 'author')
    readonly_fields = ('time_create', 'time_update')
    actions = ('publish_selected', 'unpublish_selected', 'increase_rating', 'decrease_rating')

    @admin.display(description='Статус')
    def published_badge(self, obj):
        return published_badge(obj)

    @admin.display(description='Рейтинг')
    def rating_stars(self, obj):
        return rating_stars(obj)

    @admin.action(description='Опубликовать выбранные')
    def publish_selected(self, request, queryset):
        count = queryset.update(is_published=Status.PUBLISHED)
        self.message_user(request, f'Опубликовано: {count}', messages.SUCCESS)

    @admin.action(description='Снять с публикации')
    def unpublish_selected(self, request, queryset):
        count = queryset.update(is_published=Status.DRAFT)
        self.message_user(request, f'Снято с публикации: {count}', messages.WARNING)

    @admin.action(description='Увеличить рейтинг на 0.5')
    def increase_rating(self, request, queryset):
        count = queryset.update(rating=F('rating') + 0.5)
        self.message_user(request, f'Рейтинг увеличен: {count}', messages.INFO)

    @admin.action(description='Уменьшить рейтинг на 0.5')
    def decrease_rating(self, request, queryset):
        count = queryset.update(rating=F('rating') - 0.5)
        self.message_user(request, f'Рейтинг уменьшен: {count}', messages.INFO)

    def get_fieldsets(self, request, obj=None):
        return (
            ('Основное', {'fields': ('title', 'slug', 'category', 'description')}),
            *self.extra_fieldsets(),
            ('Контакты', {'fields': ('address', 'phone', 'work_time')}),
            (
                'Публикация',
                {'fields': ('rating', 'is_published', 'author')},
            ),
            (
                'Связи',
                {
                    'fields': ('tags', 'contact_info'),
                    'classes': ('collapse',),
                },
            ),
            (
                'Служебное',
                {
                    'fields': ('time_create', 'time_update'),
                    'classes': ('collapse',),
                },
            ),
        )

    def extra_fieldsets(self):
        return ()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'website', 'social_vk', 'social_tg')
    list_display_links = ('email',)
    search_fields = ('email', 'website')
    fieldsets = (
        ('Контакты', {'fields': ('email', 'website')}),
        ('Соцсети', {'fields': ('social_vk', 'social_tg')}),
    )


@admin.register(CarService)
class CarServiceAdmin(BaseServiceAdmin):
    list_display = (
        'title',
        'admin_photo',
        'category',
        'published_badge',
        'rating',
        'rating_stars',
        'author',
        'time_create',
    )
    list_filter = ('category', 'is_published', 'diagnostic_available', RatingRangeFilter, 'author')
    readonly_fields = ('time_create', 'time_update', 'admin_photo_preview')

    def extra_fieldsets(self):
        return (
            (
                'Изображение',
                {'fields': ('image', 'admin_photo_preview')},
            ),
            (
                'СТО',
                {
                    'fields': ('specialization', 'diagnostic_available'),
                    'classes': ('collapse',),
                },
            ),
        )

    @admin.display(description='Фото')
    def admin_photo(self, obj):
        if obj is None:
            return '—'
        return admin_thumbnail(obj.image, 48, 48)

    @admin.display(description='Превью')
    def admin_photo_preview(self, obj):
        if obj is None:
            return '—'
        return admin_thumbnail(obj.image, 120, 120)


@admin.register(TireService)
class TireServiceAdmin(BaseServiceAdmin):
    list_filter = ('category', 'is_published', 'tire_storage', RatingRangeFilter, 'author')

    def extra_fieldsets(self):
        return (
            (
                'Шиномонтаж',
                {
                    'fields': ('wheel_size_from', 'wheel_size_to', 'tire_storage'),
                    'classes': ('collapse',),
                },
            ),
        )


@admin.register(TowTruck)
class TowTruckAdmin(BaseServiceAdmin):
    list_filter = ('category', 'is_published', 'work_24_7', RatingRangeFilter, 'author')

    def extra_fieldsets(self):
        return (
            (
                'Эвакуатор',
                {
                    'fields': ('load_capacity', 'work_24_7'),
                    'classes': ('collapse',),
                },
            ),
        )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'service_link', 'short_text', 'time_create')
    list_display_links = ('short_text',)
    list_filter = ('content_type', 'time_create')
    search_fields = ('text', 'author__username', 'author__email')
    readonly_fields = ('time_create', 'service_link')
    autocomplete_fields = ('author',)
    date_hierarchy = 'time_create'
    ordering = ('-time_create',)

    fieldsets = (
        ('Комментарий', {'fields': ('author', 'content_type', 'object_id', 'text')}),
        ('Служебное', {'fields': ('time_create', 'service_link')}),
    )

    @admin.display(description='Услуга')
    def service_link(self, obj):
        if obj is None or not obj.pk:
            return '—'
        return service_target_link(obj)

    @admin.display(description='Текст')
    def short_text(self, obj):
        return truncate_text(obj.text, 80)


@admin.register(ServiceReaction)
class ServiceReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_link', 'reaction_label', 'time_create')
    list_filter = ('content_type', 'value', 'time_create')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('time_create', 'service_link', 'reaction_label')
    autocomplete_fields = ('user',)
    date_hierarchy = 'time_create'
    ordering = ('-time_create',)

    @admin.display(description='Услуга')
    def service_link(self, obj):
        if obj is None or not obj.pk:
            return '—'
        return service_target_link(obj)

    @admin.display(description='Оценка')
    def reaction_label(self, obj):
        if obj is None or not obj.pk:
            return '—'
        return reaction_badge(obj)
