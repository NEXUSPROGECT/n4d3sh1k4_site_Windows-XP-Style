from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STORAGES = {
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
    'default': {
        'BACKEND': 'portfolio.storage.MinIOStorage',
        'OPTIONS': {
            'access_key': 'minioadmin',
            'secret_key': 'minioadmin',
            'bucket_name': 'portfolio',
            'endpoint_url': 'http://minio:9000',
            'custom_domain': 'localhost:9000/portfolio',
            'secure_urls': False,
            'file_overwrite': False,
            'default_acl': 'public-read',
            'querystring_auth': False,
        },
    },
}
