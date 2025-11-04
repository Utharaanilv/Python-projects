from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_service, name='book_service'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.view_bookings, name='view_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]