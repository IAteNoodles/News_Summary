from django.core.management.base import BaseCommand
from api.models import Article

class Command(BaseCommand):
    help = 'Deletes all articles from the database'

    def handle(self, *args, **kwargs):
        # This is the core logic of the command.
        # It gets all Article objects and deletes them.
        count, _ = Article.objects.all().delete()
        
        # self.stdout is the proper way to print output in management commands.
        # self.style.SUCCESS makes the text green for better readability.
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} articles.'))
