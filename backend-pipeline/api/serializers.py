"""
API Serializers
===============

Django REST Framework serializers for API data transformation.
"""

from rest_framework import serializers
from .models import NewsData


class NewsDataSerializer(serializers.ModelSerializer):
    """
    Serializer for NewsData model.
    Handles conversion between model instances and JSON.
    """
    
    class Meta:
        model = NewsData
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class NewsAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for NewsData with analytics fields.
    Use this when returning analyzed news data.
    """
    # Add custom analytics fields here when implemented
    # sentiment_score = serializers.FloatField(read_only=True)
    # sentiment_label = serializers.CharField(read_only=True)
    # summary = serializers.CharField(read_only=True)
    
    class Meta:
        model = NewsData
        fields = [
            'id', 'title', 'description', 'url', 'source', 
            'country', 'category', 'published_at',
            # Add analytics fields here
            # 'sentiment_score', 'sentiment_label', 'summary'
        ]


class CountryNewsSerializer(serializers.Serializer):
    """
    Serializer for country-grouped news data.
    """
    country = serializers.CharField()
    news_count = serializers.IntegerField()
    latest_update = serializers.DateTimeField()
    articles = NewsDataSerializer(many=True, read_only=True)


class NewsFilterSerializer(serializers.Serializer):
    """
    Serializer for news filtering parameters.
    """
    country = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    source = serializers.CharField(required=False)
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    limit = serializers.IntegerField(default=50, max_value=200) 