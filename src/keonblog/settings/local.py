# locals.py
import os

## import dotenv module
from dotenv import load_dotenv

## import pahtlib
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from .base import *

# load dotenv variables to env
def get_dotenv():
  env_dir = Path(__file__).resolve().parents[4]
  env_path = Path(env_dir)/'.env'

  if env_path.exists():
    load_dotenv(dotenv_path=env_path)



def get_env_variable(var_name):
    """Get environment variable from os"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f'Set the {var_name} environment variable'
        raise ImproperlyConfigured(error_msg)

def get_json_secret(var_name, secret_file_name):
    """ Get environment variable from json file"""
    with open(secret_file_name) as f:
        secrets = json.loads(f.read())

        try:
            return secrets[var_name]

        except KeyError:
            error_msg = f'Set the {setting} environment variable'
            raise ImproperlyConfigured(error_msg)


get_dotenv()

SECRET_KEY = get_env_variable('SECRET_KEY')
# Debugging Settings only allow True in developing versions
DEBUG = True

# Following os path can be changed later benchmarking twoscoops of django pg98
# In production, we could use different sources to feed cdns, nginx, ...
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

ALLOWED_HOSTS = [
    '.localhost',
    '127.0.0.1',
    '[::1]',
    ]


DATABASES={
   'default':{
      'ENGINE':'django.db.backends.postgresql_psycopg2',
      'NAME': get_env_variable('DB_NAME'),
      'USER': get_env_variable('USER'),
      'PASSWORD': get_env_variable('PASSWORD'),
      'HOST':'localhost',
      'PORT':'5432',
   }
}
