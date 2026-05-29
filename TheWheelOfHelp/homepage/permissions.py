def user_can_add_service(user):
    return user.is_authenticated


def user_can_change_service(user, service):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if user.has_perm(service.change_permission()):
        return True
    return service.author_id == user.pk


def user_can_delete_service(user, service):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if user.has_perm(service.delete_permission()):
        return True
    return service.author_id == user.pk
