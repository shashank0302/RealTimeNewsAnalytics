from celery import shared_task
import logging
from datetime import timedelta
from django.utils import timezone
from .models import RawData
from .ingestion import process_and_store_news, delete_processed_raw_data
from .processing import clean_and_process_data

# TODO: Import your analytics functions here
# from .analytics.sentiment import analyze_sentiment
# from .analytics.summarizer import summarize_text

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


# ==================== ANALYTICS TASKS ====================
# Add your analytics tasks below this line

@shared_task
def analyze_news_sentiment(article_id):
    """
    Example task to analyze sentiment of a news article.
    
    TODO: Implement this with your sentiment analysis logic
    """
    # from .models import NewsData
    # from .analytics.sentiment import analyze_sentiment
    # 
    # article = NewsData.objects.get(id=article_id)
    # sentiment_result = analyze_sentiment(article.description)
    # 
    # # Update the article with sentiment data
    # article.sentiment_score = sentiment_result['polarity']
    # article.sentiment_label = sentiment_result['sentiment']
    # article.save()
    
    pass


@shared_task 
def generate_article_summary(article_id):
    """
    Example task to generate summary of a news article.
    
    TODO: Implement this with your summarization logic
    """
    # from .models import NewsData
    # from .analytics.summarizer import summarize_text
    # 
    # article = NewsData.objects.get(id=article_id)
    # summary = summarize_text(article.description)
    # 
    # # Update the article with summary
    # article.summary = summary
    # article.save()
    
    pass 