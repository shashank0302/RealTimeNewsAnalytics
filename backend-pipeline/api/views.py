# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ProcessedData

@api_view(['GET'])
def country_news(request):
    country_code = request.GET.get('country', '').lower()
    print(f"Country code received: {country_code}")
    #country_code = 'us'
    limit = int(request.GET.get('limit', 10))  # Default to 10 articles
    
    articles = ProcessedData.objects.filter(country=country_code)\
                           .order_by('-published_date')[:limit]
    
    data = [{
        "title": article.title,
        "description": article.description,
        "source": article.source,
        "published_date": article.published_date,
        "link": article.link,
        "sentiment_score": article.sentiment_score
    } for article in articles]
    
    return Response(data)
