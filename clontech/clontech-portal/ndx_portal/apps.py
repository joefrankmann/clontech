from ndx_portal_source.apps import *  # noqa
import ndx_portal_source.apps as source  # noqa


class NdxPortalConfig(source.NdxPortalConfig):
    """AppConfig for the ndx_portal app."""

    name = "clontech_portal"
    verbose_name = "Clontech Portal"