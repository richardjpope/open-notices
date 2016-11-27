from django.core.management.base import BaseCommand, CommandError
from alerts.models import Alert
from core.tasks import send_alert

class Command(BaseCommand):
    help = 'Alert users'

    def handle(self, *args, **options):
        for alert in Alert.objects.all():
            print(".")
            send_alert.delay(alert.id)
