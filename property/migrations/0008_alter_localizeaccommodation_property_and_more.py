# Generated by Django 5.1.3 on 2024-12-03 04:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_remove_userprofile_user_delete_propertyowner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localizeaccommodation',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='localizations', to='property.accommodation'),
        ),
        migrations.AlterUniqueTogether(
            name='localizeaccommodation',
            unique_together={('property', 'language')},
        ),
    ]
