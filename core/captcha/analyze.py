from PIL import Image
from utility.hash import get_img_hash_by_object
from utility.file import create_dir


DIGIT_REGIONS = [
    (0, 17), # first digit is from col 0 to 17
    (19, 36),
    (40, 57),
    (60, 77),
]

def extract_digit_regions(image_path: str) -> list[Image.Image]:
    
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    digit_images = []
    for col_start, col_end in DIGIT_REGIONS:
        box = (col_start, 0, col_end + 1, 25)
        digit_image = img.crop(box)
        digit_images.append(digit_image)
    
    return digit_images

def split_digit_into_parts(digit_image: Image.Image) -> list[Image.Image]:
    
    part_width = 3
    part_height = 5
    
    parts = []
    for row in range(5):
        for col in range(6):
            left = col * part_width
            upper = row * part_height
            right = (col + 1) * part_width
            lower = (row + 1) * part_height
            box = (left, upper, right, lower)
            part = digit_image.crop(box)
            parts.append(part)
    
    return parts

def calculate_white_pixel_density(image: Image.Image) -> float:
    
    img = image.convert('RGB')
    width, height = img.size
    white_pixels = 0
    
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            if (r, g, b) == (255, 255, 255):
                white_pixels += 1
    
    total_pixels = width * height
    density = white_pixels / total_pixels
    return density

def analyze_image(image_path: str) -> list[float]:

    digit_regions = extract_digit_regions(image_path)    
    all_densities = []
    
    for digit_region in digit_regions:
        parts = split_digit_into_parts(digit_region)
        densities = [round(calculate_white_pixel_density(part),2) for part in parts]
        all_densities.append(densities)
    
    return all_densities

def print_image_data(image_path : str) -> None:
    
    densities = analyze_image(image_path)
    for row in range(5):
        for col in range(6):
            print(f"{densities[0][(row * 6) + col]:.2f}", end=" | ")
        print()


# TEST
hashes = [[],[],[],[]]
counter = 1

create_dir("tmp/digits/1",False)
create_dir("tmp/digits/2",False)
create_dir("tmp/digits/3",False)
create_dir("tmp/digits/4",False)

for i in range(1,20):
    path = "tmp/images/" + str(i) + ".png"
    img = extract_digit_regions(path)
    
    for j in range(4):

        img_hash = get_img_hash_by_object(img[j])
        if img_hash not in hashes[j]:
            save_path = f"tmp/digits/{j+1}/{counter}.png"
            img[j].save(save_path, format="PNG")
            counter += 1
            hashes[j].append(img_hash)
            print(i,j+1,"saved!")
        else:
            print(i,j+1,"duplicate found!")
