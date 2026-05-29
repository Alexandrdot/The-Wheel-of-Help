from django import template

from homepage.permissions import (
    user_can_change_service as can_change_service,
    user_can_delete_service as can_delete_service,
)

register = template.Library()


@register.simple_tag
def service_change_perm(service):
    return f'{service._meta.app_label}.change_{service._meta.model_name}'


@register.simple_tag
def service_delete_perm(service):
    return f'{service._meta.app_label}.delete_{service._meta.model_name}'


@register.filter
def user_has_perm(user, perm):
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.has_perm(perm)


@register.filter
def user_can_edit_service(user, service):
    return can_change_service(user, service)


@register.filter
def user_can_delete_service(user, service):
    return can_delete_service(user, service)
