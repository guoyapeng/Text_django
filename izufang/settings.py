"""
Django settings for izufang project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sk70$(kqz4n)96)^ua#unt7oam9#*2@$bj13rv+@m*@tt%=et@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'debug_toolbar',
    'api',
    'common'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'izufang.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'izufang.wsgi.application'


# DRF配置
REST_FRAMEWORK = {
    # 分页配置
    'PAGE_SIZE': 3,                                             # 配置默认每页加载的数据量三条
    'DEFAULT_PAGINATION_CLASS': 'api.helper.CustomPagination',  # 配置分页类。指定自定义分页类

    # 限流配置
    'DEFAULT_THROTTLE_CLASSES': (                      # 默认限流类
        'rest_framework.throttling.AnonRateThrottle',  # 匿名游客限流类
        'rest_framework.throttling.UserRateThrottle',  # 登陆用户限流类
    ),
    'DEFAULT_THROTTLE_RATES': {     # 默认限流速率
        'anon': '30/min',           # 匿名游客访问限制。每分钟30次
        'user': '10000/day',        # 登陆用户访问限制。每天10000
    }

}


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zufang',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '123456',
        'CHARSET': 'utf8',
        'TIME_ZONE': 'Asia/Shanghai',
    },
}

# 缓存库配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            'redis://127.0.0.1:6379/0',
        ],
        'KEY_PREFIX': 'izufang',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 2048,
            },
        }
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# 调试工具栏
DEBUG_TOOLBAR_CONFIG = {  # debug_toolbar
    # 引入jquery库
    'JQUERY_URL': 'https://cdn.bootcss.com/jquery/3.4.1/jquery.min.js',
    'SHOW_COLLAPSED': True,  # 工具栏是否折叠
    'SHOW_TOOLBAR_CALLBACK': lambda x: True,  # 是否显示工具栏
}
