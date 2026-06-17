from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

INSTALLED_APPS = [
    'jazzmin',  # must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'storages',
    'portfolio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='portfolio'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='db'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files (WhiteNoise)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    ('assets', BASE_DIR / 'assets'),
]
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
    'default': {
        'BACKEND': 'portfolio.storage.MinIOStorage',
        'OPTIONS': {
            'access_key': config('MINIO_ACCESS_KEY', default='minioadmin'),
            'secret_key': config('MINIO_SECRET_KEY', default='minioadmin'),
            'bucket_name': config('MINIO_BUCKET', default='portfolio'),
            'endpoint_url': config('MINIO_ENDPOINT', default='http://minio:9000'),
            'custom_domain': config('MINIO_PUBLIC_DOMAIN', default=''),
            'secure_urls': config('MINIO_SECURE', default=False, cast=bool),
            'file_overwrite': False,
            'default_acl': 'public-read',
            'querystring_auth': False,
        },
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Jazzmin admin theme
# ---------------------------------------------------------------------------
JAZZMIN_SETTINGS = {
    'site_title': 'Portfolio Admin',
    'site_header': 'Portfolio',
    'site_brand': 'N4d3sh1k4',
    'welcome_sign': 'Добро пожаловать',
    'copyright': 'N4d3sh1k4',
    'search_model': ['portfolio.Project', 'portfolio.Translation'],
    'topmenu_links': [
        {'name': 'Открыть сайт', 'url': '/', 'new_window': True},
    ],
    'show_sidebar': True,
    'navigation_expanded': True,
    'order_with_respect_to': [
        'portfolio',
        'portfolio.SiteSettings',
        'portfolio.Project',
        'portfolio.Translation',
        'auth',
    ],
    'icons': {
        'portfolio.sitesettings': 'fas fa-cog',
        'portfolio.project': 'fas fa-folder-open',
        'portfolio.translation': 'fas fa-language',
        'auth.user': 'fas fa-user',
        'auth.group': 'fas fa-users',
    },
    'default_icon_parents': 'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',
    'related_modal_active': True,
    'show_ui_builder': False,
    'use_google_fonts_cdn': True,
    'changeform_format': 'horizontal_tabs',
}

JAZZMIN_UI_TWEAKS = {
    'navbar': 'navbar-dark',
    'sidebar': 'sidebar-dark-primary',
    'accent': 'accent-primary',
    'brand_colour': 'navbar-primary',
    'theme': 'default',
    'sidebar_nav_compact_style': True,
    'sidebar_nav_flat_style': True,
}
