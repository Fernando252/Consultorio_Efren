"""
Django settings for consultorio project.

Generated by 'django-admin startproject' using Django 3.2.24.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from pathlib import Path
from django.contrib.messages import constants as messages
import os

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#_e3fccne#093b!z1_8%5qusayi3#0f#pj$6$&v21^-9xesu^_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['stdk.pythonanywhere.com', 
                 '127.0.0.8000']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap_datepicker_plus',
    'django_extensions',
    'login',
     #Local App
    'e_mail',
    'components',
    'extra_pages',
    'email_templates',
    'layouts',
    'authentication',


    "crispy_forms",
    'crispy_bootstrap5',

    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'widget_tweaks',
    'imagekit',
    'rest_framework',
     
    
    

]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
   'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Middleware de allauth añadido aquí
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'consultorio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates','/home/stdk/Consultorio_Efren/holamundo/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'consultorio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'consultorio',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stdk$consultorio',
        'USER': 'stdk',
        'PASSWORD': 'consultorio2000',
        'HOST': 'stdk.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_L10N = True

USE_TZ = True

import os

# Otras configuraciones de Django...

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuración de archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
 
]


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

BOOTSTRAP4 = {
    'include_jquery': True,
}
DATE_INPUT_FORMATS = ['%d/%m/%Y']

STATICFILES_FINDERS: {
'djangobower.finders.BowerFinder',
}

BOWER_COMPONENTS_ROOT = 'Users/Jonathan/Documents/git/consultorio_abogados/consultorio'
BOWER_INSTALLED_APPS = (
    'jquery',
    'jquery-ui',
    'bootstrap'
)

NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
    '--port', '8888',
]
IPYTHON_KERNEL_DISPLAY_NAME = 'Django Kernel'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
    
# Otras configuraciones de allauth (opcional)
# Puedes personalizar el comportamiento con las siguientes opciones:
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
STATIC_ROOT = os.path.join(BASE_DIR,'static/assets')


#  All Auth Configurations
LOGIN_REDIRECT_URL = "/accounts/profile/"
LOGIN_URL = "account_login"
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS =True

# social Additional configuration settings
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET = True

#  All auth form customaization
ACCOUNT_FORMS = {
    "login": "consultorio.forms.UserLoginForm",
    "signup": "consultorio.forms.UserRegistrationForm",
    "change_password": "consultorio.forms.PasswordChangeForm",
    "set_password": "consultorio.forms.PasswordSetForm",
    "reset_password": "consultorio.forms.PasswordResetForm",
    "reset_password_from_key": "consultorio.forms.PasswordResetKeyForm",
    
}
# SMTP Configure
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "jonathan.cayo12@gmail.com"
EMAIL_HOST_PASSWORD = "wevsyskcswflekxz"
DEFAULT_FROM_EMAIL = "jonathan.cayo12@gmail.com"


SITE_ID = 1

# Provider Configurations
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': 
        {
            'client_id': '556542475411-atai04oepna72lf526enbkq3b5d6sod1.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# client id = '556542475411-atai04oepna72lf526enbkq3b5d6sod1.apps.googleusercontent.com'
# client secret = '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'