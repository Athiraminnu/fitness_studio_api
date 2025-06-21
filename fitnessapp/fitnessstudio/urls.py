from . import views
from django.urls import path

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('book/', views.bookings, name='bookings'),
    path('bookings/', views.bookingData, name='bookingdata'),
]