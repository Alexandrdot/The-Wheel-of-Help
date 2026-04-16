from django.contrib import admin
from django.contrib import messages
from django.db.models import F
from django.utils.translation import gettext_lazy as _
from .models import Category, CarService, TireService, TowTruck, Tag, ContactInfo, Status


# Собственный фильтр по диапазону рейтинга
class RatingRangeFilter(admin.SimpleListFilter):
    title = _("Диапазон рейтинга")
    parameter_name = 'rating_range'
    
    def lookups(self, request, model_admin):
        return (
            ('excellent', 'Отлично (4.5 - 5.0)'),
            ('good', 'Хорошо (4.0 - 4.5)'),
            ('normal', 'Нормально (3.0 - 4.0)'),
            ('low', 'Низкий (менее 3.0)'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'excellent':
            return queryset.filter(rating__gte=4.5, rating__lte=5.0)
        if self.value() == 'good':
            return queryset.filter(rating__gte=4.0, rating__lt=4.5)
        if self.value() == 'normal':
            return queryset.filter(rating__gte=3.0, rating__lt=4.0)
        if self.value() == 'low':
            return queryset.filter(rating__lt=3.0)
        return queryset


# Настройка заголовков админ-панели
admin.site.site_header = "АвтоПомощь - Панель управления"
admin.site.site_title = "АвтоПомощь"
admin.site.index_title = "Добро пожаловать в систему управления сайтом"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'website', 'social_vk', 'social_tg')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'website')


@admin.register(CarService)
class CarServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'address', 'phone', 'rating', 'is_published', 'short_description', 'rating_stars')
    list_display_links = ('title',)
    list_editable = ('is_published', 'rating')
    list_filter = ('category', 'is_published', 'diagnostic_available', RatingRangeFilter)
    search_fields = ('title', 'address', 'phone', 'category__name', 'specialization')
    ordering = ('-rating',)
    list_per_page = 10
    actions = ['publish_selected', 'unpublish_selected', 'increase_rating', 'decrease_rating']
    
    # Пользовательское поле 1: краткое описание
    def short_description(self, obj):
        if len(obj.description) > 50:
            return obj.description[:50] + '...'
        return obj.description
    short_description.short_description = "Краткое описание"
    
    # Пользовательское поле 2: рейтинг звездами
    def rating_stars(self, obj):
        full_stars = int(obj.rating)
        empty_stars = 5 - full_stars
        return '★' * full_stars + '☆' * empty_stars
    rating_stars.short_description = "Рейтинг"

    @admin.action(description="Опубликовать выбранные СТО")
    def publish_selected(self, request, queryset):
        count = queryset.update(is_published=Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} СТО", messages.SUCCESS)
    
    @admin.action(description="Снять с публикации выбранные СТО")
    def unpublish_selected(self, request, queryset):
        count = queryset.update(is_published=Status.DRAFT)
        self.message_user(request, f"Снято с публикации {count} СТО", messages.WARNING)
    
    @admin.action(description="Увеличить рейтинг на 0.5")
    def increase_rating(self, request, queryset):
        count = queryset.update(rating=F('rating') + 0.5)
        self.message_user(request, f"Рейтинг увеличен для {count} СТО", messages.INFO)
    
    @admin.action(description="Уменьшить рейтинг на 0.5")
    def decrease_rating(self, request, queryset):
        count = queryset.update(rating=F('rating') - 0.5)
        self.message_user(request, f"Рейтинг уменьшен для {count} СТО", messages.INFO)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'category', 'description')
        }),
        ('Контактная информация', {
            'fields': ('address', 'phone', 'work_time')
        }),
        ('Специфичные поля для СТО', {
            'fields': ('specialization', 'diagnostic_available'),
            'classes': ('collapse',)
        }),
        ('Рейтинг и статус', {
            'fields': ('rating', 'is_published')
        }),
        ('Связи', {
            'fields': ('tags', 'contact_info'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('time_create', 'time_update'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('time_create', 'time_update')
    filter_horizontal = ('tags',)
    autocomplete_fields = ('category',)


@admin.register(TireService)
class TireServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'address', 'phone', 'rating', 'is_published', 'tire_storage')
    list_display_links = ('title',)
    list_editable = ('is_published', 'rating')
    list_filter = ('category', 'is_published', 'tire_storage', RatingRangeFilter)
    search_fields = ('title', 'address', 'phone', 'category__name')
    ordering = ('-rating',)
    list_per_page = 10
    actions = ['publish_selected', 'unpublish_selected', 'increase_rating', 'decrease_rating']
    
    @admin.action(description="Опубликовать выбранные шиномонтажи")
    def publish_selected(self, request, queryset):
        count = queryset.update(is_published=Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} шиномонтажей", messages.SUCCESS)
    
    @admin.action(description="Снять с публикации выбранные шиномонтажи")
    def unpublish_selected(self, request, queryset):
        count = queryset.update(is_published=Status.DRAFT)
        self.message_user(request, f"Снято с публикации {count} шиномонтажей", messages.WARNING)
    
    @admin.action(description="Увеличить рейтинг на 0.5")
    def increase_rating(self, request, queryset):
        count = queryset.update(rating=F('rating') + 0.5)
        self.message_user(request, f"Рейтинг увеличен для {count} шиномонтажей", messages.INFO)
    
    @admin.action(description="Уменьшить рейтинг на 0.5")
    def decrease_rating(self, request, queryset):
        count = queryset.update(rating=F('rating') - 0.5)
        self.message_user(request, f"Рейтинг уменьшен для {count} шиномонтажей", messages.INFO)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'category', 'description')
        }),
        ('Контактная информация', {
            'fields': ('address', 'phone', 'work_time')
        }),
        ('Специфичные поля для шиномонтажа', {
            'fields': ('wheel_size_from', 'wheel_size_to', 'tire_storage'),
            'classes': ('collapse',)
        }),
        ('Рейтинг и статус', {
            'fields': ('rating', 'is_published')
        }),
        ('Связи', {
            'fields': ('tags', 'contact_info'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('time_create', 'time_update'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('time_create', 'time_update')
    filter_horizontal = ('tags',)
    autocomplete_fields = ('category',)


@admin.register(TowTruck)
class TowTruckAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'address', 'phone', 'rating', 'is_published', 'work_24_7')
    list_display_links = ('title',)
    list_editable = ('is_published', 'rating')
    list_filter = ('category', 'is_published', 'work_24_7', RatingRangeFilter)
    search_fields = ('title', 'address', 'phone', 'category__name')
    ordering = ('-rating',)
    list_per_page = 10
    actions = ['publish_selected', 'unpublish_selected', 'increase_rating', 'decrease_rating']
    
    @admin.action(description="Опубликовать выбранные эвакуаторы")
    def publish_selected(self, request, queryset):
        count = queryset.update(is_published=Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} эвакуаторов", messages.SUCCESS)
    
    @admin.action(description="Снять с публикации выбранные эвакуаторы")
    def unpublish_selected(self, request, queryset):
        count = queryset.update(is_published=Status.DRAFT)
        self.message_user(request, f"Снято с публикации {count} эвакуаторов", messages.WARNING)
    
    @admin.action(description="Увеличить рейтинг на 0.5")
    def increase_rating(self, request, queryset):
        count = queryset.update(rating=F('rating') + 0.5)
        self.message_user(request, f"Рейтинг увеличен для {count} эвакуаторов", messages.INFO)
    
    @admin.action(description="Уменьшить рейтинг на 0.5")
    def decrease_rating(self, request, queryset):
        count = queryset.update(rating=F('rating') - 0.5)
        self.message_user(request, f"Рейтинг уменьшен для {count} эвакуаторов", messages.INFO)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'category', 'description')
        }),
        ('Контактная информация', {
            'fields': ('address', 'phone', 'work_time')
        }),
        ('Специфичные поля для эвакуатора', {
            'fields': ('load_capacity', 'work_24_7'),
            'classes': ('collapse',)
        }),
        ('Рейтинг и статус', {
            'fields': ('rating', 'is_published')
        }),
        ('Связи', {
            'fields': ('tags', 'contact_info'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('time_create', 'time_update'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('time_create', 'time_update')
    filter_horizontal = ('tags',)
    autocomplete_fields = ('category',)
