"""
Collect and store captchas for later processing from: https://sfd.ui.ac.ir/UserControls/Captcha.ashx
"""

import os
import requests
import hashlib
from io import BytesIO
from PIL import Image
from core.utility.variables import CAPTCHA_URL, CAPTCHA_CROP_BOX
from core.utility.file import create_directory, get_image_by_path
from core.utility.hash import get_image_hash, get_image_hash_from_object
from core.captcha.process import extract_digits_from_captcha


def find_duplicates(dir: str) -> None:
    """Find and print duplicate images in a directory."""
        
    hashes = {}
    duplicates = []
    
    for image_name in os.listdir(dir):
        
        if image_name.endswith('.png'):
            
            image_path = os.path.join(dir, image_name)
            image_hash = get_image_hash(image_path)

            if image_hash in hashes:
                print(f"Duplicate found: {image_name} is the same as {hashes[image_hash]}")
                duplicates.append((image_name, hashes[image_hash]))
            else:
                hashes[image_hash] = image_name

    print("No duplicates." if not duplicates else f"Found duplicates: {len(duplicates)}")
 
def load_hashes(dir: str, hashes: list) -> int:
    """
    Load existing image hashes from a directory.<br>
    Return number of found images.
    """
        
    counter = 0
    
    for file_name in os.listdir(dir):
        
        if file_name.endswith('.png'):
            
            image_path = os.path.join(dir, file_name)
            image_hash = get_image_hash(image_path)
            
            if image_hash not in hashes:
                hashes.append(image_hash)
                counter += 1

    print(f"{counter} hashes are added.")
    return counter

def collect_captchas(dir: str, limit: int = 100) -> None:
    """
    Collect & store captchas from the source and avoid duplicates.<br>
    Continues as long as it has stored `amount` number of new captchas.
    """
    
    create_directory(dir)        
    hashes = []
    count = load_hashes(dir, hashes)
    counter = 0
            
    while (counter < limit):
        
        response = requests.get(CAPTCHA_URL)
    
        if response.status_code == 200:

            img = Image.open(BytesIO(response.content)).convert("RGB").crop(CAPTCHA_CROP_BOX)
            image_hash = hashlib.md5(img.tobytes()).hexdigest()
            
            if image_hash not in hashes:
                print("New captcha found, amount:", count)
                hashes.append(hash)
                count += 1
                counter += 1
                filename = os.path.join(dir, f"{count}.png")
                img.save(filename, format="PNG")
            else:
                print("Duplicate found.")
        else:
            print("Failed to get image.")
            
    print("Finished.")

def seprate_digits_in_dirs() -> None:
    """
    Separate digits from captcha images into designated directories.<br>
    Avoid duplicate digits<br>
    e.g: `/digits/1` for first placed digits, `/digits/2` for second ...
    """
    
    hashes = [[],[],[],[]]
    counter = 1

    create_directory("tmp/digits/1",False)
    create_directory("tmp/digits/2",False)
    create_directory("tmp/digits/3",False)
    create_directory("tmp/digits/4",False)

    for i in range(1,1001):
        path = "../tmp/images/" + str(i) + ".png"
        captcha = get_image_by_path(path)
        images = extract_digits_from_captcha(captcha)
        
        for j in range(4):

            img_hash = get_image_hash_from_object(images[j])
            if img_hash not in hashes[j]:
                save_path = f"tmp/digits/{j+1}/{counter}.png"
                images[j].save(save_path, format="PNG")
                counter += 1
                hashes[j].append(img_hash)
                print(i,j+1,"saved!")
            else:
                print(i,j+1,"duplicate found!")
