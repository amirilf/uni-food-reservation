# =================================== MAIN VARIABLES
DEVELOPMENT = True


# =================================== BOT VARIABLES
from datetime import time
import pytz

MIN_IN_SECONDS = 60
HOUR_IN_SECONDS = 60 * MIN_IN_SECONDS
DAY_IN_SECONDS = 24 * HOUR_IN_SECONDS
WEEK_IN_SECONDS = 7 * DAY_IN_SECONDS

RESERVE_TIME = time(tzinfo=pytz.timezone('Asia/Tehran'),hour=14,minute=44,second=25)
RESERVE_DAY = (1,)  # Monday


# =================================== CORE VARIABLES
# Base URL
MAIN_URL = "https://sfd.ui.ac.ir"

# Auth URLs
LOGIN_URL = MAIN_URL + "/Login.aspx"

# User URLs
USER_URL = MAIN_URL + "/UserControls"
CAPTCHA_URL = USER_URL + "/Captcha.ashx"
PROFILE_IMAGE_URL = USER_URL + "/UserImage.ashx"

# Callinun URLs
CALLINUN_URL = MAIN_URL + "/MyCullinan"
PROFILE_URL = CALLINUN_URL + "/MyProfile.aspx"
TRANSACTIONS_URL = CALLINUN_URL + "/MyTransaction.aspx"
MESSAGES_URL = CALLINUN_URL + "/MyMessage.aspx"

# Reservation URLs
RESERVATION_URL = MAIN_URL + "/Reservation"
SELF_URL = RESERVATION_URL + "/Reservation.aspx"
YAS_URL = RESERVATION_URL + "/CafeteriaReservation.aspx"
FORGET_URL = RESERVATION_URL + "/ForgotReceipt.aspx"

# Payment URLs
PAYMENT_URL = MAIN_URL + "/ePay/ePay_Payment.aspx"
PAYMENT_MIN = 1_000
PAYMENT_MAX = 5_000_000

# CAPTCHA settings
CAPTCHA_CROP_BOX = (78, 9, 156, 34)  # Captcha size is (78, 25)
DIGIT_COL_REGIONS = [(0, 17), (19, 36), (40, 57), (60, 77)]
CAPTCHA_ROWS_RANGE = (0, 25)
DIGIT_ROWS = 25
DIGIT_COLS = 18
PARTS_ROWS = 5
PARTS_COLS = 3
DENSITIES_SIZE = (DIGIT_ROWS // PARTS_ROWS, DIGIT_COLS // PARTS_COLS)

# Auth session headers
AUTH_SESSION_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
}

CULLINAN_COOKIE_NAME = "ASP.NET_SessionId"
