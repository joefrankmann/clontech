import os
import sys

from celery import Celery
import envdir


if 'SECRET_KEY' not in os.environ:
    if 'test' in sys.argv:
        envdir.open(os.path.join(os.path.dirname(__file__), '..', 'testing', 'envdir'))
    elif 'ENVDIR' in os.environ:
        envdir.open(os.environ['ENVDIR'])
    else:
        envdir.open(os.path.join(os.path.dirname(__file__), '..', 'envdir'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.portal_settings")

app = Celery('ndx_portal')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
