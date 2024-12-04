from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Location, Accommodation, LocalizeAccommodation
from .utils.partition_utils import partition_accommodation_by_feed, partition_localize_accommodation_by_language
from leaflet.admin import LeafletGeoAdmin  # Import LeafletGeoAdmin

# Location Admin with Leaflet support
@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code', 'state_abbr')

    # Adding Leaflet Map widget for geolocation fields
    settings_overrides = {
        'DEFAULT_CENTER': (0, 0),  # Default map center (latitude, longitude)
        'DEFAULT_ZOOM': 5,        # Default zoom level
    }

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

# Accommodation Admin with Leaflet for geolocation
@admin.register(Accommodation)
class AccommodationAdmin(LeafletGeoAdmin):  # Extend LeafletGeoAdmin
    list_display = ('title', 'usd_rate', 'review_score', 'bedroom_count', 'location', 'published', 'created_at')
    search_fields = ('title', 'location__title', 'country_code')
    list_filter = ('published', 'country_code', UniqueLocationFilter, 'feed')
    actions = ['show_partitioned_by_feed']

    def get_form(self, request, obj=None, **kwargs):
        """
        Customize the admin form based on the user's role.
        - Superusers can see and edit the 'user' field.
        - Property owners won't see the 'user' field in the form.
        """
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            # Remove the 'user' field for non-superusers
            if 'user' in form.base_fields:
                del form.base_fields['user']
        return form

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

    def show_partitioned_by_feed(self, request, queryset):
        """
        Admin action to display partitioned accommodations grouped by feed, with detailed information.
        This partitions all accommodations by their feed and displays them with more details.
        """
        partitions = partition_accommodation_by_feed()  # Apply partitioning to all accommodations
        message = "<ul>"
        for feed, accommodations in partitions.items():
            message += f"<li><b>Feed {feed}:</b><ul>"
            for accommodation in accommodations:
                message += f"<li>{accommodation.title} (ID: {accommodation.id}, Rate: {accommodation.usd_rate}, Location: {accommodation.location.title})</li>"
            message += "</ul></li>"
        message += "</ul>"

        self.message_user(request, format_html(message))
    show_partitioned_by_feed.short_description = "Show accommodations partitioned by feed"

# LocalizeAccommodation Admin (view translations in admin panel)
@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('property', 'language', 'description', 'policy')
    search_fields = ('property__title', 'language')
    actions = ['show_partitioned_by_language']

    # Custom filter for partitioned languages
    class LanguageFilter(admin.SimpleListFilter):
        title = 'Language'
        parameter_name = 'language'

        def lookups(self, request, model_admin):
            # Create a list of available languages based on the partitioned language data
            partitions = partition_localize_accommodation_by_language()
            return [(language, f'Language {language}') for language in partitions.keys()]

        def queryset(self, request, queryset):
            # Filter localizations by language
            if self.value():
                return queryset.filter(language=self.value())
            return queryset

    list_filter = ('language', LanguageFilter)  # Use LanguageFilter for partitioned language filtering

    def show_partitioned_by_language(self, request, queryset):
        """
        Admin action to display partitioned localizations grouped by language, with detailed information.
        This partitions all localizations by their language and displays them with more details.
        """
        partitions = partition_localize_accommodation_by_language()  # Apply partitioning to all localizations
        message = "<ul>"
        for language, localizations in partitions.items():
            message += f"<li><b>Language {language}:</b><ul>"
            for localization in localizations:
                message += f"<li>{localization.property.title} (ID: {localization.property.id}, Description: {localization.description})</li>"
            message += "</ul></li>"
        message += "</ul>"

        self.message_user(request, format_html(message))
    show_partitioned_by_language.short_description = "Show localizations partitioned by language"
