from PIL import Image, UnidentifiedImageError
from customtkinter import CTkImage

def load_image(path, size=None):
    try:
        img = Image.open(path)
        if size:
            img = img.resize(size, Image.Resampling.LANCZOS)
        return CTkImage(dark_image=img, size=size)
    except UnidentifiedImageError:
        print(f"Invalid image file at {path}")
    return None