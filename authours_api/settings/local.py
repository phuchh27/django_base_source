from .base import *  # noqa
from .base import env
SECRET_KEY = env("DJANGO_SECRET_KEY",
                 default="pNfVXk0s5ei-Dnu8nx0bT871BVs_4Na85V9zVB7qoBg")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]
