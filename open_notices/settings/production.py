import dj_database_url
from open_notices.settings.base import *

DEBUG = os.environ.get('DEBUG', False)
SECRET_KEY = os.environ.get('SECRET_KEY', None)
ALLOWED_HOSTS = []
BROKER_URL = os.environ.get('BROKER_URL', None)
INSTALLED_APPS += [
  "anymail",
]

ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get('MAILGUN_API_KEY', None),
}

EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"
EMAIL_FROM_ADDRESS = 'mail@localhost'

# Database
DATABASES = {
    'default': dj_database_url.config()
}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

