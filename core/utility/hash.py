from cryptography.hazmat.primitives import serialization, padding, hashes
import base64
import hashlib
from PIL import Image
from core.utility.file import get_image_by_path

def get_image_hash(path: str) -> str:
    """
    Calculate the MD5 hash of an image file given its path.<br>
    This helps to compare images and find duplicates.
    """
    
    return hashlib.md5(get_image_by_path(path).tobytes()).hexdigest()

def get_image_hash_from_object(img: Image.Image) -> str:
    """
    Calculate the MD5 hash of an image object.<br>
    This helps to compare images and find duplicates.
    """
    
    img = img.convert('RGB')  # Ensure the image is in RGB format
    return hashlib.md5(img.tobytes()).hexdigest()

def encrypt_data(data: str, pub_key_str: str) -> str:
    """
    Encrypt a string using a provided public key.<br>
    Returns the encrypted result as a base64-encoded string.
    """
    
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
