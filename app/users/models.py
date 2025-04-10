from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    membership_type = models.CharField(
        max_length=20,
        choices=[
            ('regular', 'Regular'),
            ('premium', 'Premium'),
            ('student', 'Student'),
            ('senior', 'Senior'),
        ],
        default='regular'
    )
    membership_start_date = models.DateField(null=True, blank=True)
    membership_end_date = models.DateField(null=True, blank=True)
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    booking_reminders = models.BooleanField(default=True)
    promotional_emails = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"

    @property
    def is_membership_active(self):
        if not self.membership_end_date:
            return False
        return self.membership_end_date >= timezone.now().date()

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles') 