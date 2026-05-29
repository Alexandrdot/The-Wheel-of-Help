from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from users.models import User


class Command(BaseCommand):
    help = 'Создаёт группу moderator, пользовательское разрешение social_auth и назначает права на услуги.'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(User)
        social_perm, created = Permission.objects.get_or_create(
            codename='social_auth',
            content_type=content_type,
            defaults={'name': 'Social Auth'},
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Создано разрешение: Social Auth (social_auth)'))
        else:
            self.stdout.write('Разрешение social_auth уже существует')

        group, created = Group.objects.get_or_create(name='moderator')
        service_perms = Permission.objects.filter(
            content_type__app_label='homepage',
            codename__in=[
                'add_carservice', 'change_carservice', 'delete_carservice', 'view_carservice',
                'add_tireservice', 'change_tireservice', 'delete_tireservice', 'view_tireservice',
                'add_towtruck', 'change_towtruck', 'delete_towtruck', 'view_towtruck',
            ],
        )
        group.permissions.set(service_perms)
        self.stdout.write(self.style.SUCCESS(f'Группа moderator: {service_perms.count()} разрешений на услуги'))

        self.stdout.write(
            self.style.WARNING(
                'Назначьте группу moderator или разрешения пользователям в админ-панели: /admin/users/user/'
            )
        )
