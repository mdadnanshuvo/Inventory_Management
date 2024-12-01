from django.core.management.base import BaseCommand
from django.utils.text import slugify
import json
from property.models import Location


class Command(BaseCommand):
    help = "Generate a sitemap.json for all country locations"

    def handle(self, *args, **kwargs):
        # Recursive function to build the location hierarchy
        def build_location_hierarchy(locations, parent=None):
            hierarchy = []
            for location in locations.filter(parent=parent).order_by("title"):
                # Generate the slug for the current location
                slug = "/".join(
                    [slugify(ancestor.title) for ancestor in get_ancestors(location)]
                )
                # Add current location and its nested sublocations
                location_data = {
                    location.title: f"https://www.xyz.com/location/{slug}"
                }
                sublocations = build_location_hierarchy(locations, parent=location)
                if sublocations:
                    location_data["sublocations"] = sublocations
                hierarchy.append(location_data)
            return hierarchy

        # Helper function to get all ancestors of a location
        def get_ancestors(location):
            ancestors = []
            while location:
                ancestors.insert(0, location)
                location = location.parent
            return ancestors

        # Query all locations
        locations = Location.objects.select_related("parent")

        # Group locations by top-level countries
        countries = []
        for location in locations.filter(parent__isnull=True):  # Top-level countries
            country_name = location.title
            country_code = slugify(location.country_code)
            country_data = {
                country_name: country_code,
                "locations": build_location_hierarchy(locations, parent=location),
            }
            countries.append(country_data)

        # Sort countries alphabetically
        sitemap = sorted(countries, key=lambda x: list(x.keys())[0].lower())

        # Write to sitemap.json
        with open("sitemap.json", "w") as f:
            json.dump(sitemap, f, indent=4)

        self.stdout.write(self.style.SUCCESS("Successfully generated sitemap.json"))
