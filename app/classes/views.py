from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import FitnessClass, ClassSchedule
from bookings.models import Booking
from django.utils import timezone
from django.db import transaction

def class_list(request):
    classes = FitnessClass.objects.filter(is_active=True)
    return render(request, 'classes/class_list.html', {'classes': classes})

def class_detail(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    available_schedules = fitness_class.schedules.filter(
        end_time__gt=timezone.now(),
        is_cancelled=False,
        available_spots__gt=0
    ).order_by('start_time')
    
    context = {
        'fitness_class': fitness_class,
        'schedules': available_schedules,
        'has_available_spots': available_schedules.exists()
    }
    return render(request, 'classes/class_detail.html', context)

@login_required
def book_class(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    
    # Check if user already has a booking for this schedule
    existing_booking = Booking.objects.filter(
        user=request.user,
        class_schedule=schedule,
        status__in=['confirmed', 'waitlisted']
    ).first()
    
    if existing_booking:
        messages.warning(request, 'You have already booked this class.')
        return redirect('classes:class_detail', class_id=schedule.fitness_class.id)
    
    # Check if the schedule is in the past
    if schedule.start_time <= timezone.now():
        messages.error(request, 'Cannot book a class that has already started.')
        return redirect('classes:class_detail', class_id=schedule.fitness_class.id)
    
    # Check if the schedule is cancelled
    if schedule.is_cancelled:
        messages.error(request, 'This class has been cancelled.')
        return redirect('classes:class_detail', class_id=schedule.fitness_class.id)
    
    with transaction.atomic():
        # Check available spots and create booking accordingly
        if schedule.available_spots > 0:
            booking = Booking.objects.create(
                user=request.user,
                class_schedule=schedule,
                status='confirmed'
            )
            schedule.available_spots -= 1
            schedule.save()
            
            # Send confirmation email
            context = {
                'user': request.user,
                'class_name': schedule.fitness_class.name,
                'start_time': schedule.start_time,
                'end_time': schedule.end_time,
            }
            html_message = render_to_string('emails/booking_confirmation.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject='Class Booking Confirmation',
                message=plain_message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True,
            )
            
            messages.success(request, 'Class booked successfully!')
        else:
            # Add to waitlist
            booking = Booking.objects.create(
                user=request.user,
                class_schedule=schedule,
                status='waitlisted'
            )
            messages.info(request, 'Class is full. You have been added to the waitlist.')
    
    return redirect('bookings:booking_list') 