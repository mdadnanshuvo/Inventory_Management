import pytest
from django.test import Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import constants as messages

from property.models import Accommodation, Location
from property.forms import PropertyOwnerSignupForm, AccommodationForm
from property.views import home, property_owner_signup

@pytest.fixture
def client():
    return Client()

@pytest.fixture
@pytest.mark.django_db
def user():
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
@pytest.mark.django_db
def location():
    return Location.objects.create(
        id='test_loc_01', 
        title='Test Location', 
        country_code='US', 
        center='POINT(0 0)',
        location_type='city'
    )

@pytest.fixture
@pytest.mark.django_db
def accommodation(user, location):
    return Accommodation.objects.create(
        user=user,
        location=location,
        title='Test Accommodation',
        country_code='US',
        bedroom_count=2,
        review_score=4.5,
        usd_rate=100.00,
        center='POINT(0 0)',
        images=['http://example.com/image.jpg'],
        amenities=['Wi-Fi', 'Kitchen'],
        published=True
    )

# Views Tests
@pytest.mark.django_db
def test_home_view(client, accommodation):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'properties' in response.context
    assert accommodation in response.context['properties']

@pytest.mark.django_db
def test_property_owner_signup_view(client):
    # Test GET request
    response = client.get(reverse('property_owner_signup'))
    assert response.status_code == 200
    assert 'form' in response.context

    # Test POST request with valid data
    signup_data = {
        'username': 'newowner',
        'email': 'owner@example.com',
        'password1': 'TestPass123!',
        'password2': 'TestPass123!'
    }
    response = client.post(reverse('property_owner_signup'), signup_data)
    
    # Check redirect and user creation
    assert response.status_code == 302  # Redirect after successful signup
    assert User.objects.filter(username='newowner').exists()

# Form Tests
@pytest.mark.django_db
def test_property_owner_signup_form():
    form_data = {
        'username': 'newuser',
        'email': 'test@example.com',
        'password': 'SecurePass123!'
    }
    form = PropertyOwnerSignupForm(data=form_data)
    assert form.is_valid()

    # Test form save method
    user = form.save()
    assert user.username == 'newuser'
    assert user.check_password('SecurePass123!')

@pytest.mark.django_db
def test_accommodation_form(user, location):
    # Test valid form data
    form_data = {
        'title': 'Test Accommodation',
        'country_code': 'US',
        'bedroom_count': 2,
        'review_score': 4.5,
        'usd_rate': 100.00,
        'location': location.id,
        'images': ['http://example.com/image.jpg'],
        'amenities': ['Wi-Fi', 'Kitchen']
    }
    form = AccommodationForm(data=form_data)
    assert form.is_valid()

    # Test image validation
    invalid_image_form = AccommodationForm(data={
        **form_data,
        'images': ['invalid_url']
    })
    assert not invalid_image_form.is_valid()
    assert 'Each image URL must start with' in str(invalid_image_form.errors)

    # Test amenities validation
    invalid_amenities_form = AccommodationForm(data={
        **form_data,
        'amenities': ['A' * 200]
    })
    assert not invalid_amenities_form.is_valid()
    assert 'Each amenity should not exceed 100 characters' in str(invalid_amenities_form.errors)

# Model Tests
@pytest.mark.django_db
def test_accommodation_model(accommodation):
    assert str(accommodation) == 'Test Accommodation'
    assert accommodation.published is True
    assert accommodation.bedroom_count == 2
    assert accommodation.images == ['http://example.com/image.jpg']

# Coverage Configuration
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "django_db: mark test to use django database"
    )