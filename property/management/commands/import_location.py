import csv
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from property.models import Location
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = 'Import locations from a CSV file'

    def add_arguments(self, parser):
        # Define the arguments for the command
        parser.add_argument('csv_file', type=str, help='CSV file containing location data')

    def handle(self, *args, **options):
        # Get the CSV file path
        csv_file = options['csv_file']
        
        # Open and read the CSV file
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)

            # Create a dictionary to keep track of created locations
            locations = {}

            # First pass to create all locations (top-down, parents first)
            for row in reader:
                location_id = row['id']
                location_title = row['title']
                location_type = row['location_type']
                country_code = row['country_code'] if row['country_code'] else 'US'  # Set default for continents
                state_abbr = row['state_abbr'] if row['state_abbr'] else None
                city = row['city'] if row['city'] else None
                parent_location_id = row['parent_location_id'] if row['parent_location_id'] else None

                # Ensure title is not null
                if not location_title:
                    self.stdout.write(self.style.WARNING(f"Location {location_id} skipped due to missing title"))
                    continue

                # If parent_location_id exists, find the parent location
                parent_location = None
                if parent_location_id:
                    try:
                        parent_location = Location.objects.get(id=parent_location_id)
                    except Location.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Parent location with id {parent_location_id} not found. Skipping {location_id}."))
                        continue  # Skip creating this location if parent is not found
                
                # Check if location already exists, if so update, otherwise create a new location
                location, created = Location.objects.update_or_create(
                    id=location_id,
                    defaults={
                        'title': location_title,
                        'location_type': location_type,
                        'country_code': country_code,
                        'state_abbr': state_abbr,
                        'city': city,
                        'parent': parent_location,
                        'center': Point(0, 0)  # Default center, modify later if needed
                    }
                )

                # Log success or failure
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Successfully imported location: {location.title}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Location already exists, updated: {location.title}"))
