# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('news/country/', views.country_news, name='country_news'),
]