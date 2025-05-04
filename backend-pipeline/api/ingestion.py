import requests
import logging
import feedparser
import time
import random
from datetime import datetime
from django.conf import settings
from .models import RawData
from .processing import normalize_text, clean_and_process_data
from django.utils import timezone

logger = logging.getLogger(__name__)

# Define countries to fetch news from
COUNTRIES = ['us', 'gb', 'in', 'jp', 'fr', 'ca', 'au', 'de']

# Define news categories to fetch
CATEGORIES = ['BUSINESS', 'TECHNOLOGY', 'WORLD', 'NATION', 'SCIENCE', 'ENTERTAINMENT', 'SPORTS', 'HEALTH']

def fetch_google_news_rss(country_code, category=None):
    """
    Fetch news from Google News RSS feeds based on country and optional category.
    
    Args:
        country_code: Two-letter country code (us, gb, in, etc.)
        category: News category (BUSINESS, TECHNOLOGY, etc.) or None for top stories
    
    Returns:
        List of article dictionaries
    """
    articles = []
    country = country_code.lower()
    language = 'en'  # Default to English
    
    # Format URL parameters based on country
    # Some countries need specific language codes
    language_mapping = {'fr': 'fr', 'de': 'de', 'jp': 'ja'}
    hl_param = f"{language_mapping.get(country, language)}-{country.upper()}"
    gl_param = country.upper()
    ceid_param = f"{country.upper()}:{language_mapping.get(country, language)}"
    
    # Build the URL based on whether we want a category or top stories
    if category:
        url = f"https://news.google.com/rss/headlines/section/topic/{category}?hl={hl_param}&gl={gl_param}&ceid={ceid_param}"
    else:
        url = f"https://news.google.com/rss?hl={hl_param}&gl={gl_param}&ceid={ceid_param}"
    
    try:
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:20]:  # Limit to 20 articles per feed
            # Extract the source from the title if possible (Google format: "Title - Source")
            title_parts = entry.title.split(' - ')
            title = title_parts[0] if len(title_parts) > 1 else entry.title
            source = title_parts[-1] if len(title_parts) > 1 else "Google News"
            
            # Parse the published date
            try:
                published_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
            except (ValueError, AttributeError):
                published_date = datetime.now()
            
            articles.append({
                'title': title,
                'description': getattr(entry, 'description', ''),
                'content': getattr(entry, 'content', getattr(entry, 'summary', '')),
                'published_date': published_date.isoformat(),
                'publishedAt': published_date.isoformat(),  # For compatibility
                'source': source,
                'url': entry.link,
                'country': country,
                'category': category.lower() if category else 'general'
            })
        
        logger.info(f"Fetched {len(feed.entries)} Google News RSS articles for {country}, category: {category or 'top stories'}")
    except Exception as e:
        logger.error(f"Error fetching Google News RSS for {country}, {category}: {e}")
    
    return articles

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
        articles = response.json().get('articles', [])
        
        # Tag articles with country
        for article in articles:
            article['country'] = country_code
            
        return articles
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
    
    # Map country codes to locale format
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

def detect_country_from_content(title, content, description):
    """
    Extract country from news text using keyword matching
    """
    country_keywords = {
        'us': ['united states', 'america', 'biden', 'trump', 'washington', 'new york', 'california', 'florida', 'texas', 'dollar', 'usd'],
        'in': ['india', 'mumbai', 'delhi', 'bangalore', 'rupee', '₹', 'crore', 'lakh', 'modi', 'bengaluru', 'hyderabad'],
        'gb': ['uk', 'britain', 'london', 'england', 'british', 'scotland', 'wales', 'pound sterling', 'sunak'],
        'jp': ['japan', 'tokyo', 'yen', 'osaka', 'japanese', 'kyoto'],
        'fr': ['france', 'paris', 'french', 'euro', 'macron', 'lyon', 'marseille'],
        'ca': ['canada', 'toronto', 'vancouver', 'montreal', 'canadian', 'trudeau', 'ottawa'],
        'au': ['australia', 'sydney', 'melbourne', 'australian', 'canberra', 'brisbane'],
        'de': ['germany', 'berlin', 'german', 'euro', 'munich', 'frankfurt', 'hamburg']
    }
    
    combined_text = (f"{title} {description} {content}").lower()
    
    for country_code, keywords in country_keywords.items():
        for keyword in keywords:
            if keyword in combined_text:
                return country_code
    
    return "unknown"

def fetch_all_news():
    """
    Combines articles from all sources for all countries and categories.
    """
    all_articles = []
    
    # 1. Fetch from Google News RSS - first priority
    for country in COUNTRIES:
        # Top stories for each country
        top_stories = fetch_google_news_rss(country)
        all_articles.extend(top_stories)
        
        # Category-specific stories for each country
        for category in CATEGORIES:
            category_stories = fetch_google_news_rss(country, category)
            all_articles.extend(category_stories)
            
            # Add a small delay to avoid overwhelming servers
            time.sleep(0.5)
    
    # 2. Fetch from API sources as backup/additional
    for country in COUNTRIES:
        # Only fetch from APIs if we have fewer than 10 articles for this country
        country_article_count = sum(1 for article in all_articles if article.get('country') == country)
        
        if country_article_count < 10:
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
        published_date = article.get('publishedAt') or article.get('published_date')
        if published_date:
            if isinstance(published_date, str):
                try:
                    # Try parsing ISO format
                    published_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                except ValueError:
                    # Fallback to now if parsing fails
                    published_date = datetime.now()
                    
            # Now make it timezone aware if it's not
            if not timezone.is_aware(published_date):
                published_date = timezone.make_aware(published_date)

        link = article.get('url', '')
        
        # Get country from article or try to detect from content
        country = article.get('country', 'unknown')
        if country == 'unknown':
            country = detect_country_from_content(title, content, description)
        
        # For both APIs, the "source" field might be a dictionary or a string
        source_info = article.get('source', {})
        if isinstance(source_info, dict):
            source = source_info.get('name', '')
        else:
            source = str(source_info)
            
        # Use the provided category or default to 'general'
        category = article.get('category', 'general')
        
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
            logger.info(f"Article already exists: {title}")
            
    return stored_articles

def delete_processed_raw_data(processed_records=None):
    """
    Deletes raw data records that have been processed.
    """
    if processed_records:
        processed_ids = [record.id for record in processed_records]
        deleted_count, _ = RawData.objects.filter(id__in=processed_ids).delete()
    else:
        deleted_count, _ = RawData.objects.all().delete()
    
    logger.info(f"Deleted {deleted_count} raw data records")
    return deleted_count

def fetch_process_and_clean():
    """
    Full pipeline: fetch, process, clean
    """
    # Fetch and store news articles
    stored_articles = process_and_store_news()
    
    # Process the articles (uncomment when ready to use)
    # processed_articles = clean_and_process_data(stored_articles)
    
    # After processing, delete the raw data (uncomment when ready)
    # delete_processed_raw_data(stored_articles)
    
    return stored_articles




# import requests
# import logging
# from django.conf import settings
# from .models import RawData
# import time
# import random
# from .processing import normalize_text, clean_and_process_data

# logger = logging.getLogger(__name__)

# # Define list of countries to fetch news from
# COUNTRIES = ['us', 'gb', 'in', 'jp', 'fr', 'ca', 'au', 'de']  # Add more as needed

# def fetch_gnews_for_country(country_code, retry_count=0, max_retries=3):
#     """
#     Fetches the latest business news articles from GNews for a specific country.
#     """
#     GNEWS_API_KEY = settings.GNEWS_API_KEY
#     url = 'https://gnews.io/api/v4/top-headlines'
#     params = {
#         'category': 'business',
#         'lang': 'en',
#         'country': country_code,
#         'max': 10,
#         'apikey': GNEWS_API_KEY,
#     }

#     try:
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         return response.json().get('articles', [])
#     except requests.exceptions.HTTPError as e:
#         if e.response.status_code == 429 and retry_count < max_retries:
#             # Exponential backoff with jitter
#             sleep_time = (2 ** retry_count) + random.uniform(0, 1)
#             logger.info(f"Rate limited for {country_code}. Retrying in {sleep_time:.2f} seconds")
#             time.sleep(sleep_time)
#             return fetch_gnews_for_country(country_code, retry_count + 1, max_retries)
#         logger.error(f"GNews API error for country {country_code}: {e}")
#         return []


# def fetch_newsapi_for_country(country_code):
#     """
#     Fetches the latest business news articles from NewsAPI for a specific country.
#     """
#     NEWSAPI_KEY = settings.NEWSAPI_KEY
#     url = 'https://api.thenewsapi.com/v1/news/top'
    
#     # Map country codes to locale format if needed
#     # Some APIs use different country code formats
#     locale_mapping = {
#         'us': 'us', 'gb': 'gb', 'in': 'in', 'jp': 'jp', 
#         'fr': 'fr', 'ca': 'ca', 'au': 'au', 'de': 'de'
#     }
    
#     locale = locale_mapping.get(country_code.lower(), country_code)
    
#     params = {
#         'api_token': NEWSAPI_KEY,
#         'locale': locale,
#         'language': 'en',
#         'categories': 'business'
#     }
#     try:
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#         articles = data.get('data', [])
#         # Tag each article with the country code
#         for article in articles:
#             article['country'] = country_code
#         return articles
#     except requests.RequestException as e:
#         logger.error(f"NewsAPI error for country {country_code}: {e}")
#         return []

# def fetch_all_news():
#     """
#     Combines articles from GNews and NewsAPI for all countries.
#     """
#     all_articles = []
    
#     # Fetch from all countries
#     for country in COUNTRIES:
#         gnews_articles = fetch_gnews_for_country(country)
#         newsapi_articles = fetch_newsapi_for_country(country)
        
#         all_articles.extend(gnews_articles)
#         all_articles.extend(newsapi_articles)
        
#         logger.info(f"Fetched {len(gnews_articles)} articles from GNews and {len(newsapi_articles)} articles from NewsAPI for {country}")
    
#     return all_articles

# def process_and_store_news():
#     """
#     Processes and stores fetched articles in the RawData model.
#     Returns a list of stored articles.
#     """
#     articles = fetch_all_news()
#     stored_articles = []
    
#     for article in articles:
#         title = article.get('title')
#         description = article.get('description', '')
#         content = article.get('content', '')
#         published_date = article.get('publishedAt')
#         link = article.get('url', '')
        
#         # Use the country from the article (added in the fetch functions)
#         country = article.get('country', 'unknown')
        
#         # For both APIs, the "source" field might be a dictionary or a string.
#         source_info = article.get('source', {})
#         if isinstance(source_info, dict):
#             source = source_info.get('name', '')
#         else:
#             source = str(source_info)
            
#         # Use the provided category or default to 'business'
#         category = article.get('category', 'business')
        
#         # Use link as unique identifier if available, otherwise use title
#         if link:
#             obj, created = RawData.objects.get_or_create(
#                 link=link,
#                 defaults={
#                     'title': title,
#                     'description': description,
#                     'content': content,
#                     'published_date': published_date,
#                     'source': source,
#                     'category': category,
#                     'country': country,
#                 }
#             )
#         else:
#             obj, created = RawData.objects.get_or_create(
#                 title=title,
#                 defaults={
#                     'description': description,
#                     'content': content,
#                     'published_date': published_date,
#                     'source': source,
#                     'category': category,
#                     'country': country,
#                     'link': link,
#                 }
#             )
            
#         if created:
#             stored_articles.append(obj)
#             logger.info(f"Stored new article: {title} for country {country}")
#         else:
#             logger.info(f"Article already exists: {title} for country {country}")
            
#     return stored_articles

# def delete_processed_raw_data(processed_records=None):
#     """
#     Deletes raw data records that have been processed.
    
#     Args:
#         processed_records: Optional list of RawData objects that were processed.
#                           If None, all RawData objects are deleted.
    
#     Returns:
#         int: Number of records deleted
#     """
#     if processed_records:
#         # Get IDs of processed records
#         processed_ids = [record.id for record in processed_records]
#         # Delete only those specific records
#         deleted_count, _ = RawData.objects.filter(id__in=processed_ids).delete()
#     else:
#         # Delete all raw data
#         deleted_count, _ = RawData.objects.all().delete()
    
#     logger.info(f"Deleted {deleted_count} raw data records")
#     return deleted_count



# # Full pipeline: fetch, process, clean
# def fetch_process_and_clean():
#     # Fetch and store news articles
#     stored_articles = process_and_store_news()
    
#     # Process the articles (call your processing function here)
#     #wprocessed_articles = clean_and_process_data(stored_articles)
    
#     # After processing, delete the raw data
#     #delete_processed_raw_data(stored_articles)
    
#     return stored_articles
