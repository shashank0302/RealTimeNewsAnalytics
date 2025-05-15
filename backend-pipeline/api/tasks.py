from celery import shared_task
import logging
from datetime import timedelta
from django.utils import timezone
from .models import RawData
from .ingestion import process_and_store_news, delete_processed_raw_data
from .processing import clean_and_process_data

logger = logging.getLogger(__name__)

@shared_task
def delete_old_raw_data():
    """
    Delete raw data older than 1 hour to keep the database clean.
    """
    # Get the cutoff time (1 hour ago)
    cutoff_time = timezone.now() - timedelta(hours=1)
    
    # Delete records older than cutoff_time
    deleted_count, _ = RawData.objects.filter(created_at__lt=cutoff_time).delete()
    
    logger.info(f"Deleted {deleted_count} old raw data records")
    return deleted_count

@shared_task
def fetch_and_process_news():
    """
    Fetch fresh news data, process it, and clean up old raw data.
    This keeps the country data up-to-date.
    """
    # Step 1: Fetch and store new articles
    logger.info("Starting scheduled news fetch and processing")
    stored_articles = process_and_store_news()
    logger.info(f"Fetched and stored {len(stored_articles)} new articles")
    
    # Step 2: Process the raw data into processed data
    processed_articles = clean_and_process_data()
    logger.info(f"Processed {len(processed_articles)} articles")
    
    # Step 3: Clean up raw data that has been processed
    delete_processed_raw_data(stored_articles)
    
    return {
        'fetched': len(stored_articles),
        'processed': len(processed_articles)
    } 