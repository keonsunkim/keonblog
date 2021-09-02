import os

from django.core.exceptions import ImproperlyConfigured

from dotenv import load_dotenv
from .base import *

project_folder = os.path.expanduser('~/dev/KeonBlog')
load_dotenv(os.path.join(project_folder, '.env'))

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

TINYMCE_DEFAULT_CONFIG = {
    # 'height': 360,
    # 'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
    }
