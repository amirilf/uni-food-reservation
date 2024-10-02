import os
import shutil
from PIL import Image

def create_directory(dir: str, only_check: bool = True) -> None:
    """
    Create a directory at the specified path. If it already exists and `only_check` is False,
    the directory will be removed and recreated.
    """
    
    if os.path.exists(dir):
        if only_check:
            return
        shutil.rmtree(dir)
    os.makedirs(dir)

def get_image_by_path(image_path: str, make_rgb: bool = True) -> Image.Image:
    """
    Load an image from a file path and return it as an Image object.
    Optionally convert it to RGB.
    """
    
    img = Image.open(image_path)
    if make_rgb:
        img = img.convert("RGB")
    return img
