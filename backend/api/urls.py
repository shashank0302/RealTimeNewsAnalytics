from django.urls import path
from .views import trending_topics

urlpatterns = [
    path('trending/', trending_topics),
]