from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        username = 'testuser'
        email = 'test@example.com'
        password = 'test12345'
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )
        user.email = email
        user.set_password(password)
        user.is_active = True
        user.save()
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created user "{username}"'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated user "{username}"'))
