from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def trending_topics(request):
    dummy_data = [
        {"topic": "Stock Market", "category": "Business", "score": 95},
        {"topic": "AI Revolution", "category": "Technology", "score": 89},
        {"topic": "World Cup", "category": "Sports", "score": 78},
    ]
    return Response(dummy_data)

