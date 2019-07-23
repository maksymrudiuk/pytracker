from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from decouple import config

# Set the default Django Settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pytracker.settings')

app = Celery('pytracker',
             broker=config('CLOUDAMQP_URL'),
             backend=config('CLOUDAMQP_URL'))

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    result_expires=3600,
)
# Load task modules from all registred Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Debug Celery Task"""
    print('Request: {0!r}'.format(self.request))

if __name__ == '__main__':
    app.start()
