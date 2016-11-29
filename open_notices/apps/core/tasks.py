from __future__ import absolute_import
from celery import shared_task
from alerts.models import Alert
from notices.models import Notice
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

@shared_task
def send_alert(alert_id):
    
    alert = Alert.objects.get(id=alert_id)

    #get notices that overlap with area of alert
    notices = Notice.objects.filter(location__intersects=alert.location, updated_at__gte=alert.last_checked_at)

    #update the last checked datetime for this user
    alert.last_checked_at = timezone.now()
    alert.save()

    #Send one email per notice
    for notice in notices:
        title = "Notice: %s" % notice.title
        message = notice.details
        send_mail(title, message, settings.EMAIL_FROM_ADDRESS, [alert.user.email])