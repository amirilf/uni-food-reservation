"""
This script is used to process captchas to find a detection pattern.
"""

from PIL import Image
from core.utility.variables import *


# find white cols
def find_white_cols(image_path: str) -> list[int]:
    
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    width, height = img.size
    col_results = []
    
    for col in range(width):
        
        column_has_white = False
                
        for row in range(height):
            r, g, b = img.getpixel((col, row))
            if (r, g, b) == (255, 255, 255):
                column_has_white = True
                break
        
        col_results.append(int(column_has_white))   
    
    return col_results                    

def find_prev_white_cols(cols: list[int]) -> list[int]:
    
    size = len(cols)
    res = []
    prev_white = cols[0]
    
    for i in range(1,size):
        cur = cols[i]
        if prev_white and not cur:
            res.append(i)
        prev_white = cur
    
    return res
            
def find_next_white_cols(cols: list[int]) -> list[int]:
    
    size = len(cols)
    res = []
    prev_white = cols[0]
    
    for i in range(1,size):
        cur = cols[i]
        if cur and not prev_white:
            res.append(i-1)
        prev_white = cur
    
    return res

def find_surrounded_white_cols(cols: list[int]) -> list[int]:
    
    size = len(cols)
    res = []
    
    prev_prev_white = cols[0]
    prev_white = cols[1]
    
    for i in range(2,size-2):
        cur = cols[i]
        if cur and prev_prev_white and not prev_white:
            res.append(i-1)
        prev_prev_white = prev_white
        prev_white = cur
    
    return res


# find white rows
def find_white_rows(image_path: str) -> list[int]:
    
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    width, height = img.size
    row_results = []
    
    for row in range(height):
        
        row_result = []
        row_has_white = False
                
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            if (r, g, b) == (255, 255, 255):
                row_result.append(1)
            else:
                row_result.append(0)
        
        row_results.append(row_result)
    
    return row_results

def find_prev_white_rows(rows: list[int]) -> list[int]:
        
    size = len(rows)
    res = []
    prev_white = rows[0]
    
    for i in range(1, size):
        cur = rows[i]
        if prev_white and not cur:
            res.append(i)
        prev_white = cur
    
    return res

def find_next_white_rows(rows: list[int]) -> list[int]:
        
    size = len(rows)
    res = []
    prev_white = rows[0]
    
    for i in range(1, size):
        cur = rows[i]
        if cur and not prev_white:
            res.append(i-1)
        prev_white = cur
    
    return res

def find_surrounded_white_rows(rows: list[int]) -> list[int]:
    
    size = len(rows)
    res = []
    
    prev_prev_white = rows[0]
    prev_white = rows[1]
    
    for i in range(2, size-2):
        cur = rows[i]
        if cur and prev_prev_white and not prev_white:
            res.append(i-1)
        prev_prev_white = prev_white
        prev_white = cur
    
    return res


def extract_digits_from_captcha(captcha_image: Image.Image) -> list[Image.Image]:
    """
        This method gets the captcha image and extracts 4 image from it, each one is a digit.
        The area of each digit is defined in DIGIT_COL_REGIONS.
        
        - Req -> image must be RBG
        - Return -> A list of 4 images each for one digit.
    """
            
    digit_images = []
    for col_start, col_end in DIGIT_COL_REGIONS:
        box = (col_start, CAPTCHA_ROWS_RANGE[0], col_end + 1, CAPTCHA_ROWS_RANGE[1])
        digit_image = captcha_image.crop(box)
        digit_images.append(digit_image)
    
    return digit_images

def split_digit_into_parts(digit_image: Image.Image) -> list[Image.Image]:
    """
        This method gets the digit image and split it into part with size of (PARTS_ROWS, PARTS_COLS).
        
        - Req -> image must be RBG
        - Return -> List of parts in a row major order with size of DENSITIES_SIZE
    """
   
    parts = []
    for row in range(DENSITIES_SIZE[0]):
        for col in range(DENSITIES_SIZE[1]):
            left = col * PARTS_COLS
            upper = row * PARTS_ROWS
            right = (col + 1) * PARTS_COLS
            lower = (row + 1) * PARTS_ROWS
            box = (left, upper, right, lower)
            part = digit_image.crop(box)
            parts.append(part)
    
    return parts

def calculate_pixel_in_image(image: Image.Image, color: tuple[int] = (255,255,255)) -> list[int]:
    """
        This method gets an image object and then finds number of matching pixels with desired rgb code like (0,0,0) for black pixels.
    
        - Req -> image must be RBG
        - Return -> A list: [total pixels, density] 
    """
    
    width, height = image.size
    total_pixels = width * height
    pixels = 0
    
    for row in range(height):
        for col in range(width):
            r, g, b = image.getpixel((col, row))
            if (r, g, b) == color:
                pixels += 1
    
    density = pixels / total_pixels
    return [total_pixels, density]

def print_densites_list(densities : list[float]) -> None:
    """
        Just print densities list in a human readable way
    """
    
    for row in range(DENSITIES_SIZE[0]):
        for col in range(DENSITIES_SIZE[1]):
            print(f"{densities[(row * DENSITIES_SIZE[1]) + col]:.2f}", end=" | ")
        print()

def get_digit_densities_list(digit_image: Image.Image) -> list[float]:
    """
        This methods gets digit image (not captcha image!) and returns list of its parts densities (row major order)
        
        - Req -> image must be RBG
        - Return -> densities list
    """

    parts = split_digit_into_parts(digit_image)
    densities = [round(calculate_pixel_in_image(part)[1] * 100) for part in parts]
    return densities

"""
    These find_{ith}_digit method have a simple pattern to find {ith} placed digit in captcha using its densities list.
    I know this is the worst way but I'm not interested in finding a better/optimal way 0-0
    
    Actually there is no need to calculate density at all, only knowing which parts have white pixel inside is
    enough to detect most of the cases but for some, it may be necessary to know the density based on the pattern like
    the 8 and 9 in first placed digit which is solved using its density, it also can be solved with using better areas to check but I'm tired.
"""
def find_first_digit(image_densities : list[float]) -> int:    
    
    if image_densities[24]:
        # 2,3,5,6,8,9
        if not image_densities[9]:
            # 2,9 {maybe 8}
            if not image_densities[29]:
                # 9 {maybe 8}
                if image_densities[18] > 30: # using density value
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
