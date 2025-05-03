# Minimal Django settings for testing xgallery

ROOT_URLCONF="xgallery.urls"

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.auth',  # Required if xgallery uses auth-related models
    'xgallery',  # Your app
    'xblog',
    'easy_thumbnails',
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
MIDDLEWARE = []

# Optional: Minimal template configuration (if xgallery uses templates)
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


