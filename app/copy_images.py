import os
from pathlib import Path
import shutil

def copy_images():
    # Get the base directory
    base_dir = Path(__file__).resolve().parent
    media_dir = base_dir / 'media' / 'class_images'
    media_dir.mkdir(parents=True, exist_ok=True)

    # Define the image mappings (you'll need to provide the actual image paths)
    image_mappings = {
        'zumba.jpg': 'path/to/zumba/image.jpg',
        'pilates.jpg': 'path/to/pilates/image.jpg',
        'hiit.jpg': 'path/to/hiit/image.jpg',
        'yoga.jpg': 'path/to/yoga/image.jpg'
    }

    # Copy each image
    for dest_name, src_path in image_mappings.items():
        dest_path = media_dir / dest_name
        try:
            # For now, create placeholder images
            with open(dest_path, 'wb') as f:
                f.write(b'Placeholder image data - Replace with actual image')
            print(f"Created placeholder for {dest_name}")
        except Exception as e:
            print(f"Error copying {dest_name}: {str(e)}")

if __name__ == '__main__':
    copy_images() 