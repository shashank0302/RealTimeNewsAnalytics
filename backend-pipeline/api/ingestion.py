import requests
import logging
from django.conf import settings
from .models import RawData
import time
import random
from .processing import normalize_text, clean_and_process_data

logger = logging.getLogger(__name__)

# Define list of countries to fetch news from
COUNTRIES = ['us', 'gb', 'in', 'jp', 'fr', 'ca', 'au', 'de']  # Add more as needed

def fetch_gnews_for_country(country_code, retry_count=0, max_retries=3):
    """
    Fetches the latest business news articles from GNews for a specific country.
    """
    GNEWS_API_KEY = settings.GNEWS_API_KEY
    url = 'https://gnews.io/api/v4/top-headlines'
    params = {
        'category': 'business',
        'lang': 'en',
        'country': country_code,
        'max': 10,
        'apikey': GNEWS_API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get('articles', [])
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429 and retry_count < max_retries:
            # Exponential backoff with jitter
            sleep_time = (2 ** retry_count) + random.uniform(0, 1)
            logger.info(f"Rate limited for {country_code}. Retrying in {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
            return fetch_gnews_for_country(country_code, retry_count + 1, max_retries)
        logger.error(f"GNews API error for country {country_code}: {e}")
        return []


def fetch_newsapi_for_country(country_code):
    """
    Fetches the latest business news articles from NewsAPI for a specific country.
    """
    NEWSAPI_KEY = settings.NEWSAPI_KEY
    url = 'https://api.thenewsapi.com/v1/news/top'
    
    # Map country codes to locale format if needed
    # Some APIs use different country code formats
    locale_mapping = {
        'us': 'us', 'gb': 'gb', 'in': 'in', 'jp': 'jp', 
        'fr': 'fr', 'ca': 'ca', 'au': 'au', 'de': 'de'
    }
    
    locale = locale_mapping.get(country_code.lower(), country_code)
    
    params = {
        'api_token': NEWSAPI_KEY,
        'locale': locale,
        'language': 'en',
        'categories': 'business'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = data.get('data', [])
        # Tag each article with the country code
        for article in articles:
            article['country'] = country_code
        return articles
    except requests.RequestException as e:
        logger.error(f"NewsAPI error for country {country_code}: {e}")
        return []

def fetch_all_news():
    """
    Combines articles from GNews and NewsAPI for all countries.
    """
    all_articles = []
    
    # Fetch from all countries
    for country in COUNTRIES:
        gnews_articles = fetch_gnews_for_country(country)
        newsapi_articles = fetch_newsapi_for_country(country)
        
        all_articles.extend(gnews_articles)
        all_articles.extend(newsapi_articles)
        
        logger.info(f"Fetched {len(gnews_articles)} articles from GNews and {len(newsapi_articles)} articles from NewsAPI for {country}")
    
    return all_articles

def process_and_store_news():
    """
    Processes and stores fetched articles in the RawData model.
    Returns a list of stored articles.
    """
    articles = fetch_all_news()
    stored_articles = []
    
    for article in articles:
        title = article.get('title')
        description = article.get('description', '')
        content = article.get('content', '')
        published_date = article.get('publishedAt')
        link = article.get('url', '')
        
        # Use the country from the article (added in the fetch functions)
        country = article.get('country', 'unknown')
        
        # For both APIs, the "source" field might be a dictionary or a string.
        source_info = article.get('source', {})
        if isinstance(source_info, dict):
            source = source_info.get('name', '')
        else:
            source = str(source_info)
            
        # Use the provided category or default to 'business'
        category = article.get('category', 'business')
        
        # Use link as unique identifier if available, otherwise use title
        if link:
            obj, created = RawData.objects.get_or_create(
                link=link,
                defaults={
                    'title': title,
                    'description': description,
                    'content': content,
                    'published_date': published_date,
                    'source': source,
                    'category': category,
                    'country': country,
                }
            )
        else:
            obj, created = RawData.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'content': content,
                    'published_date': published_date,
                    'source': source,
                    'category': category,
                    'country': country,
                    'link': link,
                }
            )
            
        if created:
            stored_articles.append(obj)
            logger.info(f"Stored new article: {title} for country {country}")
        else:
            logger.info(f"Article already exists: {title} for country {country}")
            
    return stored_articles

def delete_processed_raw_data(processed_records=None):
    """
    Deletes raw data records that have been processed.
    
    Args:
        processed_records: Optional list of RawData objects that were processed.
                          If None, all RawData objects are deleted.
    
    Returns:
        int: Number of records deleted
    """
    if processed_records:
        # Get IDs of processed records
        processed_ids = [record.id for record in processed_records]
        # Delete only those specific records
        deleted_count, _ = RawData.objects.filter(id__in=processed_ids).delete()
    else:
        # Delete all raw data
        deleted_count, _ = RawData.objects.all().delete()
    
    logger.info(f"Deleted {deleted_count} raw data records")
    return deleted_count



# Full pipeline: fetch, process, clean
def fetch_process_and_clean():
    # Fetch and store news articles
    stored_articles = process_and_store_news()
    
    # Process the articles (call your processing function here)
    #wprocessed_articles = clean_and_process_data(stored_articles)
    
    # After processing, delete the raw data
    #delete_processed_raw_data(stored_articles)
    
    return stored_articles
