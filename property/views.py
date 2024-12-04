from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AccommodationForm
from .models import  Accommodation



@login_required
def home(request):
    properties = Accommodation.objects.all()
    return render(request, 'property/home.html', {'properties': properties})


# User sign-up request page
def property_owner_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

           
            
            messages.success(request, "Your request to become a property owner has been submitted. Please wait for admin approval.")
            return redirect('home')  # Redirect to the home page after sign-up
    else:
        form = UserCreationForm()

    return render(request, 'property/property_owner_signup.html', {'form': form})


