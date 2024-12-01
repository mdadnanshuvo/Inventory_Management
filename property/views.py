from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AccommodationForm
from .models import PropertyOwner, Accommodation, UserProfile

# Home page for listing properties
def home(request):
    properties = Accommodation.objects.all()
    return render(request, 'property/home.html', {'properties': properties})
  

# User sign-up request page
def property_owner_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create UserProfile with a request to become a property owner
            UserProfile.objects.create(user=user, is_property_owner_requested=True)
            
            messages.success(request, "Your request to become a property owner has been submitted. Please wait for admin approval.")
            return redirect('home')  # Redirect to the home page after sign-up
    else:
        form = UserCreationForm()

    return render(request, 'property/property_owner_signup.html', {'form': form})



@login_required
def add_property(request):
    # Ensure the user is an approved property owner
    try:
        property_owner = PropertyOwner.objects.get(user=request.user)
    except PropertyOwner.DoesNotExist:
        messages.error(request, "You are not an approved property owner.")
        return redirect('home')

    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES)  # Don't forget request.FILES for file upload (images)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user  # Assign the logged-in user as the owner
            property_obj.save()
            messages.success(request, "Property added successfully.")
            return redirect('property_detail', pk=property_obj.pk)  # Redirect to the property detail page after successful submission
    else:
        form = AccommodationForm()

    return render(request, 'property/add_property.html', {'form': form})

@login_required
def edit_property(request, pk):
    property_obj = get_object_or_404(Accommodation, pk=pk)

    # Check if the logged-in user is the owner of the property
    if not property_obj.owner or property_obj.owner != request.user:
        messages.error(request, "You are not authorized to edit this property.")
        return redirect('home')

    if request.method == 'POST':
        form = AccommodationForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully.")
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form = AccommodationForm(instance=property_obj)

    return render(request, 'property/edit_property.html', {'form': form, 'property': property_obj})
