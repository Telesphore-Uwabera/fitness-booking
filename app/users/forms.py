from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        exclude = ('password',) 