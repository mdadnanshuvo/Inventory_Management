# property/admin.py
from django.contrib import admin
from .models import Accommodation, Location, LocalizeAccommodation

class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('title', 'usd_rate', 'review_score', 'bedroom_count', 'location', 'published', 'created_at')  # Correct field names
    search_fields = ('title', 'location__title', 'country_code', 'state_abbr')  # Search by title, location title, etc.
    list_filter = ('location', 'published', 'country_code')  # Filter by location and publication status

class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent_id', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at')  # Correct field names
    search_fields = ('title', 'country_code', 'state_abbr', 'city')  # Search by title, country, state, or city
    list_filter = ('location_type', 'country_code')  # Filter by location type and country

admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(LocalizeAccommodation)  # Register LocalizeAccommodation if needed
