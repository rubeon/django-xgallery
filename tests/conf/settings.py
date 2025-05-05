# Minimal Django settings for testing xgallery
USE_TZ=True
TIME_ZONE="UTC"
ROOT_URLCONF="tests.conf.urls"
SITE_ID = 1
INSTALLED_APPS = [
    'easy_thumbnails',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'xblog',
    'xgallery',
    'markdown_deux',
    'django_xmlrpc_dx'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # In-memory SQLite for fast tests
    }
}

SECRET_KEY = 'test-secret-key'  # Required but can be any string for tests

# Silence migrations warning during tests
SILENCED_SYSTEM_CHECKS = ['1_7.W001']

# Optional: Disable middleware for faster tests
MIDDLEWARE = [
    #  'django.contrib.auth.context_processors.auth',
    # 'django.contrib.messages.context_processors.messages',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
]

# Optional: Minimal template configuration (if xgallery uses templates)
"""
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
"""
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]
# If xgallery handles file uploads
MEDIA_ROOT = '/tmp/test-media/'
MEDIA_URL = '/media/'


