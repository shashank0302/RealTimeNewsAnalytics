# check_db.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoBackend.settings')
django.setup()

from django.db import connections
from django.db.utils import OperationalError

def check_database_connection():
    db_conn = connections['default']
    try:
        db_conn.cursor()
        print("Database connection is successful.")
    except OperationalError as e:
        print("Database connection failed:", e)

if __name__ == "__main__":
    check_database_connection()
