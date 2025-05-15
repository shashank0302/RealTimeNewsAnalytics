from celery import shared_task
import logging
from datetime import timedelta
from django.utils import timezone
from .models import RawData, ProcessedData, CountryData
from .ingestion import fetch_news_for_countries
from .processing import process_raw_data

# Setup logging
logger = logging.getLogger(__name__)

@shared_task(name="api.tasks.delete_old_raw_data")
def delete_old_raw_data():
    """
    Delete raw data older than 24 hours
    This task runs hourly via Celery Beat
    """
    logger.info("Starting task: delete_old_raw_data")
    
    # Get timestamp for data older than 24 hours
    cutoff_time = timezone.now() - timedelta(hours=24)
    
    # Count items to be deleted
    old_data_count = RawData.objects.filter(timestamp__lt=cutoff_time).count()
    logger.info(f"Found {old_data_count} raw data items older than 24 hours")
    
    # Delete the old data
    deleted_count, _ = RawData.objects.filter(timestamp__lt=cutoff_time).delete()
    
    logger.info(f"Successfully deleted {deleted_count} raw data items")
    return f"Deleted {deleted_count} raw data items"

@shared_task(name="api.tasks.fetch_and_process_news")
def fetch_and_process_news():
    """
    Fetch news for all supported countries and process it
    This task runs hourly via Celery Beat
    """
    logger.info("Starting task: fetch_and_process_news")
    
    # List of country codes to fetch news for
    countries = ["us", "in", "jp", "fr", "gb", "ca", "au", "de"]
    
    total_new_items = 0
    for country in countries:
        try:
            logger.info(f"Fetching news for country: {country}")
            news_items = fetch_news_for_countries(country)
            logger.info(f"Fetched {len(news_items)} news items for {country}")
            total_new_items += len(news_items)
            
            # Process the new data
            processed_count = process_raw_data()
            logger.info(f"Processed {processed_count} new data items for {country}")
        except Exception as e:
            logger.error(f"Error fetching/processing news for {country}: {str(e)}")
    
    logger.info(f"Completed fetch_and_process_news task. Total new items: {total_new_items}")
    return f"Fetched and processed {total_new_items} news items"

@shared_task(name="api.tasks.clean_database")
def clean_database():
    """
    Task to completely clean the database and start fresh
    Run this manually when needed
    """
    logger.info("Starting task: clean_database")
    
    # Count items before deletion
    raw_count = RawData.objects.count()
    processed_count = ProcessedData.objects.count()
    country_count = CountryData.objects.count()
    
    # Delete all data
    RawData.objects.all().delete()
    ProcessedData.objects.all().delete()
    CountryData.objects.all().delete()
    
    logger.info(f"Database cleaned. Deleted {raw_count} raw items, {processed_count} processed items, and {country_count} country items")
    return f"Database cleaned. Deleted {raw_count} raw items, {processed_count} processed items, and {country_count} country items" 