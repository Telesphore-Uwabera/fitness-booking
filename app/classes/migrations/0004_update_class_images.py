from django.db import migrations
from django.core.files import File
from pathlib import Path
import shutil
import os

def update_class_images(apps, schema_editor):
    FitnessClass = apps.get_model('classes', 'FitnessClass')
    
    # Create media directory if it doesn't exist
    media_root = Path(__file__).resolve().parent.parent.parent / 'media' / 'class_images'
    media_root.mkdir(parents=True, exist_ok=True)

    # Update each class with its corresponding image
    classes = {
        'Yoga Flow': 'yoga.jpeg',
        'HIIT Training': 'hiit.jpeg',
        'Mat Pilates': 'pilates.jpeg',
        'Zumba Dance': 'zumba.jpeg'
    }

    for class_name, image_name in classes.items():
        try:
            fitness_class = FitnessClass.objects.get(name=class_name)
            image_path = media_root / image_name
            
            # Create a placeholder image file
            with open(image_path, 'wb') as f:
                f.write(b'Placeholder image data')
            
            # Update the class image field
            fitness_class.image = f'class_images/{image_name}'
            fitness_class.save()
        except FitnessClass.DoesNotExist:
            print(f"Class {class_name} not found")
        except Exception as e:
            print(f"Error updating {class_name}: {str(e)}")

def remove_class_images(apps, schema_editor):
    FitnessClass = apps.get_model('classes', 'FitnessClass')
    
    # Remove image references from classes
    FitnessClass.objects.all().update(image='')

    # Clean up media directory
    media_root = Path(__file__).resolve().parent.parent.parent / 'media' / 'class_images'
    if media_root.exists():
        shutil.rmtree(str(media_root))

class Migration(migrations.Migration):
    dependencies = [
        ('classes', '0003_add_class_images'),
    ]

    operations = [
        migrations.RunPython(update_class_images, remove_class_images),
    ] 