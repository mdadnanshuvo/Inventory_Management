from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation

# Location Admin
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code', 'state_abbr')



@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('title', 'usd_rate', 'review_score', 'bedroom_count', 'location', 'published', 'created_at')
    search_fields = ('title', 'location__title', 'country_code', 'state_abbr')
    list_filter = ('location', 'published', 'country_code')

    def get_queryset(self, request):
        """Limit to only properties owned by the logged-in user."""
        queryset = super().get_queryset(request)
        # Check if the user is in the Property Owners group
        if request.user.groups.filter(name='Property Owners').exists():
            # Restrict to properties owned by the logged-in user
            return queryset.filter(owner=request.user)
        return queryset  # Allow admins to see all properties


# LocalizeAccommodation Admin
@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('property', 'language', 'description')
    search_fields = ('property__title', 'language')
