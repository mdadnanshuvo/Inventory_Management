from collections import defaultdict
from property.models import Accommodation, LocalizeAccommodation

def partition_accommodation_by_feed():
    accommodations = Accommodation.objects.all()
    partitions = defaultdict(list)
    for accommodation in accommodations:
        partitions[accommodation.feed].append(accommodation)
    return partitions

def partition_localize_accommodation_by_language():
    localizations = LocalizeAccommodation.objects.all()
    partitions = defaultdict(list)
    for localization in localizations:
        partitions[localization.language].append(localization)
    return partitions
