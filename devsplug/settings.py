import os
from pathlib import Path
from datetime import timedelta
import sys
from dotenv import load_dotenv
import logging.handlers

# Load environment variables
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY SETTINGS
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# APPLICATIONS
INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'easy_thumbnails',
    'filer',
    'authentication',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'challenges',
    'taggit',
    'drf_spectacular',
    'django_crontab',
    'django_extensions',  # Django Extensions
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.gitlab',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'devsplug.middleware.SchemaErrorMiddleware',
]

# URL CONFIGURATION
ROOT_URLCONF = 'devsplug.urls'

# TEMPLATES CONFIGURATION
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

# WSGI CONFIGURATION
WSGI_APPLICATION = 'devsplug.wsgi.application'

# DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# AUTHENTICATION CONFIGURATION
AUTH_USER_MODEL = "authentication.User"

# PASSWORD VALIDATORS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC & MEDIA FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Ensure WhiteNoise is properly configured
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Create required directories
os.makedirs(os.path.join(BASE_DIR, 'static'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'staticfiles'), exist_ok=True)

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STORAGE CONFIGURATION
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_VERSION = os.getenv('AWS_S3_SIGNATURE_VERSION')

# Single consolidated LOGGING configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'gunicorn': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.request': {  # Captures 500 errors
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {  # Captures 500 errors
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'gunicorn.error': {
            'handlers': ['gunicorn'],
            'level': 'ERROR',
            'propagate': True,
        },
        'gunicorn.access': {
            'handlers': ['gunicorn'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

# For production (when DEBUG is False)
if not DEBUG:
    # Add file handler for production
    LOGGING['handlers']['file'] = {
        'class': 'logging.FileHandler',
        'filename': '/var/log/django-error.log',  # Make sure this path is writable
        'formatter': 'verbose',
    }
    # Add file handler to all loggers
    for logger in LOGGING['loggers'].values():
        logger['handlers'] = ['console', 'file']

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# JWT CONFIGURATION
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=14),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS512',
    'SIGNING_KEY': SECRET_KEY,
}

# CORS CONFIGURATION
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_ORIGIN_WHITELIST = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# FILER CONFIGURATION
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

# CRON JOBS
CRONJOBS = [
    ("*/1 * * * *", "authentication.jobs.increase_score")
]

# EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# DEFAULT PRIMARY KEY FIELD TYPE
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Test settings
if 'test' in sys.argv:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.test.sqlite3',
        }
    }
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]
    # Disable migrations during tests
    class DisableMigrations:
        def __contains__(self, item):
            return True
        def __getitem__(self, item):
            return None
    MIGRATION_MODULES = DisableMigrations()

# Add Unfold settings
UNFOLD = {
    "SITE_TITLE": "Devsplug Admin",
    "SITE_HEADER": "Devsplug",
    "SITE_URL": "/",
    "SITE_ICON": None,  # path to icon file (e.g. 'path/to/icon.png')
    "DASHBOARD_CALLBACK": None,
    "STYLES": [],
    "SCRIPTS": [],
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "EXTENSIONS": {
        "modals": True,
    },
}

TEST_RUNNER = "devsplug.test_runner.CustomTestRunner"

# Add this near the email configuration:
if DEBUG or 'test' in sys.argv:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # Enable logging for emails
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.core.mail': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }

# Email logging for non-test environment
if not 'test' in sys.argv:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.core.mail': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

# Remove all duplicate configurations and keep only these OAuth2 and social auth settings

# OAuth2 Provider Settings
OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
    },
    'ACCESS_TOKEN_EXPIRE_SECONDS': 36000,
    'OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL': 'oauth2_provider.AccessToken',
    'OAUTH2_PROVIDER_APPLICATION_MODEL': 'oauth2_provider.Application',
    'OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL': 'oauth2_provider.RefreshToken',
    'OAUTH2_PROVIDER_GRANT_MODEL': 'oauth2_provider.Grant',
    'OAUTH2_PROVIDER_ID_TOKEN_MODEL': 'oauth2_provider.IDToken',
}

# Single Authentication Backends Configuration
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.gitlab.GitLabOAuth2',
    'oauth2_provider.backends.OAuth2Backend',
)

# Social Auth Settings
SOCIAL_AUTH_GITHUB_KEY = os.getenv('GITHUB_CLIENT_ID')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'prompt': 'select_account'
}

SOCIAL_AUTH_GITLAB_KEY = os.getenv('GITLAB_CLIENT_ID')
SOCIAL_AUTH_GITLAB_SECRET = os.getenv('GITLAB_CLIENT_SECRET')
SOCIAL_AUTH_GITLAB_SCOPE = ['read_user']

# Django AllAuth Settings
SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
ACCOUNT_LOGIN_METHODS = {'username'}
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_STORE_TOKENS = False
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

# URL Settings
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'http://localhost:3000'
ACCOUNT_LOGOUT_REDIRECT_URL = 'http://localhost:3000'

# Single Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'authentication': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'social_core': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# Social Auth Pipeline
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Create static directory if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, 'static'), exist_ok=True)

# Ensure the static directory exists
os.makedirs(os.path.join(BASE_DIR, 'staticfiles'), exist_ok=True)

# Email logging for non-test environment
if not 'test' in sys.argv:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.core.mail': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

# Set the SITE_ID for django.contrib.sites
SITE_ID = 1

# django-allauth settings
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

# Add OAuth2 URLs
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'

# Update Google OAuth settings
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'prompt': 'select_account',
    'hd': 'example.com'  # If you need to restrict to specific domains
}

# Update the URL namespace
DRFSO2_URL_NAMESPACE = 'oauth2_provider'

# Update authentication backends order
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.gitlab.GitLabOAuth2',
    'oauth2_provider.backends.OAuth2Backend',
)

# Add OAuth2 URLs
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'

# Add this to your settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'authentication': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'social_core': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Update Google OAuth settings
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'prompt': 'select_account',
    'hd': 'example.com'  # If you need to restrict to specific domains
}

# Email Verification Settings
EMAIL_VERIFICATION_TIMEOUT = 48 * 3600  # 48 hours in seconds
PASSWORD_RESET_TIMEOUT = 24 * 3600  # 24 hours in seconds

# Site URL for email links
SITE_URL = os.getenv('SITE_URL', 'https://devsplug.com')

# Email Template Settings
EMAIL_TEMPLATE_DIR = os.path.join(BASE_DIR, 'authentication/templates/emails')

# Update email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'Devsplug <noreply@devsplug.com>'

# Django Extensions Settings
SHELL_PLUS = "ipython"

SHELL_PLUS_PRINT_SQL = True

SHELL_PLUS_IMPORTS = [
    'from django.core.cache import cache',
    'from django.conf import settings',
    'from django.contrib.auth.models import User',
    'from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When',
    'from django.utils import timezone',
]

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

# Notebook settings for Django Extensions
NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
    '--port', '8888',
    '--allow-root',
    '--no-browser',
]

# Django Extensions settings for URL command
SHELL_PLUS_MODEL_ALIASES = {
    'auth': {
        'User': 'U',
    },
}

# Logging configuration for Django Extensions
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django_extensions': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        },
    }

# Add drf_spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Devsplug API',
    'DESCRIPTION': 'Devsplug API documentation',
    'VERSION': 'v1',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'CONTACT': {
        'name': 'Devsplug Team',
        'email': 'info@devsplug.com',
    },
    # Optional UI settings
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
    },
    # Optional: Control which auth methods to show in the docs
    'SECURITY': [
        {
            'Bearer': [],
        }
    ],
    # Add this to fix the 500 error
    'SERVE_AUTHENTICATION': None,
    'SCHEMA_PATH_PREFIX': '/api/',
}

# Add this setting
JWT_AUTH_COOKIE = 'jwt-auth'
