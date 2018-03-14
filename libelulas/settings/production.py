from libelulas.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
with open('/etc/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'plidi-ianroses.c9users.io',
    '127.0.0.1',
    'localhost'
]


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'libelulas',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
