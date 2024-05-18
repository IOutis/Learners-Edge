from __future__ import absolute_import,unicode_literals
from celery.schedules import crontab
import os
from celery import Celery
from django.conf import settings
from django.contrib.auth import get_user

os.environ.setdefault('DJANGO_SETTINGS_MODULE','FirstSite.settings')

app = Celery('FirstSite')

app.conf.enable_utc = True
app.conf.update(timezone='Asia/Kolkata')  

# app.conf.update(enable_utc=False,timezone='Asia/Kolkata',)
app.config_from_object(settings,namespace='CELERY')




#CELERY BEATS SETTINGS HERE
app.conf.beat_schedule={
    'every-5-seconds': {
        'task': 'notifications_app.tasks.process_timetable_deadlines',
        'schedule': 10.0,
        # 'args': ('mdmus',), 
}
}


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


