"""Context processors for the portal."""
import pkg_resources

from django.conf import settings

_version = None


def site_settings(request):
    """Context processor that adds some site settings."""
    return {
        'site_title': settings.SITE_NAME,
        'site_logo': settings.SITE_LOGO,
        'site_login_logo': settings.SITE_LOGIN_LOGO,
    }


def version(request):
    """Context processor that adds the portal version."""
    global _version
    if _version is None:
        _version = pkg_resources.require('ndx357_clontech_portal')[0].version
    return {
        'version': _version,
    }


def site_env(request):
    """Context processor that adds the site environment (Staging, Prelive, Live)."""
    return {'site_env': settings.SITE_ENV}
