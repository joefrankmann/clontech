"""Portal settings overrides."""
import settings.portal_env_vars  # noqa
from ndx_django_utils.settings.base import *  # noqa
from ndx_django_utils.settings.base import TEMPLATES, INSTALLED_APPS, PIPELINE, REST_FRAMEWORK

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if 'DIRS' not in TEMPLATES[0]:
    TEMPLATES[0]['DIRS'] = []
TEMPLATES[0]['DIRS'] += [os.path.join(BASE_DIR, 'ndx_frontend/templates')]
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'ndx_frontend/static')]

NDX_RESULT_USE_INTERPRETATION = True
NDX_USE_ORGANISATIONS = False

NDX_MOBILE_USER_EMAIL = 'mobile-app@novarumdx.com'

# This setting is only used when creating the mobile app user in a post_migrate signal.
# Others  than that it is not used.
# It is also set to a dummy value in test_overrides.py
NDX_MOBILE_USER_PASSWORD = os.environ.get('NDX_MOBILE_USER_PASSWORD')

NDX_SELECT_ALL = '**SELECT ALL**'
# The list of valid user types for selection in forms. MobileApp is deliberately excluded.
NDX_VALID_USER_TYPES = ['administrators', 'qc user']

NDX_USER_TYPES_ADMIN_GROUP_NAME = 'Normal user'
NDX_AUTH_USER_CREATE_FORM = 'ndx_auth.forms.UserForm'
NDX_AUTH_USER_UPDATE_FORM = 'ndx_auth.forms.UserUpdateForm'

# Default Placeholder value for legacy objects
# NOTE: changing this value will require a new migration
NDX_BLANK_LEGACY_PLACEHOLDER = '-----'

# .save() signal on Batch triggers a celery task, which you may not have on local
# You can set this to False in your local portal settings.
NDX_CREATE_MISSING_DATA_MATRICES_ON_SAVE = True

SITE_PACKAGE = 'ndx357_clontech_portal'
SITE_NAME = os.environ.get('SITE_NAME', 'Clontech Portal')
SITE_LOGO = {'filename': 'img/takara_clontech_logo.png', 'width': 'auto', 'height': '45px'}
SITE_LOGIN_LOGO = {'filename': 'img/takara_clontech_logo.png', 'width': 'auto', 'height': '45px'}

INSTALLED_APPS += ('ndx_batch', 'ndx_feedback')

# We have our own eula app for now, so removing the shadow apps eula js file
PIPELINE['JAVASCRIPT']['main']['source_filenames'] = (
    'vendor/jquery/dist/jquery.min.js',
    'vendor/jquery-ui/dist/jquery-ui.min.js',
    'vendor/bootstrap/dist/js/bootstrap.js',
    'vendor/datatables.net/js/jquery.dataTables.js',
    'vendor/datatables.net-bs/js/dataTables.bootstrap.js',
    'vendor/@babel/polyfill/dist/polyfill.js',
    'js/logger.es6',
    'js/datatables_init.es6',
    'js/date-input-fix.js',
    'ndx_result/js/result_list_csv_export.es6',
)
del PIPELINE['JAVASCRIPT']['show_eula_html']

PIPELINE['JAVASCRIPT']['feedback_csv_export'] = {
    'source_filenames': ('ndx_feedback/js/feedback_csv_export.es6',),
    'output_filename': 'js/pub/feedback_csv_export.js',
    'extra_context': {'defer': True},
}

PIPELINE['JAVASCRIPT']['result_csv_export'] = {
    'source_filenames': ('ndx_result/js/result_csv_export.es6',),
    'output_filename': 'js/pub/result_csv_export.js',
    'extra_context': {'defer': True},
}

PIPELINE['JAVASCRIPT']['eula_size_validation'] = {
    'source_filenames': ('ndx_eula/js/eula_size_validation.es6',),
    'output_filename': 'js/pub/eula_size_validation.js',
    'extra_context': {'defer': True},
}

PIPELINE['STYLESHEETS']['result_csv_export'] = {
    'source_filenames': ('ndx_result/css/result_csv_export.css',),
    'output_filename': 'css/pub/result_csv_export.css',
}

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'rest_framework.authentication.BasicAuthentication',
    'oauth2_provider.contrib.rest_framework.OAuth2Authentication', 
    'rest_framework.authentication.SessionAuthentication'
)
