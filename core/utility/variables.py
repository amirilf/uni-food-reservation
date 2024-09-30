# URLs
MAIN_URL = "https://sfd.ui.ac.ir"
CAPTCHA_URL = MAIN_URL + "/UserControls/Captcha.ashx"
CAPTCAH_CROP_BOX = (78, 9, 156, 34)


# CAPTCHA
DIGIT_COL_REGIONS = [
    # cpatcha size is 78*25, we need full rows but specific cols
    (0, 17),
    (19, 36),
    (40, 57),
    (60, 77),
]
CAPTCHA_ROWS_RANGE = (0,25)
DIGIT_ROWS = 25
DIGIT_COLS = 18
PARTS_ROWS = 5
PARTS_COLS = 3
DENSITIES_SIZE = (int(DIGIT_ROWS / PARTS_ROWS), int(DIGIT_COLS / PARTS_COLS))
