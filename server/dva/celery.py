from __future__ import absolute_import

import os

from celery import Celery
from kombu.common import Broadcast

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dva.settings')

from django.conf import settings  # noqa

app = Celery('dva')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.conf.update(
    CELERYD_PREFETCH_MULTIPLIER=1,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_RESULT_BACKEND='django-db',

)
app.conf.task_queue_max_priority = 10
app.conf.task_queues = (Broadcast('qmanager'),Broadcast('qrefresher'),)
app.conf.task_routes = {
    'manage_host': {'queue': 'qmanager'},
    'refresh_retriever': {'queue': 'qrefresher'},
}
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
