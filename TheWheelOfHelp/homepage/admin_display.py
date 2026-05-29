from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import CarService, ServiceReaction, Status, TireService, TowTruck

SERVICE_MODELS = (CarService, TireService, TowTruck)


def _admin_badge(label, css_class):
    return format_html('<span class="admin-badge {}">{}</span>', css_class, label)


def published_badge(obj):
    if obj.is_published == Status.PUBLISHED:
        return _admin_badge('Опубликовано', 'admin-badge--success')
    return _admin_badge('Черновик', 'admin-badge--muted')


published_badge.short_description = 'Статус'


def rating_stars(obj):
    full = max(0, min(5, int(obj.rating)))
    stars = format_html(
        '<span class="admin-stars" title="{}">{}<span class="admin-stars__empty">{}</span></span>',
        obj.rating,
        '★' * full,
        '☆' * (5 - full),
    )
    return stars


rating_stars.short_description = 'Рейтинг'


def short_description_field(obj, length=50):
    if not obj.description:
        return '—'
    if len(obj.description) > length:
        return f'{obj.description[:length]}…'
    return obj.description


short_description_field.short_description = 'Описание'


def truncate_text(value, length=80):
    if not value:
        return '—'
    if len(value) > length:
        return f'{value[:length]}…'
    return value


def admin_thumbnail(image_field, width=56, height=56):
    if image_field:
        return format_html(
            '<img src="{}" class="admin-thumb" width="{}" height="{}" alt="">',
            image_field.url,
            width,
            height,
        )
    return mark_safe('<span class="admin-muted">Нет фото</span>')


def service_target_link(obj):
    model = obj.content_type.model_class()
    if model not in SERVICE_MODELS:
        return f'{obj.content_type} #{obj.object_id}'
    try:
        service = model.objects.get(pk=obj.object_id)
    except model.DoesNotExist:
        return format_html('<span class="admin-muted">Удалено (#{})</span>', obj.object_id)
    url = reverse(
        f'admin:{service._meta.app_label}_{service._meta.model_name}_change',
        args=[service.pk],
    )
    return format_html('<a href="{}">{}</a>', url, service.title)


service_target_link.short_description = 'Услуга'


def reaction_badge(obj):
    if obj.value == ServiceReaction.LIKE:
        return _admin_badge('👍 Лайк', 'admin-badge--success')
    return _admin_badge('👎 Дизлайк', 'admin-badge--danger')


reaction_badge.short_description = 'Оценка'
