#!/bin/bash
set -e

echo "Apply database migrations"
python manage.py migrate

echo "Triggering initial news data fetch in background"
python manage.py shell -c "
from api.tasks import fetch_and_process_news
import threading
threading.Thread(target=fetch_and_process_news).start()
print('News fetch triggered in background - continuing startup')
"

echo "Starting Django server"
python manage.py runserver 0.0.0.0:8000 