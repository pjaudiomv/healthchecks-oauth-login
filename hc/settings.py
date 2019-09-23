"""
Django settings for healthchecks project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings
"""

import os
import warnings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def envbool(s, default):
    v = os.getenv(s, default=default)
    if v not in ("", "True", "False"):
        msg = "Unexpected value %s=%s, use 'True' or 'False'" % (s, v)
        raise Exception(msg)
    return v == "True"


def envint(s, default):
    v = os.getenv(s, default)
    if v == "None":
        return None

    return int(v)


SECRET_KEY = os.getenv("SECRET_KEY", "---")
DEBUG = envbool("DEBUG", "True")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "healthchecks@example.org")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL")
USE_PAYMENTS = envbool("USE_PAYMENTS", "False")
REGISTRATION_OPEN = envbool("REGISTRATION_OPEN", "True")

# these are split so that other things can be inserted dynamically
INSTALLED_APPS_1 = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites',
    "compressor",
    'allauth',
    'allauth.account',
    'allauth.socialaccount'
)
INSTALLED_APPS_2_OAUTH = () # disabled by default
INSTALLED_APPS_3 = (
    "hc.accounts",
    "hc.api",
    "hc.front",
    "hc.payments",
)

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "hc.accounts.middleware.TeamAccessMiddleware",
)

# split so that things can be dynamically inserted or removed later.
AUTHENTICATION_BACKENDS_OAUTH2_1 = () # not enabled by default
AUTHENTICATION_BACKENDS_EMAIL_2 = (
    "hc.accounts.backends.EmailBackend",
)
AUTHENTICATION_BACKENDS_PROFILE_3 = (
    "hc.accounts.backends.ProfileBackend",
)

ROOT_URLCONF = "hc.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "hc.payments.context_processors.payments",
            ]
        },
    }
]

WSGI_APPLICATION = "hc.wsgi.application"
TEST_RUNNER = "hc.api.tests.CustomRunner"


# Default database engine is SQLite. So one can just check out code,
# install requirements.txt and do manage.py runserver and it works
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.getenv("DB_NAME", BASE_DIR + "/hc.sqlite"),
    }
}

# You can switch database engine to postgres or mysql using environment
# variable 'DB'. Travis CI does this.
if os.getenv("DB") == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": os.getenv("DB_HOST", ""),
            "PORT": os.getenv("DB_PORT", ""),
            "NAME": os.getenv("DB_NAME", "hc"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "CONN_MAX_AGE": envint("DB_CONN_MAX_AGE", "0"),
            "TEST": {"CHARSET": "UTF8"},
            "OPTIONS": {
                "sslmode": os.getenv("DB_SSLMODE", "prefer"),
                "target_session_attrs": os.getenv(
                    "DB_TARGET_SESSION_ATTRS", "read-write"
                ),
            },
        }
    }

if os.getenv("DB") == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": os.getenv("DB_HOST", ""),
            "PORT": os.getenv("DB_PORT", ""),
            "NAME": os.getenv("DB_NAME", "hc"),
            "USER": os.getenv("DB_USER", "root"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "TEST": {"CHARSET": "UTF8"},
        }
    }

TIME_ZONE = "UTC"

USE_I18N = False

USE_L10N = False

USE_TZ = True

SITE_ROOT = os.getenv("SITE_ROOT", "http://localhost:8000")
SITE_NAME = os.getenv("SITE_NAME", "Mychecks")
MASTER_BADGE_LABEL = os.getenv("MASTER_BADGE_LABEL", SITE_NAME)
PING_ENDPOINT = os.getenv("PING_ENDPOINT", SITE_ROOT + "/ping/")
PING_EMAIL_DOMAIN = os.getenv("PING_EMAIL_DOMAIN", "localhost")
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static-collected")
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)
COMPRESS_OFFLINE = True
COMPRESS_CSS_HASHING_METHOD = "content"

# Discord integration
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")

# Email integration
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = envint("EMAIL_PORT", "587")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = envbool("EMAIL_USE_TLS", "True")
EMAIL_USE_VERIFICATION = envbool("EMAIL_USE_VERIFICATION", "True")

# Slack integration
SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET")

# Pushover integration
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")
PUSHOVER_SUBSCRIPTION_URL = os.getenv("PUSHOVER_SUBSCRIPTION_URL")
PUSHOVER_EMERGENCY_RETRY_DELAY = int(os.getenv("PUSHOVER_EMERGENCY_RETRY_DELAY", "300"))
PUSHOVER_EMERGENCY_EXPIRATION = int(os.getenv("PUSHOVER_EMERGENCY_EXPIRATION", "86400"))

# Pushbullet integration
PUSHBULLET_CLIENT_ID = os.getenv("PUSHBULLET_CLIENT_ID")
PUSHBULLET_CLIENT_SECRET = os.getenv("PUSHBULLET_CLIENT_SECRET")

# Telegram integration -- override in local_settings.py
TELEGRAM_BOT_NAME = os.getenv("TELEGRAM_BOT_NAME", "ExampleBot")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# SMS and WhatsApp (Twilio) integration
TWILIO_ACCOUNT = os.getenv("TWILIO_ACCOUNT")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_USE_WHATSAPP = envbool("TWILIO_USE_WHATSAPP", "False")

# PagerDuty
PD_VENDOR_KEY = os.getenv("PD_VENDOR_KEY")

# Trello
TRELLO_APP_KEY = os.getenv("TRELLO_APP_KEY")

# Matrix
MATRIX_HOMESERVER = os.getenv("MATRIX_HOMESERVER")
MATRIX_USER_ID = os.getenv("MATRIX_USER_ID")
MATRIX_ACCESS_TOKEN = os.getenv("MATRIX_ACCESS_TOKEN")

# Apprise
APPRISE_ENABLED = envbool("APPRISE_ENABLED", "False")

# Custom OAuth2
CUSTOM_OAUTH2_CLIENT_ID = str(os.getenv("CUSTOM_OAUTH2_CLIENT_ID"))
CUSTOM_OAUTH2_CLIENT_SECRET = str(os.getenv("CUSTOM_OAUTH2_CLIENT_SECRET"))
CUSTOM_OAUTH2_TOKEN_URL = str(os.getenv("CUSTOM_AUTH2_TOKEN_URL"))
CUSTOM_OAUTH2_AUTHORIZE_URL = str(os.getenv("CUSTOM_AUTH2_AUTHORIZE_URL"))
CUSTOM_OAUTH2_ACCOUNT_URL = str(os.getenv("CUSTOM_OAUTH2_ACCOUNT_URL"))
CUSTOM_OAUTH2_DISPLAY_NAME = str(os.getenv("CUSTOM_OAUTH2_DISPLAY_NAME"))
# CSS to put in the link (for images and decoration etc)
CUSTOM_OAUTH2_LINK_CSS = ""

# in local settings add other allauth providers
AUTH_PROVIDERS = ()

# disable local login when oauth in use
OAUTH_DISABLE_LOCAL_LOGIN = envbool("OAUTH_DISABLE_LOCAL_LOGIN", "False")
# disable magic link login when oauth in use
OAUTH_DISABLE_MAGIC_LOGIN = envbool("OAUTH_DISABLE_MAGIC_LOGIN", "False")

#=============================================================================
#=============================================================================
#=============================================================================
# KR customizations, do not contribute these.
#=============================================================================
#=============================================================================
#=============================================================================
# Custom OAuth2
AUTH_PROVIDERS = ('hc.providers.customoauth2',)

KRID_BASE_URL = str(os.getenv("KRID_BASE_URL"))
CUSTOM_OAUTH2_CLIENT_ID = str(os.getenv("CUSTOM_OAUTH2_CLIENT_ID"))
CUSTOM_OAUTH2_CLIENT_SECRET = str(os.getenv("CUSTOM_OAUTH2_CLIENT_SECRET"))
CUSTOM_OAUTH2_TOKEN_URL = KRID_BASE_URL + '/oauth/token' 
CUSTOM_OAUTH2_AUTHORIZE_URL = KRID_BASE_URL + '/oauth/authorize'
CUSTOM_OAUTH2_ACCOUNT_URL = KRID_BASE_URL + '/oauth/user_info'
CUSTOM_OAUTH2_DISPLAY_NAME = "KRID"
CUSTOM_OAUTH2_LINK_CSS = \
"background-image: url(/static/img/kr-btn.png);" + \
"background-position: center;" + \
"background-repeat: no-repeat;" + \
"background-size: 19em;" + \
"color: transparent;" + \
"height: 4.5em;"

# disable email verify for us, we are doing social login. just log in!
ACCOUNT_EMAIL_VERIFICATION = "none"

OAUTH_DISABLE_LOCAL_LOGIN = False
OAUTH_DISABLE_MAGIC_LOGIN = False


#=============================================================================
#=============================================================================

SITE_ID = 1

if os.path.exists(os.path.join(BASE_DIR, "hc/local_settings.py")):
    from .local_settings import *
else:
    warnings.warn("local_settings.py not found, using defaults")

#=============================================================================
#=============================================================================
# Post-Configuration based on settings
#=============================================================================
# for custom oauth, add appropriate apps and authentication backends
if AUTH_PROVIDERS:
    # add desired providers
    INSTALLED_APPS_2_OAUTH += AUTH_PROVIDERS

    # fill this tuple to enable oauth
    AUTHENTICATION_BACKENDS_OAUTH2_1 = (
        "allauth.account.auth_backends.AuthenticationBackend",
    )
    
    # empty these tuples if they are to be disabled.
    if OAUTH_DISABLE_MAGIC_LOGIN:
        AUTHENTICATION_BACKENDS_EMAIL_2 = ()
    if OAUTH_DISABLE_LOCAL_LOGIN:
        AUTHENTICATION_BACKENDS_PROFILE_3 = ()
#=============================================================================
#=============================================================================
#=============================================================================
        
# put apps and authentication backends together    
INSTALLED_APPS = \
    INSTALLED_APPS_1 + \
    INSTALLED_APPS_2_OAUTH + \
    INSTALLED_APPS_3

AUTHENTICATION_BACKENDS = \
    AUTHENTICATION_BACKENDS_OAUTH2_1 + \
    AUTHENTICATION_BACKENDS_EMAIL_2 + \
    AUTHENTICATION_BACKENDS_PROFILE_3
