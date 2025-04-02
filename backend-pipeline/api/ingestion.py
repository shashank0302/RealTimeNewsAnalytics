import requests
import logging
from django.conf import settings
from .models import RawData

logger = logging.getLogger(__name__)

def fetch_gnews():
    """
    Fetches the latest business news articles from GNews.
    """
    GNEWS_API_KEY = settings.GNEWS_API_KEY
    url = 'https://gnews.io/api/v4/top-headlines'
    params = {
        'category': 'business',
        'lang': 'en',
        'country': 'us',
        'max': 10,
        'apikey': GNEWS_API_KEY,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('articles', [])
    except requests.RequestException as e:
        logger.error("GNews API error: %s", e)
        return []


def fetch_newsapi():
    """
    Fetches the latest business news articles from NewsAPI.
    """
    NEWSAPI_KEY = settings.NEWSAPI_KEY
    url = 'https://api.thenewsapi.com/v1/news/top'
    params = {
    'api_token': NEWSAPI_KEY,
    'locale': 'us',
    'language': 'en',
    'categories': 'business'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except requests.RequestException as e:
        logger.error("NewsAPI error: %s", e)
        return []

def fetch_all_news():
    """
    Combines articles from GNews and NewsAPI.
    """
    articles = fetch_gnews() + fetch_newsapi()
    return articles

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
        # We are filtering for US news, so we preset the country.
        country = "us"
        # For both APIs, the "source" field might be a dictionary or a string.
        source_info = article.get('source', {})
        if isinstance(source_info, dict):
            source = source_info.get('name', '')
        else:
            source = str(source_info)
        # Use the provided category or default to 'business'
        category = article.get('category', 'business')
        
        # Use get_or_create to avoid duplicates. Here the article is uniquely identified by its title.
        # (You might later choose link as the unique field if your API provides reliable URLs.)
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
            logger.info("Stored new article: %s", title)
        else:
            logger.info("Article already exists: %s", title)
    return stored_articles
