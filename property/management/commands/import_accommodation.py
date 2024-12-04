from django.core.exceptions import PermissionDenied
import csv
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from property.models import Accommodation, Location
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = 'Import accommodations from a CSV file'

    def add_arguments(self, parser):
        # Define the arguments for the command
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        csv_file = options['csv_file']

        # Authenticate the user
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                self.stdout.write(self.style.ERROR('Incorrect password'))
                return
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User not found'))
            return

        # Ensure the user is a staff member and a property owner
        if not user.is_staff:
            self.stdout.write(self.style.ERROR('User is not a staff member. Only staff members can import data.'))
            return
        
        # Check if the user is a property owner (assuming this is defined by a custom field or group)
        if not user.groups.filter(name='Property Owners').exists():  # Assuming there's a 'Property Owners' group
            self.stdout.write(self.style.ERROR('User is not a property owner. Only property owners can import data.'))
            return

        # Open the CSV file
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Handle location; if not found, create it
                location_id = row['location']  # Assume 'location' is in the CSV as an ID or name
                location_title = row['location_title']  # Assuming 'location_title' is in your CSV file
                country_code = row['country_code']
                location_type = row['location_type']  # E.g., 'city', 'state', 'country', etc.

                try:
                    location = Location.objects.get(id=location_id)
                except Location.DoesNotExist:
                    # If location doesn't exist, create a new one
                    self.stdout.write(self.style.WARNING(f"Location with id {location_id} not found. Creating new location..."))

                    # Handle center field: Ensure it's correctly formatted as 'latitude,longitude'
                    center_data = row['center'].strip()

                    # Check if center contains both latitude and longitude
                    if ',' in center_data:
                        try:
                            latitude, longitude = map(float, center_data.split(','))
                            center = Point(longitude, latitude)  # Create a valid Point object for GeoDjango
                        except ValueError:
                            self.stdout.write(self.style.ERROR(f"Invalid center format in row: {row}. Skipping this entry."))
                            continue  # Skip this row if center data is invalid
                    else:
                        self.stdout.write(self.style.ERROR(f"Invalid center data (must be 'latitude,longitude') in row: {row}. Skipping this entry."))
                        continue  # Skip if center data is missing or incorrectly formatted

                    # Create the Location object
                    location = Location.objects.create(
                        id=location_id,
                        title=location_title,
                        country_code=country_code,
                        location_type=location_type,
                        center=center
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created new location: {location.title}"))

                # Validate the 'country_code' field: must be 2 characters long
                country_code = country_code.strip().upper()  # Strip any spaces and make it uppercase

                if len(country_code) != 2:
                    self.stdout.write(self.style.ERROR(f"Invalid country code '{country_code}' in row: {row}. Skipping this entry."))
                    continue  # Skip if the country code is not valid

                # Convert 'published' value to boolean
                published = True if row['published'] == 'True' else False

                # Fix images and amenities format
                try:
                    # Clean images and amenities fields
                    images = row['images'].strip()
                    amenities = row['amenities'].strip()

                    # Ensure valid JSON format by fixing quotes and spaces
                    images = images.replace("'", '"')  # Replace single quotes with double quotes
                    amenities = amenities.replace("'", '"')  # Replace single quotes with double quotes

                    # Remove leading/trailing spaces
                    images = images.strip()
                    amenities = amenities.strip()

                    # Validate the format of JSON strings
                    images = json.loads(images)  # This will now work if the format is correct
                    amenities = json.loads(amenities)  # This will now work if the format is correct

                except json.JSONDecodeError:
                    self.stdout.write(self.style.ERROR(f"Invalid JSON format for 'images' or 'amenities' in row: {row}. Skipping this entry."))
                    continue  # Skip this row if JSON is invalid

                # Create and save a new accommodation
                try:
                    accommodation = Accommodation(
                        title=row['title'],
                        country_code=country_code,  # Use validated country code
                        bedroom_count=int(row['bedroom_count']),
                        review_score=float(row['review_score']),
                        usd_rate=float(row['usd_rate']),
                        center=Point(float(row['center'].split(',')[1]), float(row['center'].split(',')[0])),  # Correct geospatial format
                        images=images,
                        amenities=amenities,
                        location=location,  # Use the fetched/created location
                        user=user,
                        published=published,  # Use the boolean value
                        feed=int(row['feed'])  # Ensure feed is an integer
                    )
                    accommodation.save()

                    self.stdout.write(self.style.SUCCESS(f"Successfully added accommodation: {accommodation.title}"))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error adding accommodation: {e}. Skipping this entry."))
                    continue
