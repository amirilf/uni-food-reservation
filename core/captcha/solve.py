"""
This is the main script of the captcha package.
"""

from PIL import Image
from io import BytesIO
from core.captcha.process import find_first_digit, find_second_digit, find_third_digit, find_forth_digit, extract_digits_from_captcha,get_digit_densities_list
from core.utility.variables import CAPTCHA_CROP_BOX

def solve(captcha_image: Image.Image) -> int: 

    digits = extract_digits_from_captcha(captcha_image)
    result = 0
    result += find_first_digit(get_digit_densities_list(digits[0])) * 1000
    result += find_second_digit(get_digit_densities_list(digits[1])) * 100
    result += find_third_digit(get_digit_densities_list(digits[2])) * 10
    result += find_forth_digit(get_digit_densities_list(digits[3]))
    return result

def solve_in_byte(captcha_byte: bytes):
    """
        This methods gets result of captcha api which is type of byte<br>
        and comes from `utility.variables.CAPTCHA_URL`.
    """
       
    captcha_image = Image.open(BytesIO(captcha_byte))
    captcha_image = captcha_image.convert("RGB")
    captcha_image = captcha_image.crop(CAPTCHA_CROP_BOX)
    return solve(captcha_image)
