from django.urls import reverse

from .constants import CATEGORY_SLUG_STO, CATEGORY_SLUG_TIRE, CATEGORY_SLUG_TOW
from .models import Category


def get_mainmenu():
    return [
        {'title': 'Главная', 'url': reverse('homepage:index')},
        {'title': 'СТО', 'url': reverse('homepage:category_detail', kwargs={'cat_slug': CATEGORY_SLUG_STO})},
        {'title': 'Эвакуаторы', 'url': reverse('homepage:category_detail', kwargs={'cat_slug': CATEGORY_SLUG_TOW})},
        {'title': 'Шиномонтаж', 'url': reverse('homepage:category_detail', kwargs={'cat_slug': CATEGORY_SLUG_TIRE})},
        {'title': 'Контакты', 'url': reverse('homepage:contact')},
    ]


class DataMixin:
    """Общий контекст (сайдбар) и настройки пагинации для CBV."""

    paginate_by = 5

    def get_mixin_context(self, context, **kwargs):
        context['categories'] = Category.objects.all()
        context.update(kwargs)
        return context
