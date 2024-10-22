import os
import json
import shutil
from PIL import Image


def remove_pycaches():
    current_directory = os.getcwd()
    for root, dirs, files in os.walk(current_directory):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)

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

def save_json(text: str, filename: str ="output.json") -> None:
    """
    Get the raw text, which is generally taken from the HTTP Header Live extension in firefox (in my case).<br>
    Convert into a json file so that the form data can be checked more easily.
    """
    
    data = {}
    for pair in text.split('&'):
        if pair.strip():
            key, value = pair.split("=", 1)
            data[key.strip()] = value.strip()

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
