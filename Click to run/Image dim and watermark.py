# pyright: reportUnknownMemberType=false
import math
import os
from multiprocessing import Pool
from typing import Optional

import cupy as cp

# import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as ImageType
from PIL.ImageDraw import ImageDraw as ImageDrawType
from PIL.ImageFont import FreeTypeFont


def decrease_brightness(file_name: str, intensity: float, font_path: Optional[str] = None) -> ImageType:
    h, s, v = Image.open(file_name).convert("HSV").split()
    # v = Image.fromarray(
    #     np.clip(np.array(v) * intensity, 0, 255).astype(np.uint8)
    # )
    v_gpu = cp.asarray(v.getdata(), dtype=cp.uint8).reshape(v.size[::-1])
    v_out_gpu = cp.clip(v_gpu * intensity, 0, 255).astype(cp.uint8)
    v_out = cp.asnumpy(v_out_gpu)
    v = Image.fromarray(v_out, mode="L")
    image: ImageType = Image.merge("HSV", (h, s, v)).convert("RGBA")

    if font_path is not None:
        layer_txt = Image.new("RGBA", image.size, (255, 255, 255, 0))

        w, h = layer_txt.size
        # Determine font size and margins
        font_size = math.ceil(3.5 / 100 * h)  # 3.5% of image height
        margin = math.ceil(0.2 / 100 * h)    # 0.2% of image height

        # Load the font
        font: FreeTypeFont = ImageFont.truetype(font_path, font_size)

        # Create a drawing context
        draw: ImageDrawType = ImageDraw.Draw(layer_txt, mode="RGBA")

        # Determine text size
        text_bbox = draw.textbbox((0, 0), file_name[:-4], font=font)
        text_width = text_bbox[2] - text_bbox[0]  # Width of the text
        text_height = text_bbox[3] - text_bbox[1]  # Height of the text

        # Calculate position for bottom-right alignment with margins
        x_position = w - text_width - 2*margin
        y_position = h - text_height - 8*margin

        # Draw text
        draw.text(
            (x_position, y_position),
            file_name[:-4],
            fill=(255, 255, 255, 25),  # White with 20% opacity
            font=font
        )
        image = Image.alpha_composite(image, layer_txt)

        # Save or show the image
        # image.show()  # Or save using image.save("output_path.jpg")
        # input()
    return image.convert("RGB")


def process_image(file_name: str, intensity: float, font_path: Optional[str] = None):
    try:
        # Open the image
        # image = Image.open(file_path)
        # Decrease brightness and save
        decrease_brightness(file_name, intensity,font_path).save(f"{file_name[:-4]}.jpg")
        print("Image processed:", file_name)
    except Exception as e:
        print("Error processing image:", file_name)
        print(e)


def process_directory(directory: str, intensity: float, font_path: Optional[str] = None):
    # Check if the directory exists
    if not os.path.isdir(directory):
        print("Error: Directory not found.")
        return
    os.chdir(directory)
    paras = [
        (file_name, intensity, font_path)
        for file_name in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file_name))
        and (file_name.lower().endswith('.jpg') or file_name.lower().endswith('.png'))
    ]
    # Use Pool of workers to parallelize the processing
    with Pool(processes=16) as pool:
        pool.starmap(process_image, paras)


if __name__ == "__main__":
    directory = input("directory: ")
    font_path = input("font_path(Leave blank to no watermark): ")
    font_path = font_path if font_path else None
    process_directory(directory, 0.2, font_path)
