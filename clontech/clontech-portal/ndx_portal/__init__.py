from .celery import app as celery_app
from .signals import init as signals_init

__all__ = ('celery_app',)

signals_init()
