from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db import models as geomodels
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Validators
def validate_country_code(value):
    if len(value) != 2 or not value.isalpha():
        raise ValidationError("Country code must be a valid 2-letter ISO code.")

def validate_image_urls(value):
    if not isinstance(value, list):
        raise ValidationError("Images must be a list of URLs.")
    for url in value:
        if len(url) > 300:
            raise ValidationError(f"Image URL '{url}' exceeds 300 characters.")

def validate_amenities(value):
    if not isinstance(value, list):
        raise ValidationError("Amenities must be a list of strings.")
    for amenity in value:
        if len(amenity) > 100:
            raise ValidationError(f"Amenity '{amenity}' exceeds 100 characters.")

# Location Model
class Location(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)  # Required
    center = geomodels.PointField()  # Geospatial field
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE
    )  # Hierarchical location nesting
    location_type = models.CharField(max_length=20)  # e.g., continent, country, state, city
    country_code = models.CharField(max_length=2, validators=[validate_country_code])
    state_abbr = models.CharField(max_length=3, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Accommodation Model
class Accommodation(models.Model):
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=100)  # Required
    country_code = models.CharField(
        max_length=2, validators=[validate_country_code]
    )  # ISO country code
    bedroom_count = models.PositiveIntegerField()
    review_score = models.DecimalField(
        max_digits=3, decimal_places=1, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    center = geomodels.PointField()  # Geospatial field
    images = models.JSONField(default=list, validators=[validate_image_urls])
    amenities = models.JSONField(default=list, validators=[validate_amenities])
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='accommodations'
    )
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['country_code']),
            models.Index(fields=['review_score']),
            models.Index(fields=['published']),
        ]
        ordering = ['-created_at']
        
# LocalizeAccommodation Model
class LocalizeAccommodation(models.Model):
    property = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    language = models.CharField(max_length=2)  # Language code
    description = models.TextField()
    policy = models.JSONField(default=dict)  # e.g., {"pet_policy": "value"}

    def __str__(self):
        return f"{self.property.title} - {self.language}"

# UserProfile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_property_owner_requested = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# PropertyOwner Model
class PropertyOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    approved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# Signal to Manage PropertyOwner Group
@receiver(post_save, sender=PropertyOwner)
def add_to_property_owners_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Property Owners')
        instance.user.groups.add(group)
        instance.user.save()
