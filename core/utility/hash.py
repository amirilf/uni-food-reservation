from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
import hashlib
from PIL import Image
from core.utility.file import get_image_by_path

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

def encrypt_data(data, pub_key_str):
    public_key = serialization.load_pem_public_key(pub_key_str.encode())
    encrypted_data = public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_data).decode()
