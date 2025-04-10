from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from django.utils import timezone
from datetime import timedelta

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def upgrade_membership(request):
    if request.method == 'POST':
        membership_type = request.POST.get('membership_type')
        if membership_type in ['regular', 'premium', 'student', 'senior']:
            profile = request.user.profile
            profile.membership_type = membership_type
            # Set membership end date to 1 year from now
            profile.membership_end_date = timezone.now().date() + timedelta(days=365)
            profile.save()
            messages.success(request, f'Your membership has been upgraded to {membership_type.title()}!')
            return redirect('users:profile')
    return render(request, 'users/upgrade_membership.html')

@login_required
def notification_settings(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        profile.sms_notifications = request.POST.get('sms_notifications') == 'on'
        profile.booking_reminders = request.POST.get('booking_reminders') == 'on'
        profile.promotional_emails = request.POST.get('promotional_emails') == 'on'
        profile.save()
        messages.success(request, 'Notification settings updated successfully!')
        return redirect('users:profile')
    return render(request, 'users/notification_settings.html') 