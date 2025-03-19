# pyright:reportUnknownMemberType =false

import os
import random

from PIL import Image
from PIL.Image import Image as ImageType


def crop_and_shuffle_image(image_path: str) -> None:
    """
    Crop the input image into 8x6 blocks and shuffle them randomly.

    Args:
        image_path (str): Path to the input image (Windows style).
    """
    # Open the image
    img = Image.open(image_path)

    # Determine block size based on 4:3 aspect ratio
    width, height = img.size
    block_width = width // 8
    block_height = height // 6

    # Calculate the number of pixels to be cropped from right and bottom
    crop_right = width % 8
    crop_bottom = height % 6

    # Crop the image to make it evenly divisible into blocks
    img = img.crop((0, 0, width - crop_right, height - crop_bottom))

    # Create a list to hold cropped blocks
    blocks: list[ImageType] = []
    for y in range(6):
        for x in range(8):
            # Calculate the coordinates for cropping each block
            left = x * block_width
            top = y * block_height
            right = left + block_width
            bottom = top + block_height
            # Crop the block and append it to the list
            blocks.append(img.crop((left, top, right, bottom)))

    # Shuffle the blocks randomly
    random.shuffle(blocks)

    # Create a new blank image to paste shuffled blocks
    new_img = Image.new('RGB', (width, height))

    # Paste shuffled blocks onto the new image
    for i, block in enumerate(blocks):
        x = (i % 8) * block_width
        y = (i // 8) * block_height
        new_img.paste(block, (x, y))

    # Save the shuffled image with a random prefix
    file_dir = os.path.dirname(image_path)
    file_name, file_ext = os.path.splitext(os.path.basename(image_path))
    random_name = '@random_' + file_name + file_ext
    new_img.save(random_name)
    random_name = rf"{file_dir}\@random_{file_name}{file_ext}"
    print(f"Shuffled image saved as: {random_name}")


crop_and_shuffle_image(input("Enter path:"))
