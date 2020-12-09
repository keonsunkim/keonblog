import os

from django.core.exceptions import ImproperlyConfigured

from .base import *

def get_env_variable(var_name):
    """Get environment variable from os"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f'Set the {var_name} environment variable'
        raise ImproperlyConfigured(error_msg)

def get_json_secret(setting, secret_file_name):
    """ Get environment variable from json file"""
    with open(secret_file_name) as f:
        secrets = json.loads(f.read())

        try:
            return secrets[settings]
        except KeyError:
            error_msg = f'Set the {setting} environment variable'
            raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')

# Debugging Settings only allow True in developing versions
DEBUG = True

# Following os path can be changed later benchmarking twoscoops of django pg98
# In production, we could use different sources to feed cdns, nginx, ...
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
