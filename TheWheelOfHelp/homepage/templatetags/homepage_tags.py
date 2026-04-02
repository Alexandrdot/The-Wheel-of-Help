from django import template
from ..models import Tag

register = template.Library()


@register.inclusion_tag('includes/tags_list.html')  
def show_all_tags():
    return {'tags': Tag.objects.all()}


# Данные для категорий
categories = [
    {'id': 1, 'name': 'СТО', 'url': 'tech_station', 'count': 15},
    {'id': 2, 'name': 'Эвакуаторы', 'url': 'evacuator', 'count': 8},
    {'id': 3, 'name': 'Шиномонтаж', 'url': 'tire_service', 'count': 12},
]


# Простой тег для получения категорий
@register.simple_tag
def get_categories():
    """Возвращает список всех категорий"""
    return categories

# Включающий тег для отображения категорий
@register.inclusion_tag('homepage/list_categories.html')
def show_categories():
    """Отображает список категорий"""
    return {"categories": categories}

# Тег для форматирования рейтинга
@register.simple_tag
def format_rating(rating):
    """Форматирует рейтинг и возвращает текстовое описание"""
    if rating >= 4.8:
        return "Отличный"
    elif rating >= 4.0:
        return "Хороший"
    elif rating >= 3.0:
        return "Неплохой"
    elif rating >= 2.0:
        return "Средний"
    else:
        return "Плохой"

# Тег для получения звезд рейтинга
@register.simple_tag
def get_stars(rating):
    """Возвращает HTML со звездами рейтинга"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = "★" * full_stars
    if half_star:
        stars += "½"
    stars += "☆" * empty_stars
    
    return stars

# Тег для обрезки текста
@register.simple_tag
def truncate_text(text, length=100):
    """Обрезает текст до указанной длины"""
    if len(text) <= length:
        return text
    return text[:length] + "..."