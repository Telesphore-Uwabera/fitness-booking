from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Booking
from classes.models import ClassSchedule

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).select_related('class_schedule', 'class_schedule__fitness_class')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        with transaction.atomic():
            # Store schedule reference before deletion
            schedule = booking.class_schedule
            
            # Check if the booking was confirmed (not waitlisted)
            was_confirmed = booking.status == 'confirmed'
            
            # Update booking status to cancelled
            booking.status = 'cancelled'
            booking.cancellation_date = timezone.now()
            booking.save()
            
            if was_confirmed:
                # Increment available spots for confirmed bookings
                schedule.available_spots += 1
                schedule.save()
                
                # Try to promote someone from the waitlist
                waitlist_booking = Booking.objects.filter(
                    class_schedule=schedule,
                    status='waitlisted'
                ).order_by('created_at').first()
                
                if waitlist_booking:
                    # Promote the first person from waitlist
                    waitlist_booking.status = 'confirmed'
                    waitlist_booking.save()
                    
                    # Decrement available spots again
                    schedule.available_spots -= 1
                    schedule.save()
                    
                    # Notify the promoted user (you would implement this)
                    # send_promotion_notification(waitlist_booking)
            
            messages.success(request, 'Your booking has been cancelled successfully.')
        return redirect('bookings:booking_list')
        
    return render(request, 'bookings/cancel_booking.html', {'booking': booking}) 