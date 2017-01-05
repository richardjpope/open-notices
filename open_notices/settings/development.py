from open_notices.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't_i39la$p1&q3+e03*v0birx1%lujoy7vnl8!-$h63m$-e$ap2'

ALLOWED_HOSTS = []

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FROM_ADDRESS = 'mail@localhost'
WIKI_URL = 'https://docs.google.com/document/d/1wZfB0Q_fkPJVZ9GS5I4bpZ_NhBYm5DVKpGA7_BojPsY/edit'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'open_notices',
    }
}

INSTALLED_APPS += [
  "sslserver",
]

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'