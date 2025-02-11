from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(email="admintest@mail.ru", phone_number="7 777 777 777", country="Country")
        user.set_password("adminpass")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Администратор успешно создан. {user.email}"))
