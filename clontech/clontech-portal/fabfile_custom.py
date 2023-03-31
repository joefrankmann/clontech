import ndx_django_utils.deployment.fabric_base_classes as base 


class ClontechMixin:
    portal_name = 'clontech'


class Shadow(base.Shadow, ClontechMixin):
    pass


class Staging(base.Staging, ClontechMixin):
    portal_name = 'clontech2'


class Prelive(base.Prelive, ClontechMixin):
    host = 'clontech-prelive.novarumcloud.com'


class Live(base.Live, ClontechMixin):
    host = 'clontech-1.novarumcloud.com'
  