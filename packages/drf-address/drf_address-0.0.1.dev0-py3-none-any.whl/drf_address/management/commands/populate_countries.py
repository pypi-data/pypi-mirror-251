from django.core.management.base import BaseCommand, CommandError
import json
from pathlib import Path
from ...models import Country

class Command(BaseCommand):
    help = "Populate the countries table in database"
    BASE_DIR = Path(__file__).resolve().parent
    file = BASE_DIR / "countries.json"
    
    def handle(self, *args, **kwargs):
        with open(self.file) as f:
            data = json.load(f)
            countries = [Country(name=country["Name"], code=country["Code"]) for country in data]
            try:
                Country.objects.bulk_create(countries)
            except:
                raise CommandError('Countries already exists')