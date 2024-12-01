from django import forms
from django.contrib.auth.models import User
from .models import Accommodation

# Form for property owner signup
class PropertyOwnerSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    # Overriding save method to hash passwords
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user

# Form for adding/editing accommodation
class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        exclude = ['user']  # Exclude 'user' as it will be set in the view

    # Additional validation for the images field
    def clean_images(self):
        images = self.cleaned_data.get('images')
        if not isinstance(images, list):
            raise forms.ValidationError("Images must be a list of URLs.")
        for url in images:
            if not url.startswith(('http://', 'https://')):
                raise forms.ValidationError("Each image URL must start with 'http://' or 'https://'.")
        return images

    # Additional validation for amenities
    def clean_amenities(self):
        amenities = self.cleaned_data.get('amenities')
        if not isinstance(amenities, list):
            raise forms.ValidationError("Amenities must be a list of strings.")
        for amenity in amenities:
            if len(amenity) > 100:
                raise forms.ValidationError("Each amenity should not exceed 100 characters.")
        return amenities
