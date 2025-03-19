from io import BytesIO
from struct import pack

import win32clipboard
from PIL import Image
from PIL.Image import Image as ImageClass
from PIL.Image import Resampling
from win32.win32clipboard import CF_DIB, CF_DIBV5

# BITMAPV5HEADER constants
BITMAPV5HEADER_SIZE = 124  # The size of the BITMAPV5HEADER struct in bytes

# Helper function to convert the image to DIB format (BMP with a DIB header)
# Helper function to convert the image to DIB format (BMP with a DIB header)
def image_to_dib(image):
    with BytesIO() as output:
        # Save the image in BMP format (Pillow's BMP format includes the BMP header)
        image.save(output, format='BMP')
        bmp_data = output.getvalue()

    # Strip off the BMP header, we only need the DIB data
    dib_data = bmp_data[14:]
    return dib_data

# Helper function to convert the image to DIBV5 format
def image_to_dibv5(image:ImageClass):
    with BytesIO() as output:
        # Convert image to RGBA to ensure we have an alpha channel
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Get image dimensions
        width, height = image.size
        
        # Write the BITMAPV5HEADER
        header = pack(
            '<IIIHHIIIIIIIIIIII36sIIIIIIII',  # Binary format of the BITMAPV5HEADER
            BITMAPV5HEADER_SIZE,  # bV5Size
            width,  # bV5Width
            height,  # bV5Height
            1,  # bV5Planes (always 1)
            32,  # bV5BitCount (32-bit for RGBA)
            3,  # bV5Compression (BI_BITFIELDS = 3 for bitfields)
            width * height * 4,  # bV5SizeImage (size of the image data)
            2835,  # bV5XPelsPerMeter (default horizontal resolution in PPM)
            2835,  # bV5YPelsPerMeter (default vertical resolution in PPM)
            0,  # bV5ClrUsed (number of colors used, 0 = all)
            0,  # bV5ClrImportant (all colors are important)
            0x00FF0000,  # bV5RedMask (red channel mask)
            0x0000FF00,  # bV5GreenMask (green channel mask)
            0x000000FF,  # bV5BlueMask (blue channel mask)
            0xFF000000,  # bV5AlphaMask (alpha channel mask)
            0,  # bV5CSType (logical color space type)
            0,  # bV5Endpoints (unused)
            0,  # bV5GammaRed (unused)
            0,  # bV5GammaGreen (unused)
            0,  # bV5GammaBlue (unused)
            0,  # bV5Intent (unused)
            0,  # bV5ProfileData (unused)
            0,  # bV5ProfileSize (unused)
            0   # bV5Reserved (unused)
        )

        # Save the image data as raw bytes (without BMP header)
        image.save(output, format='BMP')
        bmp_data = output.getvalue()
        image_data = bmp_data[14:]  # Strip the BMP header

        # Combine the header and the image data
        dibv5_data = header + image_data

        return dibv5_data

# Function to handle both CF_DIB and CF_DIBV5

# Open the clipboard
win32clipboard.OpenClipboard()

try:

    if win32clipboard.IsClipboardFormatAvailable(CF_DIB):
        dib_data = win32clipboard.GetClipboardData(CF_DIB)

        if dib_data:
            dib_bytes = BytesIO(dib_data)

            # Open the image using PIL
            image = Image.open(dib_bytes)

            # Get the original size
            original_width, original_height = image.size

            # Calculate the new size (half width, half height)
            new_size = (original_width // 2, original_height // 2)

            # Resize the image to 1/4 resolution with bilinear interpolation
            resized_image = image.resize(new_size, Resampling.LANCZOS)

            # Convert resized image to DIB format
            resized_dib_data = image_to_dib(resized_image)

            # Convert resized image to DIBV5 format
            resized_dibv5_data = image_to_dibv5(resized_image)

            # Clear the clipboard and set both formats (CF_DIB and CF_DIBV5)
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(CF_DIB, resized_dib_data)
            win32clipboard.SetClipboardData(CF_DIBV5, resized_dibv5_data)

finally:
    # Close the clipboard
    win32clipboard.CloseClipboard()

