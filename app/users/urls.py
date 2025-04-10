from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/upgrade-membership/', views.upgrade_membership, name='upgrade_membership'),
    path('profile/notification-settings/', views.notification_settings, name='notification_settings'),
] 