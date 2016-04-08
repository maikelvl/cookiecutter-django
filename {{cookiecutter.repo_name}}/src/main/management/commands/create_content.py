from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Create dummy data'

    def handle(self, *args, **options):
        print("Create content")
