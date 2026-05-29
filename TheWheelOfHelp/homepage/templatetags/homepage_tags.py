from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import Tag

register = template.Library()


@register.inclusion_tag('includes/tags_list.html')
def show_all_tags():
    return {'tags': Tag.objects.all()}


@register.filter
def content_type_id(obj):
    return ContentType.objects.get_for_model(obj.__class__).pk
