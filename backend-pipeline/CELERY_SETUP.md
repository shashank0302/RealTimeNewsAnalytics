# Celery and Redis Setup for Automated Tasks

This guide explains how to set up and run the automated tasks for deleting raw data and updating country data every hour.

## Prerequisites

- Redis server installed and running
- All dependencies installed: `pip install celery redis django-celery-beat`

## Configuration

The project has been configured to use Celery with Redis as the message broker. The following scheduled tasks are set:

1. `delete_old_raw_data`: Runs at the start of every hour (XX:00) to delete raw data older than 1 hour
2. `fetch_and_process_news`: Runs at the half-hour mark (XX:30) to fetch fresh country data

## Starting the Workers

To start the Celery workers, follow these steps:

### 1. Start Redis Server

Make sure Redis is running. On Windows, you can start it using:

```
redis-server
```

### 2. Start Celery Worker

Open a terminal in the `backend-pipeline` directory and run:

```
celery -A djangoBackend worker -l info
```

### 3. Start Celery Beat for Scheduled Tasks

In another terminal, run:

```
celery -A djangoBackend beat -l info
```

## Running Tasks Manually

You can also trigger tasks manually from the Django shell:

```python
python manage.py shell

# Then in the shell:
from api.tasks import delete_old_raw_data, fetch_and_process_news
delete_old_raw_data.delay()  # Run the deletion task
fetch_and_process_news.delay()  # Run the fetch and process task
```

## Monitoring

You can monitor Celery tasks using Flower, a web-based tool:

1. Install Flower: `pip install flower`
2. Run Flower: `celery -A djangoBackend flower`
3. Open a browser and go to: `http://localhost:5555`

## Troubleshooting

- If tasks are not running, check if Redis is running and accessible
- Verify that the Celery worker and beat processes are running
- Check the logs for any errors
- Make sure the `CELERY_BROKER_URL` in settings.py points to your Redis instance 