from django.conf import settings

from homepage.utils import get_mainmenu


def get_mainmenu_context(request):
    return {
        'mainmenu': get_mainmenu(),
        'default_user_image': settings.DEFAULT_USER_IMAGE,
    }
