from django.db import migrations
import os
import shutil
from pathlib import Path
import base64

def add_class_images(apps, schema_editor):
    # Define the image data (base64 encoded)
    image_data = {
        'zumba.jpg': '/9j/4AAQSkZJRgABAQEASABIAAD/4gHYSUNDX1BST...',  # Your first image
        'pilates.jpg': '/9j/4AAQSkZJRgABAQEASABIAAD/4gHYSUNDX1BST...',  # Your second image
        'hiit.jpg': '/9j/4AAQSkZJRgABAQEASABIAAD/4gHYSUNDX1BST...',  # Your third image
        'yoga.jpg': '/9j/4AAQSkZJRgABAQEASABIAAD/4gHYSUNDX1BST...'  # Your fourth image
    }

    # Create media directory if it doesn't exist
    media_root = Path(__file__).resolve().parent.parent.parent / 'media' / 'class_images'
    media_root.mkdir(parents=True, exist_ok=True)

    # Save images to media directory
    for image_name, image_data in image_data.items():
        image_path = media_root / image_name
        try:
            # Write the decoded image data to file
            with open(image_path, 'wb') as f:
                f.write(base64.b64decode(image_data))
        except Exception as e:
            print(f"Error saving {image_name}: {str(e)}")

def remove_class_images(apps, schema_editor):
    # Clean up media directory
    media_root = Path(__file__).resolve().parent.parent.parent / 'media' / 'class_images'
    if media_root.exists():
        shutil.rmtree(str(media_root))

class Migration(migrations.Migration):
    dependencies = [
        ('classes', '0002_add_default_classes'),
    ]

    operations = [
        migrations.RunPython(add_class_images, remove_class_images),
    ] 