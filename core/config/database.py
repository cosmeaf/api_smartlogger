import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

def get_env_variable(var_name, default=None):
    try:
        return config(var_name)
    except KeyError:
        if default is not None:
            return default
        raise Exception(f"Set the {var_name} environment variable")

DATABASES = {}

DB_ENGINE = get_env_variable('DB_ENGINE', default='sqlite3')

if DB_ENGINE == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
        }
    }
elif DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': get_env_variable('DB_NAME'),
            'USER': get_env_variable('DB_USER'),
            'PASSWORD': get_env_variable('DB_PASSWORD'),
            'HOST': get_env_variable('DB_HOST', default='127.0.0.1'),
            'PORT': get_env_variable('DB_PORT', default='3306'),
        }
    }
elif DB_ENGINE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': get_env_variable('DB_NAME'),
            'USER': get_env_variable('DB_USER'),
            'PASSWORD': get_env_variable('DB_PASSWORD'),
            'HOST': get_env_variable('DB_HOST', default='127.0.0.1'),
            'PORT': get_env_variable('DB_PORT', default='5432'),
        }
    }
elif DB_ENGINE == 'oracle':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.oracle',
            'NAME': get_env_variable('DB_NAME'),
            'USER': get_env_variable('DB_USER'),
            'PASSWORD': get_env_variable('DB_PASSWORD'),
            'HOST': get_env_variable('DB_HOST', default='127.0.0.1'),
            'PORT': get_env_variable('DB_PORT', default='1521'),
        }
    }
else:
    raise ValueError(f"Unsupported DB_ENGINE: {DB_ENGINE}")
