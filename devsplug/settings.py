from pathlib import Path
from datetime import timedelta
import os
import dj_database_url



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(qnk(gvaj-8fptz_^n8x-qhlu@objir)x9sfwx+ov64@k3a$*5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]





# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'easy_thumbnails',
    'filer',
    'authentication',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'challenges',
    'taggit',
    'ckeditor',
    'ckeditor_uploader',
    'drf_yasg'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'devsplug.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'devsplug.wsgi.application'


# if not DEBUG:
#     LOGGING = {                                                                                                                 
#         'version': 1,
#         'disable_existing_loggers': False,
#         'handlers': {
#             'logfile': {
#                 'class': 'logging.FileHandler',
#                 'filename': 'server.log',
#             },
#         },
#         'loggers': {
#             'django': {
#                 'handlers': ['logfile'],
#             },
#         },
#     }
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    'default': dj_database_url.config(
        default='postgresql://devsplug_owner:4aqZPVkc7HtD@ep-square-brook-a26fz8ah.eu-central-1.aws.neon.tech/devsplug?sslmode=require',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

token_value="0AybNLpyf_ovzjacoId6xVEuIuEJZ6yqy97Ybnce"
AWS_ACCESS_KEY_ID = "d16c249c4d2455b4d9c9263a01e0a81f"
AWS_SECRET_ACCESS_KEY =  "db3779199dca280f16f748e1fb5994fe5eaffaa5757bd261baee419bf51083c3"
AWS_S3_ENDPOINT_URL = "https://a47b4fa647b5c8c98f04f720c123e23d.r2.cloudflarestorage.com"
AWS_STORAGE_BUCKET_NAME="devsplug"
AWS_S3_SIGNATURE_VERSION = 's3v4'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfilespytho')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#rest framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=14),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS512',
    'SIGNING_KEY': SECRET_KEY,
}



#end rest framework

#django cors configuration

CORS_ALLOW_ALL_ORIGINS = True  


CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]



CORS_ORIGIN_WHITELIST = ["http://localhost:8000","http://127.0.0.1:8000"]

#end django cors configuration


#ckeditor configs 


CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'extraPlugins': ','.join([
            # Add here any extra plugins you need
            'codesnippet',  # For code snippets
            'image2',  # Enhanced image plugin
            'widget',  # Required by image2
            'dialog',  # Required by some plugins like image2
            'clipboard',  # Required for copy-paste
            'lineutils',  # Required for some widgets
            'table',  # For tables
            'tabletools',  # For table tools
            'mathjax',  # For math formulas
        ]),
        'codeSnippet_theme': 'monokai_sublime',
        'extraAllowedContent': 'SyntaxHighlighter[language,style](*);',
    }
}

#end ckeditor

#django filer


THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)


#end django filer

AUTH_USER_MODEL = "authentication.User"