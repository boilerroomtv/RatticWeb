import os
from datetime import timedelta
from urlparse import urljoin

import dj_database_url
import ldap
from django.utils.translation import ugettext_lazy as _
from django_auth_ldap.config import LDAPSearch


def get_env_var(name, default=None, required=False):
    try:
        return os.environ[name]
    except KeyError as e:
        if required:
            raise e
        else:
            return default


ADMINS = ()
MANAGERS = ADMINS

# The Internationalization Settings
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = (
    'conf/locale',
)
LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('de', _('German')),
    ('it', _('Italian')),
)

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# A tuple of callables that are used to populate the context in
# RequestContext. These callables take a request object as their
# argument and return a dictionary of items to be merged into
# the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'ratticweb.context_processors.base_template_reqs',
    'ratticweb.context_processors.logo_selector',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',

    # Custom Middleware
    'account.middleware.StrictAuthentication',
    'account.middleware.PasswordExpirer',
    'ratticweb.middleware.DisableClientSideCachingMiddleware',
    'ratticweb.middleware.XUACompatibleMiddleware',
    'ratticweb.middleware.CSPMiddleware',
    'ratticweb.middleware.HSTSMiddleware',
    'ratticweb.middleware.DisableContentTypeSniffing',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ratticweb.urls'

# URLs
# The subpath Rattic should appear in. Should have a leading and trailing slash.
RATTIC_ROOT_URL = get_env_var('URL_PATH', '/')
MEDIA_URL = urljoin(RATTIC_ROOT_URL, 'media/')
STATIC_URL = urljoin(RATTIC_ROOT_URL, 'static/')

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ratticweb.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

LOCAL_APPS = (
    # Sub apps
    'ratticweb',
    'cred',
    'account',
    'staff',
    'help',
)

INSTALLED_APPS = (
    # External apps
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'user_sessions',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'south',
    'tastypie',
    'kombu.transport.django',
    'djcelery',
    'database_files',
    'social_auth',
) + LOCAL_APPS

if os.environ.get("ENABLE_TESTS") == "1":
    INSTALLED_APPS += ('django_nose', )

TEST_RUNNER = 'tests.runner.ExcludeAppsTestSuiteRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_format': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console_format'
        }
    },
    'loggers': {
        'django_auth_ldap': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': True,
        },
        'db_backup': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

#######################
# Custom app settings #
#######################

# URLs
PUBLIC_HELP_WIKI_BASE = 'https://github.com/tildaslash/RatticWeb/wiki/'
LOGIN_REDIRECT_URL = urljoin(RATTIC_ROOT_URL, "cred/list/")
LOGIN_URL = RATTIC_ROOT_URL

# Set session cookie age (timeout) in seconds.
SESSION_COOKIE_AGE = int(get_env_var('SESSION_COOKIE_TIMEOUT', default=1800))
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_ENGINE = 'user_sessions.backends.db'

# Icon configuration
CRED_ICON_JSON = 'db/icons.json'
CRED_ICON_CSS = 'ratticweb/static/rattic/css/icons.css'
CRED_ICON_SPRITE = 'rattic/img/sprite.png'
CRED_ICON_BASEDIR = 'rattic/img/credicons'
CRED_ICON_CLEAR = 'rattic/img/clear.gif'
CRED_ICON_DEFAULT = 'Key.png'

# django-auth-ldap
AUTH_LDAP_USER_FLAGS_BY_GROUP = {}

# celery
BROKER_URL = 'django://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

# Sets the application to debug mode. Should not be set in production.
DEBUG = get_env_var('DEBUG', default=False)
TEMPLATE_DEBUG = DEBUG

# Setup the loglevel
LOGGING['loggers']['django.request']['level'] = 'DEBUG' if DEBUG else os.getenv('LOG_LEVEL', 'ERROR')

TIME_ZONE = get_env_var('TIME_ZONE', 'UTC')

SECRET_KEY = get_env_var('SECRET_KEY', required=True)

# The hostname that is used to access the RatticDB server.
# To prevent cache poisoning attacks RatticDB will only respond to requests
# that have either localhost or this hostname. Otherwise you will get an error
# 400 Bad Request.
HOSTNAME = get_env_var('VIRTUAL_HOST', 'localhost')
ALLOWED_HOSTS = [HOSTNAME, 'localhost']

# The attachment size limit. Please note that this is set to 2MB to prevent
# performance issues. You can raise this limit, however it may reduce the
# performance of your RatticDB node.
RATTIC_MAX_ATTACHMENT_SIZE = int(get_env_var('MAX_ATTACHMENT_SIZE', default=2097152))

# Kill switch to disable downloading a KeePass files.
# KeePass files stop people from scraping the site or the API and
# encourage them to store them in a secure encrypted format. Turning this off
# may cause them to find other means of keeping passwords for offline use.
RATTIC_DISABLE_EXPORT = bool(get_env_var('DISABLE_KEEPASS_EXPORT', default=False))

# Set to true to make /cred/detail/<cred_id>/fingerprint
# not require a login.
LOGINLESS_SSH_FINGERPRINTS = bool(get_env_var('LOGINLESS_SSH_FINGERPRINTS', default=False))

# Allow SSL termination outside RatticDB
# If this header is present in the request than Django will assume that the
# request is being made over HTTPS. Be VERY careful about setting this. as it
# can compromise the security of your RatticDB Installation. You should only
# set it if all three of the following are true:
#  1. You are running behind a load balancer, or a proxy of some sort.
#  2. You proxy will automatically remove this header if sent from a client.
#  3. The proxy sends this header for SSL secured requests only.
SECURE_PROXY_SSL_HEADER = (os.getenv('SSL_HEADER'), os.getenv('SSL_HEADER_VALUE')) if os.getenv('SSL_HEADER') else None

# [filepaths]
# The on disk location of the help wiki files.
HELP_SYSTEM_FILES = get_env_var('HELP_ROOT', default='help')
# The on disk location of media files (does nothing right now).
MEDIA_ROOT = get_env_var('MEDIA_ROOT', default='media')
# The on disk location of the static files.
STATIC_ROOT = get_env_var('STATIC_ROOT', default='static')

# [database]
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db/ratticdb')
}

# [backup]
BACKUP_DIR = get_env_var('BACKUP_DIR')
BACKUP_GPG_HOME = get_env_var('BACKUP_GPG_HOME')
BACKUP_S3_BUCKET = get_env_var('BACKUP_S3_BUCKET')
BACKUP_RECIPIENTS = get_env_var('BACKUP_RECIPIENTS')

# SMTP Mail Opts
EMAIL_HOST = get_env_var('SMTP_HOST', default='localhost')
EMAIL_PORT = get_env_var('SMTP_PORT', default=25)
EMAIL_HOST_USER = get_env_var('SMTP_USERNAME')
EMAIL_HOST_PASSWORD = get_env_var('SMTP_PASSWORD')
EMAIL_USE_TLS = bool(get_env_var('EMAIL_USE_TLS', default=False))
DEFAULT_FROM_EMAIL = get_env_var('EMAIL_FROM', default=('ratticdb@%s' % HOSTNAME))

# [scheduler]
# The time in days between change queue reminders, zero to disable
CELERYBEAT_SCHEDULE = {}
chgqreminder = int(get_env_var('CHANGE_QUEUE_REMINDER_PERIOD', default=0))
if chgqreminder > 0:
    CELERYBEAT_SCHEDULE['send-change-queue-reminder-email'] = {
        'task': 'cred.tasks.change_queue_emails',
        'schedule': timedelta(days=chgqreminder),
    }
CELERY_TIMEZONE = TIME_ZONE

# [ldap]
LDAP_ENABLED = bool(get_env_var('LDAP_ENABLED', default=False))
USE_LDAP_GROUPS = False

if LDAP_ENABLED:
    LOGGING['loggers']['django_auth_ldap']['level'] = 'DEBUG' if DEBUG else os.getenv('LOG_LEVEL', 'WARNING')

    # Needed if anonymous queries are not allowed
    AUTH_LDAP_BIND_DN = get_env_var('LDAP_BIND_DN')

    AUTH_LDAP_BIND_PASSWORD = get_env_var('LDAP_BIND_PASSWORD')

    # User attributes
    AUTH_LDAP_USER_ATTR_MAP = {"email": "mail"}
    if get_env_var('LDAP_USER_FIRST_NAME'):
        AUTH_LDAP_USER_ATTR_MAP["first_name"] = get_env_var('LDAP_USER_FIRST_NAME')
    if get_env_var('LDAP_USER_LAST_NAME'):
        AUTH_LDAP_USER_ATTR_MAP["LAST_NAME"] = get_env_var('LDAP_USER_LAST_NAME')

    # Are we using LDAP groups or local groups? Default to using LDAP groups
    USE_LDAP_GROUPS = bool(get_env_var('LDAP_GROUPS_ENABLED', True))

    # If we are not using LDAP groups, then do not update the user model's group membership
    AUTH_LDAP_MIRROR_GROUPS = USE_LDAP_GROUPS

    AUTH_LDAP_SERVER_URI = get_env_var('LDAP_URI')

    AUTH_LDAP_USER_BASE = get_env_var('LDAP_USER_BASE')

    # Defaults to AUTH_LDAP_USER_BASE because it must be defined
    AUTH_LDAP_GROUP_BASE = get_env_var('LDAP_GROUP_BASE', default=AUTH_LDAP_USER_BASE)

    AUTH_LDAP_USER_FILTER = get_env_var('LDAP_USER_FILTER')
    # Defaults to a bogus filter so that searching yields no errors in the log
    AUTH_LDAP_GROUP_FILTER = get_env_var('LDAP_GROUP_FILTER', default='(objectClass=_fake)')

    AUTH_LDAP_USER_SEARCH = LDAPSearch(AUTH_LDAP_USER_BASE, ldap.SCOPE_SUBTREE, AUTH_LDAP_USER_FILTER)
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(AUTH_LDAP_GROUP_BASE, ldap.SCOPE_SUBTREE, AUTH_LDAP_GROUP_FILTER)

    # Defaults to PosixGroupType because it must match a pre-defined list of selections
    AUTH_LDAP_GROUP_TYPE = getattr(__import__('django_auth_ldap').config,
                                   get_env_var('LDAP_GROUP_TYPE', 'PosixGroupType'))()

    # Booleans
    AUTH_LDAP_ALLOW_PASSWORD_CHANGE = bool(get_env_var('LDAP_ALLOW_PASSWORD_CHANGE', default=False))

    AUTH_LDAP_START_TLS = bool(get_env_var('LDAP_STARTTLS', default=False))

    AUTH_LDAP_GLOBAL_OPTIONS = {
        ldap.OPT_X_TLS_REQUIRE_CERT: bool(get_env_var('LDAP_REQUIRE_CERT', default=True)),
        ldap.OPT_REFERRALS: bool(get_env_var('LDAP_REFERRALS', False)),
    }

    # Determines which LDAP users are staff, if not defined, privilege can be set manually
    if get_env_var('LDAP_STAFF'):
        AUTH_LDAP_USER_FLAGS_BY_GROUP['is_staff'] = get_env_var('LDAP_STAFF', default='')

    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

# Google Apps authentication
GOAUTH2_ENABLED = bool(get_env_var('GOOGLE_APPS_AUTHENTICATION_ENABLED', default=False))
if GOAUTH2_ENABLED:
    AUTHENTICATION_BACKENDS = (
        'social_auth.backends.google.GoogleOAuth2Backend',
        'django.contrib.auth.backends.ModelBackend',
    )

    LOGIN_URL = RATTIC_ROOT_URL + 'account/login/google-oauth2/'
    LOGIN_ERROR_URL = RATTIC_ROOT_URL + '/account/login-error/'

    SOCIAL_AUTH_RAISE_EXCEPTIONS = False
    SOCIAL_AUTH_PROCESS_EXCEPTIONS = 'social_auth.utils.log_exceptions_to_messages'

    GOOGLE_OAUTH2_CLIENT_ID = get_env_var('GOOGLE_APPS_AUTHENTICATION_CLIENT_ID')
    GOOGLE_OAUTH2_CLIENT_SECRET = get_env_var('GOOGLE_APPS_AUTHENTICATION_CLIENT_SECRET')
    GOOGLE_WHITE_LISTED_DOMAINS = [get_env_var('GOOGLE_APPS_AUTHENTICATION_DOMAIN')]
    SOCIAL_AUTH_REDIRECT_IS_HTTPS = bool(get_env_var('GOOGLE_APPS_AUTHENTICATION_REDIRECT', default=False))

    SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
    SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
    SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

    SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]

    SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


# User Password Expiration
# How often (in days) users must change their password
PASSWORD_EXPIRY = timedelta(days=int(get_env_var('PASSWORD_EXPIRY_DAYS', default=90)))
if GOAUTH2_ENABLED:
    PASSWORD_EXPIRY = False
