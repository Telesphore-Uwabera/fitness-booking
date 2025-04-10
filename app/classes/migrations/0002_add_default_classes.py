from django.db import migrations
from django.utils import timezone
from datetime import timedelta, datetime, time
from django.core.files import File
from pathlib import Path
import shutil
import os

def create_default_classes(apps, schema_editor):
    FitnessClass = apps.get_model('classes', 'FitnessClass')
    ClassSchedule = apps.get_model('classes', 'ClassSchedule')
    
    # Create image directories if they don't exist
    media_root = Path(__file__).resolve().parent.parent.parent / 'media' / 'class_images'
    media_root.mkdir(parents=True, exist_ok=True)

    # Copy images to media directory
    static_root = Path(__file__).resolve().parent.parent.parent / 'static' / 'images'
    static_root.mkdir(parents=True, exist_ok=True)

    # Save images in static directory
    with open(static_root / 'zumba.jpeg', 'wb') as f:
        f.write(b'[Image data for zumba class]')
    with open(static_root / 'pilates.jpeg', 'wb') as f:
        f.write(b'[Image data for pilates class]')
    with open(static_root / 'hiit.jpeg', 'wb') as f:
        f.write(b'[Image data for HIIT class]')
    with open(static_root / 'yoga.jpeg', 'wb') as f:
        f.write(b'[Image data for yoga class]')

    # Create default classes
    yoga = FitnessClass.objects.create(
        name='Yoga Flow',
        description='A dynamic flow combining breath with movement. Suitable for all levels.',
        instructor='Sarah Johnson',
        capacity=20,
        duration=timedelta(minutes=60),
        price=15.00,
        image='class_images/yoga.jpeg'
    )

    hiit = FitnessClass.objects.create(
        name='HIIT Training',
        description='High-intensity interval training to boost metabolism and build strength.',
        instructor='Mike Thompson',
        capacity=15,
        duration=timedelta(minutes=45),
        price=20.00,
        image='class_images/hiit.jpeg'
    )

    pilates = FitnessClass.objects.create(
        name='Mat Pilates',
        description='Core-strengthening exercises focusing on flexibility and posture.',
        instructor='Emma Davis',
        capacity=12,
        duration=timedelta(minutes=60),
        price=18.00,
        image='class_images/pilates.jpeg'
    )

    zumba = FitnessClass.objects.create(
        name='Zumba Dance',
        description='Fun cardio workout through dance moves and great music.',
        instructor='Carlos Rodriguez',
        capacity=25,
        duration=timedelta(minutes=60),
        price=12.00,
        image='class_images/zumba.jpeg'
    )

    # Create schedules for each class
    now = timezone.now()
    classes = [yoga, hiit, pilates, zumba]
    
    # Create schedules for the next 4 weeks
    for fitness_class in classes:
        for week in range(4):  # 4 weeks
            for day in [0, 2, 4]:  # Monday, Wednesday, Friday
                # Morning class
                morning_start = now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=day + (week * 7))
                morning_end = morning_start + fitness_class.duration
                
                ClassSchedule.objects.create(
                    fitness_class=fitness_class,
                    start_time=morning_start,
                    end_time=morning_end,
                    available_spots=fitness_class.capacity
                )

                # Evening class
                evening_start = now.replace(hour=18, minute=0, second=0, microsecond=0) + timedelta(days=day + (week * 7))
                evening_end = evening_start + fitness_class.duration
                
                ClassSchedule.objects.create(
                    fitness_class=fitness_class,
                    start_time=evening_start,
                    end_time=evening_end,
                    available_spots=fitness_class.capacity
                )

    # Copy images from static to media
    for image_name in ['yoga.jpeg', 'hiit.jpeg', 'pilates.jpeg', 'zumba.jpeg']:
        src = static_root / image_name
        dst = media_root / image_name
        if src.exists():
            shutil.copy(str(src), str(dst))

def remove_default_classes(apps, schema_editor):
    FitnessClass = apps.get_model('classes', 'FitnessClass')
    FitnessClass.objects.all().delete()

    # Clean up media directory
    media_root = Path(__file__).resolve().parent.parent.parent / 'media' / 'class_images'
    if media_root.exists():
        shutil.rmtree(str(media_root))

class Migration(migrations.Migration):
    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_classes, remove_default_classes),
    ] 