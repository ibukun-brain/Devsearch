from .base_settings import *
import logging


# THIRD PARTY APPS
INSTALLED_APPS += [
    'debug_toolbar',
    # 'nplusone.ext'

]

# THIRD PARTY MIDDLEWAR
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'nplusone.ext.django.NPlusOneMiddleware'
] 

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = BASE_DIR / 'staticfiles'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# THIRD PARTIES DEBUGGER
INTERNAL_IPS = [
    '127.0.0.1',
]

# NPLUSONE_LOGGER = logging.getLogger('nplusone')
# NPLUSONE_LOG_LEVEL = logging.WARN

# LOGGING = {
#     'version': 1,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'nplusone': {
#             'handlers': ['console'],
#             'level': 'WARN',
#         },
#     },
# }

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '465'
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'jackgriffo49@gmail.com'
EMAIL_HOST_PASSWORD = 'cquxpgmudjimapfp'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = env('EMAIL_PORT')