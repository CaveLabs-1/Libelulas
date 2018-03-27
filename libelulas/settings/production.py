from libelulas.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
with open('/etc/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['planlibelula.com','165.227.29.111']


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'libelulas',
        'USER': 'libelula',
        'PASSWORD': '^jFlqoW^Dy$Bg81',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
