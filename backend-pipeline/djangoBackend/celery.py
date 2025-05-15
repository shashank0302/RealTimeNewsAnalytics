import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoBackend.settings')

# Create the Celery app
app = Celery('djangoBackend')

# Use Django settings for Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'delete-raw-data-hourly': {
        'task': 'api.tasks.delete_old_raw_data',
        'schedule': crontab(minute=0),  # Run every hour at XX:00
    },
    'update-countries-data-hourly': {
        'task': 'api.tasks.fetch_and_process_news',
        'schedule': crontab(minute=30),  # Run every hour at XX:30
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Run tasks on startup
@app.on_after_configure.connect
def setup_initial_tasks(sender, **kwargs):
    # Run once after Celery worker starts
    print("Running initial data fetch task...")
    from api.tasks import fetch_and_process_news
    fetch_and_process_news.delay()
