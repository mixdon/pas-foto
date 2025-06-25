from PIL import Image, ImageOps, ImageFilter
import numpy as np
import os

def apply_mask(image: Image.Image, mask: Image.Image, feather_radius=3):
    
    image = image.convert("RGBA")
    mask = mask.convert("L")

    # Feathering (blur edges)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather_radius))

    background = Image.new("RGBA", image.size, (0, 0, 0, 0))
    combined = Image.composite(image, background, mask)
    return combined

def replace_background(foreground: Image.Image, background_input, size_cm=(3, 4), dpi=300):

    width = int(size_cm[0] / 2.54 * dpi)
    height = int(size_cm[1] / 2.54 * dpi)

    # 10 warna umum untuk pas foto
    color_map = {
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "white": (255, 255, 255),
        "lightgray": (211, 211, 211),
        "darkgray": (105, 105, 105),
        "black": (0, 0, 0),
        "green": (0, 128, 0),
        "yellow": (255, 255, 0),
        "orange": (255, 165, 0),
        "brown": (150, 75, 0)
    }

    # Jika input adalah Image, gunakan sebagai custom background
    if isinstance(background_input, Image.Image):
        bg = ImageOps.fit(background_input.convert("RGB"), (width, height), method=Image.LANCZOS, centering=(0.5, 0.5))
    else:
        # Jika string warna
        bg_color = color_map.get(str(background_input).lower(), (255, 255, 255))  # default putih
        bg = Image.new("RGB", (width, height), bg_color)

    fg_resized = ImageOps.fit(foreground, (width, height), method=Image.LANCZOS, centering=(0.5, 0.5))
    bg.paste(fg_resized, (0, 0), fg_resized)
    return bg