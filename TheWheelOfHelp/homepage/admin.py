from django.contrib import admin
from .models import Category, CarService, TireService, TowTruck


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)


# Базовый класс для админки всех услуг
class BaseServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'address', 'phone', 'rating', 'is_published', 'time_create')
    list_display_links = ('title',)
    list_editable = ('is_published', 'rating')
    list_filter = ('is_published', 'category', 'rating')
    search_fields = ('title', 'address', 'phone')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'description')
        }),
        ('Контактная информация', {
            'fields': ('address', 'phone', 'work_time')
        }),
        ('Рейтинг и статус', {
            'fields': ('rating', 'is_published')
        }),
        ('Даты', {
            'fields': ('time_create', 'time_update'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('time_create', 'time_update')


@admin.register(CarService)
class CarServiceAdmin(BaseServiceAdmin):
    fieldsets = BaseServiceAdmin.fieldsets + (
        ('Специфичные поля для СТО', {
            'fields': ('specialization', 'diagnostic_available')
        }),
    )


@admin.register(TireService)
class TireServiceAdmin(BaseServiceAdmin):
    fieldsets = BaseServiceAdmin.fieldsets + (
        ('Специфичные поля для шиномонтажа', {
            'fields': ('wheel_size_from', 'wheel_size_to', 'tire_storage')
        }),
    )


@admin.register(TowTruck)
class TowTruckAdmin(BaseServiceAdmin):
    fieldsets = BaseServiceAdmin.fieldsets + (
        ('Специфичные поля для эвакуатора', {
            'fields': ('load_capacity', 'work_24_7')
        }),
    )