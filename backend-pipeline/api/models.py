from django.db import models
from django.contrib.postgres.fields import JSONField  # For Django 3.1 use models.JSONField


class RawData(models.Model):
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    published_date = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField(null=True, blank=True, unique=True, max_length=2000)  
    created_at = models.DateTimeField(auto_now_add=True)
    raw_response = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title

# Model definition with proper indexing
class ProcessedData(models.Model):
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50)
    country = models.CharField(max_length=50, db_index=True)  # Indexed for fast filtering
    sentiment_score = models.FloatField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True, db_index=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField(null=True, blank=True, unique=True, max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    raw_response = models.JSONField(null=True, blank=True)  # Store raw API response if needed

    class Meta:
        indexes = [
            models.Index(fields=['country', 'category']),  # For common filtering
            models.Index(fields=['country', 'published_date']),  # For timeline queries
        ]

    def __str__(self):
        return f"{self.title} ({self.country})"



class Meta:
    indexes = [
        models.Index(fields=['category']),
        models.Index(fields=['country']),
        models.Index(fields=['published_date']),
    ]


class SampleModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
