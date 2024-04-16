from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        content_type = ContentType.objects.get(app_label='auth', model='user')
        admin_group, _ = Group.objects.get_or_create(name='admin')
        permission, _ = Permission.objects.get_or_create(
            codename='view_user',
            content_type=content_type
        )

        admin_group.permissions.add(permission)
        self.stdout.write("Permission created successfully!!!", style_func=self.style.SUCCESS)