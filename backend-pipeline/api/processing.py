import re
import string
import unicodedata
from typing import Optional
from .models import RawData, ProcessedData

def normalize_text(text: Optional[str], is_title: bool = False) -> Optional[str]:
    """
    Normalize text content from news articles.
    
    Parameters:
        text : str or None
            The text to normalize (title, description, or content).
        is_title : bool
            Whether the text is a title (special handling for capitalization).

    Returns:
        str or None
            The normalized text.
    """
    if text is None:
        return None
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)

    # Normalize unicode characters (e.g., convert "café" to "cafe")
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    # Standardize whitespace (remove extra spaces/newlines/tabs)
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove leading/trailing punctuation
    text = text.strip(string.punctuation)

    # Special handling for titles (capitalize properly)
    if is_title:
        words = [word.capitalize() if i == 0 or i == len(text.split()) - 1 else word.lower()
                 for i, word in enumerate(text.split())]
        text = ' '.join(words)

    return text

def clean_and_process_data():
    """
    Process raw data from RawData table and store cleaned versions in ProcessedData.
    Returns a list of newly created processed articles.
    """
    raw_articles = RawData.objects.all()
    
    processed_articles = []
    
    for article in raw_articles:
        # Skip articles that have already been processed (checking by link)
        if article.link and ProcessedData.objects.filter(link=article.link).exists():
            continue
            
        title = normalize_text(article.title, is_title=True)
        description = normalize_text(article.description)
        content = normalize_text(article.content)
        
        # Create entry in ProcessedData table
        obj, created = ProcessedData.objects.get_or_create(
            link=article.link,  # Using link as unique identifier
            defaults={
                'title': title,
                'description': description,
                'content': content,
                'category': article.category,
                'country': article.country,
                'sentiment_score': None,  # Placeholder for sentiment analysis
                'published_date': article.published_date,
                'source': article.source,
                'raw_response': article.raw_response,
            }
        )
        
        if created:
            processed_articles.append(obj)
    
    return processed_articles
