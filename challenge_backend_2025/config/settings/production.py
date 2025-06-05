from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

STATIC_URL = 'static/'

MEDIA_URL = '/media/'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]