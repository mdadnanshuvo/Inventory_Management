from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.property_owner_signup, name='property_owner_signup'),
    path('add_property/', views.add_property, name='add_property'),
    path('edit_property/<int:pk>/', views.edit_property, name='edit_property'),
    
]
