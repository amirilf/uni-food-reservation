import os
import requests
from PIL import Image
from io import BytesIO
import hashlib
from utility.variables import CAPTCHA_URL, CAPTCAH_CROP_BOX
from utility.file import create_dir
from utility.hash import get_img_hash_by_path, get_img_hash_by_object
from core.captcha.process import get_image_by_path, extract_digits_from_captcha

def find_duplicates(dir:str) -> None:
    
    hashes = {}
    duplicates = []
    
    for image_name in os.listdir(dir):
        
        if image_name.endswith('.png'):
            
            image_path = os.path.join(dir, image_name)
            image_hash = get_img_hash_by_path(image_path)

            if image_hash in hashes:
                print(f"Duplicate found: {image_name} is the same as {hashes[image_hash]}")
                duplicates.append((image_name, hashes[image_hash]))
            else:
                hashes[image_hash] = image_name

    if not duplicates:
        print("No duplicates.")
    else:
        print("Found duplicates:", len(duplicates))
 
def load_hashes(dir:str, hashes:list) -> int:
    
    counter = 0
    
    for file_name in os.listdir(dir):
        
        if file_name.endswith('.png'):
            
            image_path = os.path.join(dir, file_name)
            image_hash = get_img_hash_by_path(image_path)
            
            if image_hash not in hashes:
                hashes.append(image_hash)
                counter += 1

    print(counter, "hashes are added.")
    return counter

def collect_till_death(dir:str, certainty_checker:int = 100) -> None:
    
    create_dir(dir)        
    hashes = []
    amount = load_hashes(dir, hashes)
    certainty = 0
            
    while (certainty < certainty_checker):
        
        response = requests.get(CAPTCHA_URL)
    
        if response.status_code == 200:

            img = Image.open(BytesIO(response.content))
            img = img.convert("RGB")
            img = img.crop(CAPTCAH_CROP_BOX)
            hash = hashlib.md5(img.tobytes()).hexdigest()
            
            if hash in hashes:
                certainty += 1
                print("Duplicate found.", certainty)
            else:
                print("New captcha found.", amount)
                hashes.append(hash)
                certainty = 0
                amount += 1
                filename = os.path.join(dir, f"{amount}.png")
                img.save(filename, format="PNG")
        else:
            print("Failed to get image")

    print("Finished.")

def seprate_digits_in_dirs() -> None:
    """
        Used when I wanted to seprate {ith} placed digits in seprated dirs to work with them
        and find a way to recognize them.
        
        Also used hash to avoid adding duplicates.
    """
    
    hashes = [[],[],[],[]]
    counter = 1

    create_dir("tmp/digits/1",False)
    create_dir("tmp/digits/2",False)
    create_dir("tmp/digits/3",False)
    create_dir("tmp/digits/4",False)

    for i in range(1,1001):
        path = "../tmp/images/" + str(i) + ".png"
        captcha = get_image_by_path(path)
        images = extract_digits_from_captcha(captcha)
        
        for j in range(4):

            img_hash = get_img_hash_by_object(images[j])
            if img_hash not in hashes[j]:
                save_path = f"tmp/digits/{j+1}/{counter}.png"
                images[j].save(save_path, format="PNG")
                counter += 1
                hashes[j].append(img_hash)
                print(i,j+1,"saved!")
            else:
                print(i,j+1,"duplicate found!")
