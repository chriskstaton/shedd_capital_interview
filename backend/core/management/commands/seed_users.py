from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


USERS = [
    {
        "username": "submitter",
        "first_name": "Sample",
        "last_name": "Submitter",
        "password": "password123",
        "is_staff": False,
    },
    {
        "username": "manager",
        "first_name": "Sample",
        "last_name": "Manager",
        "password": "password123",
        "is_staff": True,
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample submitter and manager users"

    def handle(self, *args, **options):
        for data in USERS:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "is_staff": data["is_staff"],
                },
            )
            if created:
                user.set_password(data["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.get_full_name()} ({user.username})"))
            else:
                self.stdout.write(f"User already exists: {user.get_full_name()} ({user.username})")
