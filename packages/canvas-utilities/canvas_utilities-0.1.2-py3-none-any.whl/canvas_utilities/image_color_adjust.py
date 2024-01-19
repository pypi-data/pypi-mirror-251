from .image_utils import load_image
from PIL import Image
import numpy as np


@load_image
def adjust_image_color_curve_pil(data, lut_in=[0, 85, 160, 255], lut_out=[0, 66, 180, 255], output=None, is_grayscale=True):
    # Ensure data is a PIL Image
    if not isinstance(data, Image.Image):
        data = Image.fromarray(data)

    # Convert the image to RGB if it's not
    if data.mode != 'RGB':
        data = data.convert('RGB')

    # Prepare the LUT (lookup table) for color curve adjustment
    lut = np.interp(np.arange(256), lut_in, lut_out).astype(np.uint8)
    
    # Apply LUT to each channel of the image
    channels = [Image.fromarray(lut[np.array(data.getchannel(ch))]) for ch in ['R', 'G', 'B']]
    image_contrasted = Image.merge('RGB', channels)

    # Convert to grayscale if required
    if is_grayscale:
        image_contrasted = image_contrasted.convert('L')

    # Save the image if an output path is provided
    if output:
        image_contrasted.save(output)

    return image_contrasted