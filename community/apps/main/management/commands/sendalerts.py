from django.core.management.base import BaseCommand, CommandError
from alerts.models import Alert
from main.tasks import send_alert

class Command(BaseCommand):
    help = 'Alert users'

    def handle(self, *args, **options):
        for alert in Alert.objects.all():
            send_alert.delay(alert.id)
