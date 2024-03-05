# pyright: reportUnknownMemberType=false
import os
from PIL import Image # type: ignore
from PIL.Image import Image as ImageType # type: ignore
import numpy as np
from multiprocessing import Pool


def decrease_brightness(file_path: str, intensity: float) -> ImageType:
    h, s, v = Image.open(file_path).convert("HSV").split()
    v = Image.fromarray(
        np.clip(np.array(v) * intensity, 0, 255).astype(np.uint8)
    )
    return Image.merge("HSV", (h, s, v)).convert("RGB")


def process_image(file_path: str, intensity: float):
    try:
        # Open the image
        # image = Image.open(file_path)
        # Decrease brightness and save
        decrease_brightness(file_path, intensity).save(file_path)
        print("Image processed:", file_path)
    except Exception as e:
        print("Error processing image:", file_path)
        print(e)


def process_directory(directory: str, intensity: float):
    # Check if the directory exists
    if not os.path.isdir(directory):
        print("Error: Directory not found.")
        return
    paras = [
        (os.path.join(directory, file_name), intensity)
        for file_name in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file_name))
        and file_name.lower().endswith('.jpg')
    ]
    # Use Pool of workers to parallelize the processing
    with Pool(processes=16) as pool:
        pool.starmap(process_image, paras)


if __name__ == "__main__":
    directory = input()
    process_directory(directory, 0.2)
