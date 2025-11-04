from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookingForm
from .models import Booking
from django.shortcuts import get_object_or_404

@login_required
def book_service(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            #  Dummy payment amount 
            booking.amount = 500.00  
            booking.payment_status = 'Paid'  # Simulating payment success
            booking.save()
            messages.success(request, 'Your booking has been placed successfully!')
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'bookings/book_service.html', {'form': form})

def booking_success(request):
    return render(request, 'bookings/booking_success.html')

def home(request):
    if request.user.is_authenticated:
        return redirect('user_home')   #redirect to user dashboard
    return render(request, 'home.html')

@login_required
def view_bookings(request):
    current_bookings = Booking.objects.filter(user=request.user).exclude(status='Completed').order_by('-date')
    past_bookings = Booking.objects.filter(user=request.user, status='Completed').order_by('-date')
    return render(request, 'bookings/view_bookings.html', {
        'current_bookings': current_bookings,
        'past_bookings': past_bookings
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'Pending':
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled successfully.')
    else:
        messages.error(request, 'Only pending bookings can be cancelled.')
    return redirect('view_bookings')
@login_required
def view_bookings(request):
    # Current = Pending or Accepted
    current_bookings = Booking.objects.filter(
        user=request.user,
        status__in=['Pending', 'Accepted']
    ).order_by('-created_at')

    # Past = Completed or Cancelled
    past_bookings = Booking.objects.filter(
        user=request.user,
        status__in=['Completed', 'Cancelled']
    ).order_by('-created_at')

    return render(request, 'bookings/view_bookings.html', {
        'current_bookings': current_bookings,
        'past_bookings': past_bookings
    })