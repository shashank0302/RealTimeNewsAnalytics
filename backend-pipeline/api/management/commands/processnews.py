from django.core.management.base import BaseCommand
from api.processing import clean_and_process_data

class Command(BaseCommand):
    help = "Clean raw data and store it in ProcessedData table"

    def handle(self, *args, **options):
        processed_articles = clean_and_process_data()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully processed {len(processed_articles)} new articles"
            )
        )
        
        # Display sample of processed articles
        if processed_articles:
            self.stdout.write("Sample of processed articles:")
            for article in processed_articles[:3]:
                self.stdout.write(f"- {article.title} ({article.country})")
