import hashlib
from PIL import Image

def get_img_hash_by_path(path: str) -> str:
    """
    Generate an MD5 hash for image by file path.\n
    Helps to compare images together and find duplicates in some scenarios.
    
    Args
    ----
    `path` : The file path to the image.
    """

    with Image.open(path) as img:
        img = img.convert('RGB')
        return hashlib.md5(img.tobytes()).hexdigest()

def get_img_hash_by_object(img: Image.Image) -> str:
    """
    Generate an MD5 hash for image object.\n
    Helps to compare images together and find duplicates in some scenarios.

    Args
    ----
    `img` : The image object to hash.
    """
    
    img = img.convert('RGB')
    return hashlib.md5(img.tobytes()).hexdigest()

