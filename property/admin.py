from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation
from django.db.models import Count

# Location Admin (no change here)
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code', 'state_abbr')

# Custom Location Filter to avoid duplicate locations in the filter dropdown
class UniqueLocationFilter(admin.SimpleListFilter):
    title = 'location'  # Title for the filter
    parameter_name = 'location'

    def lookups(self, request, model_admin):
        # Get unique locations
        locations = Location.objects.annotate(accommodation_count=Count('accommodation')).filter(accommodation_count__gt=0)
        return [(location.id, location.title) for location in locations]

    def queryset(self, request, queryset):
        # Filter accommodations by location
        if self.value():
            return queryset.filter(location__id=self.value())
        return queryset

# Accommodation Admin
@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('title', 'usd_rate', 'review_score', 'bedroom_count', 'location', 'published', 'created_at')
    search_fields = ('title', 'location__title', 'country_code')  # Removed duplicate search fields
    list_filter = ('published', 'country_code', UniqueLocationFilter)  # Use custom location filter

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        if request.user.groups.filter(name='Property Owners').exists():
            return queryset.filter(user=request.user)
        return queryset.none()  # Default: No access for other users

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.user != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.user != request.user:
            return False
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Hide the 'user' field from Property Owners in the admin panel.
        Property owners should not be able to see the list of users in the dropdown.
        """
        if db_field.name == 'user' and not request.user.is_superuser:
            kwargs['queryset'] = request.user.__class__.objects.none()  # Return no users for Property Owners
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# LocalizeAccommodation Admin (view translations in admin panel)
@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('property', 'language', 'description', 'policy')
    search_fields = ('property__title', 'language')
