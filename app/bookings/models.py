from django.db import models
from django.conf import settings
from django.utils import timezone
from classes.models import ClassSchedule

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(
        max_length=20,
        choices=[
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
            ('waitlisted', 'Waitlisted'),
        ],
        default='confirmed'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    cancellation_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'class_schedule']

    def __str__(self):
        return f"{self.user.email} - {self.class_schedule}"

    def save(self, *args, **kwargs):
        if self.status == 'cancelled' and not self.cancellation_date:
            self.cancellation_date = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_cancelled(self):
        return self.status == 'cancelled'

    @property
    def is_waitlisted(self):
        return self.status == 'waitlisted'

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('refunded', 'Refunded'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for {self.booking}" 