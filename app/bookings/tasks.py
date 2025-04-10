from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Booking

@shared_task
def send_booking_confirmation_email(booking_id):
    booking = Booking.objects.get(id=booking_id)
    subject = 'Fitness Class Booking Confirmation'
    context = {
        'booking': booking,
        'class_schedule': booking.class_schedule,
        'fitness_class': booking.class_schedule.fitness_class,
    }
    message = render_to_string('bookings/email/booking_confirmation.html', context)
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        html_message=message,
        fail_silently=False,
    )

@shared_task
def send_booking_cancellation_email(booking_id):
    booking = Booking.objects.get(id=booking_id)
    subject = 'Fitness Class Booking Cancellation'
    context = {
        'booking': booking,
        'class_schedule': booking.class_schedule,
        'fitness_class': booking.class_schedule.fitness_class,
    }
    message = render_to_string('bookings/email/booking_cancellation.html', context)
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        html_message=message,
        fail_silently=False,
    )

@shared_task
def send_class_reminder_email(booking_id):
    booking = Booking.objects.get(id=booking_id)
    subject = 'Upcoming Fitness Class Reminder'
    context = {
        'booking': booking,
        'class_schedule': booking.class_schedule,
        'fitness_class': booking.class_schedule.fitness_class,
    }
    message = render_to_string('bookings/email/class_reminder.html', context)
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        html_message=message,
        fail_silently=False,
    ) 