from PIL import Image
from math import sqrt
from utility.hash import get_img_hash_by_object
from utility.file import create_dir

DIGIT_REGIONS = [
    (0, 17), # first digit is from col 0 to 17
    (19, 36),
    (40, 57),
    (60, 77),
]

def extract_digit_regions_from_captcha_image(image_path: str) -> list[Image.Image]:
    
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

    digit_regions = extract_digit_regions_from_captcha_image(image_path)    
    all_densities = []
    
    for digit_region in digit_regions:
        parts = split_digit_into_parts(digit_region)
        densities = [round(calculate_white_pixel_density(part),2) for part in parts]
        all_densities.append(densities)
    
    return all_densities

def print_densites_like_matrix(density : list[float]) -> None:
    for row in range(5):
        for col in range(6):
            print(f"{density[(row * 6) + col]:.2f}", end=" | ")
        print()

def seprate_digits_in_dirs():
    hashes = [[],[],[],[]]
    counter = 1

    create_dir("tmp/digits/1",False)
    create_dir("tmp/digits/2",False)
    create_dir("tmp/digits/3",False)
    create_dir("tmp/digits/4",False)

    for i in range(1,1001):
        path = "../tmp/images/" + str(i) + ".png"
        img = extract_digit_regions_from_captcha_image(path)
        
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

def get_digit_densities_list(image_path : str) -> list[float]:
    parts = split_digit_into_parts(Image.open(image_path))
    densities = [round(calculate_white_pixel_density(part) * 100) for part in parts]
    return densities

def find_first_digit(image_densities : list[float]) -> int:    
    
    if image_densities[24]:
        # 2,3,5,6,8,9
        if not image_densities[9]:
            # 2,9 {maybe 8}
            if not image_densities[29]:
                # 9 {maybe 8}
                if image_densities[18] > 0.3:
                    return 8
                return 9
            return 2
        else:
            # is 3,5,6,8
            if image_densities[12]:
                # 5,6,8
                if image_densities[17]:
                    # 5,6
                    if image_densities[10]:
                        return 6
                    return 5
                return 8  
            return 3     
    else:
        # 1,4,7
        if image_densities[4]:
            # 4,7
            if image_densities[12]:
                return 4
            return 7
        return 1

def find_second_digit(image_densities : list[float]) -> int:
    
    if image_densities[24]:
        # 2,3,5,8,9
        if image_densities[11]:
            # 2,3,8,9   
            if image_densities[13]:
                # 8,9
                if image_densities[18]:
                    return 8
                return 9
            else:
                # 2,3
                if image_densities[23]:
                    return 3
                return 2
        return 5
    else:
        # 0,1,4,6,7
        if image_densities[14]:
            # 4,6
            if image_densities[21]:
                return 4
            return 6
        else:
            # 0,1,7
            if image_densities[5]:
                # 0,7
                if image_densities[21]:
                    return 7
                return 0
            else:
                return 1

def find_third_digit(image_densities : list[float]) -> int:
    if image_densities[0]:
        # 0,2,3,5,6,7,8,9
        if image_densities[18]:
            # 0,3,5,6,8,9
            if image_densities[12]:
                # 0,5,6,9
                if image_densities[9]:
                    # 5,6
                    if image_densities[10]:
                        return 6
                    return 5
                else:
                    # 0,9
                    if image_densities[14]:
                        return 9
                    return 0
            else:
                # 3,8
                if image_densities[13]:
                    return 8
                return 3
        else:
            # 2,7
            if image_densities[28]:
                return 2
            return 7
    else:
        # 1,4
        if image_densities[19]:
            return 4
        return 1

def find_forth_digit(image_densities : list[float]) -> int:
    
    if image_densities[24]:
        # 2,3,5,8,9
        if image_densities[13]:
            # 5,8,9
            if image_densities[11]:
                # 8,9
                if image_densities[18]:
                    return 8
                return 9
            return 5
        else:
            # 2,3
            if image_densities[23]:
                return 3
            return 2
    else:
        # 0,1,3,4,6,7
        if image_densities[13]:
            # 0,4,6
            if not image_densities[21]:
                # 0,6
                if image_densities[14]:
                    return 6
                return 0
            return 4
        else:
            # 1,3,7
            if image_densities[2]:
                # 3,7
                if image_densities[20]:
                    return 7
                return 3
            return 1

# Test
list_of_densities = []
for i in range(1,300):
    path = f"tmp/digits/4/{i}.png"
    try:
        densities = get_digit_densities_list(path)
        list_of_densities.append([i,densities])
    except Exception as e:
        pass

print('==================')

for i in list_of_densities:
    print(i[0],find_forth_digit(i[1]))
