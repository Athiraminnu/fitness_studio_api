from django.shortcuts import redirect

from . import views
from django.urls import path

urlpatterns = [
    path('', lambda request: redirect('classes/')),  # Redirect root to classes/
    path('classes/', views.classes, name='classes'),
    path('book/', views.bookings, name='bookings'), #url for booking a slot
    path('bookings/', views.bookingData, name='bookingdata') #lists the booking details
]