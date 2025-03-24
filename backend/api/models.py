from django.db import models

# Create your models here.
from django.db import models

class Post(models.Model):
    source = models.CharField(max_length=50)         # e.g., 'twitter', 'reddit'
    post_id = models.CharField(max_length=50)       # Unique ID from the platform
    created_at = models.DateTimeField()             # Timestamp of post creation
    content = models.TextField()                    # Post content (text)
    sentiment_score = models.FloatField(null=True)  # Sentiment analysis score (optional)
    engagement_score = models.FloatField(null=True) # Engagement metrics (likes/upvotes)
    tags = models.JSONField(null=True)              # Hashtags or keywords

class Analytics(models.Model):
    topic = models.CharField(max_length=100)        # Trending topic name
    category = models.CharField(max_length=50)      # e.g., business, sports, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField()                     # Trend score or ranking metric
