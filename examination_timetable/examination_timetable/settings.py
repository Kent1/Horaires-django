"""
Django settings for examination_timetable project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

SUIT_CONFIG = {
    'ADMIN_NAME': 'Timetable scheduler',
    'MENU_OPEN_FIRST_CHILD': False,
    # Set to empty string if you want to hide search from menu
    'SEARCH_URL': '',
    #'MENU_EXCLUDE': ('timetable.Timetable'),
    'MENU' : (
            {'label'  : 'Scheduler',
             'url'    : '/admin/timetable/timetable/1/',
             'icon'   : 'icon-calendar'},
            {'label'  : 'Databases',
             'url'    : 'timetable.exam',
             'icon'   : 'icon-hdd',
             'models' : ('timetable.exam', 'timetable.professor',
                         'timetable.student', 'timetable.room',
                         'timetable.roomtype', 'timetable.faculty',
                         'timetable.unavailability')},
        )
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't==%mjx+rrewc%))7p$@8*+6_^for3t9vb=je$7*_wh$m_3j@x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'timetable',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'examination_timetable.urls'

WSGI_APPLICATION = 'examination_timetable.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'timetable.MyUser'
