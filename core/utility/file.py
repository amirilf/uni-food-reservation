import os
import shutil
from PIL import Image

def create_dir(dir: str, only_check: bool = True) -> None:
    """
    Create a directory at the specified path. if already existed then checks `only_check`
    if it's false then will remove and create that again.
    """
    
    if os.path.exists(dir):
        if only_check:
            return
        else:
            shutil.rmtree(dir)    
    os.makedirs(dir)

def get_image_by_path(image_path: str, make_rgb = True) -> Image.Image:
    """
        This method gets image path and returns image object.
    """
    
    img = Image.open(image_path)
    if make_rgb:
        img = img.convert("RGB")
    return img
