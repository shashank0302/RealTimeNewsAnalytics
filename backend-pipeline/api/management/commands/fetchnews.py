from django.core.management.base import BaseCommand
from api.ingestion import process_and_store_news

class Command(BaseCommand):
    help = 'Fetch and store news articles from GNews and NewsAPI'

    def handle(self, *args, **options):
        stored_articles = process_and_store_news()
        self.stdout.write(self.style.SUCCESS(f"Stored {len(stored_articles)} new articles."))
        # Display a sample of the stored data
        for article in stored_articles[:3]:
            self.stdout.write(str({
                "title": article.title,
                "published_date": article.published_date,
                "source": article.source,
                "category": article.category,
                "country": article.country,
                "link": article.link,
            }))
