from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation

# Location Admin
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code', 'state_abbr')

# Accommodation Admin
@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('title', 'usd_rate', 'review_score', 'bedroom_count', 'location', 'published', 'created_at')
    search_fields = ('title', 'location__title', 'country_code', 'state_abbr')
    list_filter = ('location', 'published', 'country_code')

    def get_queryset(self, request):
        """Limit to only properties owned by the logged-in user."""
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='Property Owners').exists():
            # Restrict to properties owned by the logged-in user (use 'user' field)
            return queryset.filter(user=request.user)
        return queryset  # Allow admins to see all properties

    def has_change_permission(self, request, obj=None):
        """Allow property owners to only edit their own properties."""
        if obj and obj.user != request.user:  # Change 'owner' to 'user'
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """Allow property owners to only delete their own properties."""
        if obj and obj.user != request.user:  # Change 'owner' to 'user'
            return False
        return super().has_delete_permission(request, obj)

# LocalizeAccommodation Admin
@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('property', 'language', 'description')
    search_fields = ('property__title', 'language')
