from django.core.management.base import BaseCommand
from base.models import User, Chat, Message

class Command(BaseCommand):
    help = 'Delete all objects in the database'

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all objects'))

        Chat.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all objects'))

        Message.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all objects'))
