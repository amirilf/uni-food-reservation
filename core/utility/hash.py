import hashlib
from PIL import Image
from .file import get_image_by_path

def get_img_hash_by_path(path: str) -> str:
    """
        This method gets an image path and return the image hash.<br>
        This helps to compare images and find duplicates in some scenarios
    """
    
    return hashlib.md5(get_image_by_path(path).tobytes()).hexdigest()

def get_img_hash_by_object(img: Image.Image) -> str:
    """
        This method gets an image object and return the image hash.<br>
        This helps to compare images and find duplicates in some scenarios<br>
    """
    
    img = img.convert('RGB') # to make sure its RGB
    return hashlib.md5(img.tobytes()).hexdigest()

