from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.property_owner_signup, name='property_owner_signup'),
   
]
