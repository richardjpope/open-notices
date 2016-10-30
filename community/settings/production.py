import dj_database_url
from community.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', None)

ALLOWED_HOSTS = []

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FROM_ADDRESS = 'mail@localhost'

# # Database
# DATABASES = {
#     'default': dj_database_url.config()
# }

# BROKER_URL = 'redis://localhost:6379/0'