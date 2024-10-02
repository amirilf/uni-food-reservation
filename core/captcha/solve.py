"""
Main script for captcha solving.
"""

from PIL import Image
from io import BytesIO
from core.captcha.process import find_first_digit, find_second_digit, find_third_digit, find_forth_digit, extract_digits_from_captcha,get_digit_densities_list
from core.utility.variables import CAPTCHA_CROP_BOX

def solve(captcha_image: Image.Image) -> int: 
    """Extract digits from captcha and return the combined result as an integer."""
    
    digits = extract_digits_from_captcha(captcha_image)
    return (
        find_first_digit(get_digit_densities_list(digits[0])) * 1000 +
        find_second_digit(get_digit_densities_list(digits[1])) * 100 +
        find_third_digit(get_digit_densities_list(digits[2])) * 10 +
        find_forth_digit(get_digit_densities_list(digits[3]))
    )
    
def solve_in_byte(captcha_byte: bytes):
    """
    Process captcha bytes to return the solved result.<br>
    Useful right after retrieving the captcha from respone.content which is in bytes.
    """
    
    captcha_image = Image.open(BytesIO(captcha_byte)).convert("RGB").crop(CAPTCHA_CROP_BOX)
    return solve(captcha_image)