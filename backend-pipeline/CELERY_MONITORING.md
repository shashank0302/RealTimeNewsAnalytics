# Monitoring Celery Tasks and Database Maintenance

This document explains how to monitor your Celery tasks and perform database maintenance for your application.

## Monitoring Celery Tasks

### 1. Checking Logs

Celery logs contain detailed information about task execution. Here's how to access them:

```bash
# View Celery worker logs
tail -f celery.log

# View Celery beat logs
tail -f celerybeat.log
```

### 2. Using Flower Dashboard

[Flower](https://flower.readthedocs.io/en/latest/) is a web-based tool for monitoring Celery tasks:

1. Install Flower:
   ```bash
   pip install flower
   ```

2. Start the Flower server:
   ```bash
   celery -A djangoBackend flower --port=5555
   ```

3. Access the dashboard at `http://localhost:5555`

### 3. Running Tasks Manually

You can trigger tasks manually to test or force data updates:

```python
# In Django shell (python manage.py shell)
from api.tasks import delete_old_raw_data, fetch_and_process_news, clean_database

# Run task to delete old data
result = delete_old_raw_data.delay()
print(f"Task ID: {result.id}")

# Run task to update country news
result = fetch_and_process_news.delay()
print(f"Task ID: {result.id}")

# Check task status
print(f"Task status: {result.status}")
```

## Database Maintenance

### Cleaning the Database

To reset your database and start fresh:

1. Using Django shell:
   ```python
   from api.tasks import clean_database
   
   # Run the clean database task
   result = clean_database.delay()
   print(f"Task started with ID: {result.id}")
   ```

2. Using Django management command (open a terminal in your Django project):
   ```bash
   python manage.py shell -c "from api.tasks import clean_database; clean_database()"
   ```

### Checking Database Status

To check current database statistics:

```python
# In Django shell
from api.models import RawData, ProcessedData, CountryData

# Check counts
raw_count = RawData.objects.count()
processed_count = ProcessedData.objects.count()
country_count = CountryData.objects.count()

print(f"Raw data count: {raw_count}")
print(f"Processed data count: {processed_count}")
print(f"Country data count: {country_count}")
```

## Task Schedule

Your application has the following scheduled tasks:

1. **Delete Old Raw Data**: Runs hourly at XX:00 to remove data older than 24 hours
2. **Update Country News**: Runs hourly at XX:30 to fetch and process new data

## Troubleshooting

If tasks are not running as expected:

1. Check if Celery worker is running:
   ```bash
   ps aux | grep celery
   ```

2. Restart Celery worker:
   ```bash
   # Kill existing worker
   pkill -f celery
   
   # Start new worker
   celery -A djangoBackend worker -l info
   
   # Start celery beat
   celery -A djangoBackend beat -l info
   ```

3. Check Redis connection:
   ```bash
   redis-cli ping
   ```
   Should return `PONG` 