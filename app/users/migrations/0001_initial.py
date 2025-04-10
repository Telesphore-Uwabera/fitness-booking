# Generated by Django 4.2.7 on 2025-04-10 04:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('emergency_contact', models.CharField(blank=True, max_length=100, null=True)),
                ('emergency_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('medical_conditions', models.TextField(blank=True, null=True)),
                ('membership_type', models.CharField(choices=[('regular', 'Regular'), ('premium', 'Premium'), ('student', 'Student'), ('senior', 'Senior')], default='regular', max_length=20)),
                ('membership_start_date', models.DateField(blank=True, null=True)),
                ('membership_end_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
    ]
