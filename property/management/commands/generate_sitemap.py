from django.core.management.base import BaseCommand
from django.utils.text import slugify
import json
from property.models import Location

class Command(BaseCommand):
    help = "Generate a sitemap.json for all country locations"

    def handle(self, *args, **kwargs):
        """
        Handles the generation of the sitemap.json file by building a location hierarchy
        and writing it to a file.
        """
        # Recursive function to build the location hierarchy
        def build_location_hierarchy(locations, parent=None):
            hierarchy = []
            for location in locations.filter(parent=parent).order_by("title"):
                # Generate the slug for the current location
                slug = "/".join(
                    [slugify(ancestor.title) for ancestor in get_ancestors(location)]
                )
                # Add current location and its nested sublocations
                sublocations = build_location_hierarchy(locations, parent=location)
                location_data = {
                    "name": location.title,
                    "slug": f"https://www.xyz.com/location/{slug}",
                }
                if sublocations:
                    location_data["sublocations"] = sublocations
                hierarchy.append(location_data)
            return hierarchy

        # Helper function to get all ancestors of a location
        def get_ancestors(location):
            ancestors = []
            while location:
                ancestors.insert(0, location)  # Insert at the beginning to maintain order
                location = location.parent
            return ancestors

        # Query all locations and fetch related parent information
        locations = Location.objects.select_related("parent")

        # Group locations by top-level countries
        sitemap = []
        for location in locations.filter(parent__isnull=True).order_by("title"):
            sitemap.append({
                "name": location.title,
                "slug": f"https://www.xyz.com/location/{slugify(location.title)}",
                "sublocations": build_location_hierarchy(locations, parent=location)
            })

        # Write the sitemap to a JSON file
        with open("sitemap.json", "w", encoding="utf-8") as f:
            json.dump(sitemap, f, indent=4, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS("Successfully generated sitemap.json"))
