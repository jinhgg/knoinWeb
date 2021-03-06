import datetime
import os, sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7twg$gr7=0pift2%yyeh+!b+1yq13qt9@x$b(*@4)m6%-n)tzd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'users.apps.UserConfig',
    'mngs.apps.MngsConfig',
    'atack.apps.AtackConfig',
    'filemanager.apps.FilemanagerConfig'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'knoin_backend.urls'

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

WSGI_APPLICATION = 'knoin_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'knoin',
    #     'USER': 'ljh',
    #     'PASSWORD': 'Ljh13952010961!',
    #     'HOST': '47.92.147.61',
    #     'PORT': '3306',
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'knoin_platform',
        'USER': 'ljh',
        'PASSWORD': 'lijinhang',
        'HOST': '192.168.3.19',
        'PORT': '3306',
    }
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# ######################################################################### #
# ############################## 以下是自定义配置 ############################ #
# ######################################################################### #

# 这两项是django登录配置，不涉及到drf
AUTH_USER_MODEL = "users.User"
# 支持用户名和手机号两种方式登录
AUTHENTICATION_BACKENDS = ['knoin_backend.utils.auth.UsernameMobileAuthBackend']

# 日志
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
#     'formatters': {  # 日志信息显示的格式
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'handlers': {  # 日志处理方法
#         'console': {  # 向终端中输出日志
#             'level': 'INFO',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'file': {  # 向文件中输出日志
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/knoin.log"),  # 日志文件的位置
#             'maxBytes': 300 * 1024 * 1024,
#             'backupCount': 10,
#             'formatter': 'verbose'
#         },
#     },
#
#
#     'loggers': {  # 日志器
#         'django': {  # 定义了一个名为django的日志器
#             'handlers': ['file'],  # 可以同时向终端与文件中输出日志
#             'propagate': True,  # 是否继续传递日志信息
#             'level': 'INFO',  # 日志器接收的最低日志级别
#         },
#     }
# }

# 跨域设置
CORS_ORIGIN_ALLOW_ALL = True  # 允许所有来源，不用再设置白名单
CORS_ALLOW_CREDENTIALS = True  # 允许带cookie

# jwt认证
JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=15),
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'knoin_backend.utils.auth.jwt_response_payload_handler',
}

# drf
REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'knoin_backend.utils.exceptions.exception_handler',
    # 文档生成
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # 全局认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # jwt 认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 这是个坑，一定要加逗号
        # 'knoin_backend.utils.auth.MyJwtAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    # 'DEFAULT_FILTER_BACKENDS': (
        # 'django_filters.rest_framework.DjangoFilterBackend',
        # 'django_filters.rest_framework.filters.OrderingFilter',
    # ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '50/minute',
        'user': '50/minute'
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10

}
