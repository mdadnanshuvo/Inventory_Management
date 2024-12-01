# property/migrations/0001_auto_add_permissions.py
from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_property_owner_group(apps, schema_editor):
    # Create the Property Owners group
    group, created = Group.objects.get_or_create(name='Property Owners')
    
    # Get the Accommodation model's content type dynamically
    Accommodation = apps.get_model('property', 'Accommodation')
    content_type = ContentType.objects.get_for_model(Accommodation)
    
    # List the permissions for the Accommodation model
    permissions = [
        'add_accommodation',
        'change_accommodation',
        'view_accommodation',
    ]
    
    # Assign permissions to the group
    for perm_codename in permissions:
        try:
            permission = Permission.objects.get(codename=perm_codename, content_type=content_type)
            group.permissions.add(permission)
        except Permission.DoesNotExist:
            # Handle missing permission (log, skip, or raise an error)
            print(f"Permission {perm_codename} does not exist for content type {content_type}.")
    
    group.save()

def reverse(apps, schema_editor):
    # Remove the Property Owners group and its permissions during migration rollback
    try:
        group = Group.objects.get(name='Property Owners')
        group.permissions.clear()
        group.delete()
    except Group.DoesNotExist:
        print("Group 'Property Owners' does not exist.")

class Migration(migrations.Migration):
    dependencies = [
         ('property', '0001_initial'),
    ]  

    operations = [
        migrations.RunPython(create_property_owner_group, reverse),
    ]
