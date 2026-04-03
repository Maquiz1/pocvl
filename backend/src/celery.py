import os
from celery import Celery

# set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app = Celery('src')

# load settings from Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto-discover tasks.py in apps
app.autodiscover_tasks()


app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"