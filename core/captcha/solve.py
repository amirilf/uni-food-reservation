"""
This is the main script of the captcha package.
"""

from PIL import Image
from .process import find_first_digit, find_second_digit, find_third_digit, find_forth_digit, extract_digits_from_captcha,get_digit_densities_list

def solve(captcha_image : Image.Image) -> int: 

    digits = extract_digits_from_captcha(captcha_image)
    result = 0
    result += find_first_digit(get_digit_densities_list(digits[0])) * 1000
    result += find_second_digit(get_digit_densities_list(digits[1])) * 100
    result += find_third_digit(get_digit_densities_list(digits[2])) * 10
    result += find_forth_digit(get_digit_densities_list(digits[3]))
    return result
