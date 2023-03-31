from django.contrib.auth.signals import user_logged_in, user_logged_out


def log_user_login(sender, request=None, user=None, **kwargs):
    from ndx_audit_log.utils import log_request
    log_request(request, 'login', user=user)


def log_user_logout(sender, request=None, user=None, **kwargs):
    from ndx_audit_log.utils import log_request
    # This also gets called with AnonymousUser...
    if ((user is not None and user.is_active) or (user is None and request.user.is_active)):
        log_request(request, 'logout', user=user)


def init():
    user_logged_in.connect(log_user_login)
    user_logged_out.connect(log_user_logout)
