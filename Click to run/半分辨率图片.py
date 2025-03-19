import os

from PIL import Image

# Get the directory path from the user
process_dir = input("Enter the directory containing images to process: ")
os.chdir(process_dir)

# List files in the directory
file_list = [f for f in os.listdir() if f.lower().endswith(('.png','.jpg'))]

# Process each image
for file_name in file_list:
    with Image.open(file_name) as img:
        # Get original dimensions
        original_width, original_height = img.size
        # Calculate new dimensions
        new_size = (original_width // 2, original_height // 2)
        # Resize image
        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
        # Save image (overwriting the original file)
        resized_img.convert("RGB").save(f"{file_name[:-4]}.jpg")

print("Image processing complete.")
