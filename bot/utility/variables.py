from datetime import time
import pytz

PROXY = "http://192.168.175.26:8080"

# TIMES IN SECONDS
MIN_IN_SECONDS = 60
HOUR_IN_SECONDS = 60 * MIN_IN_SECONDS
DAY_IN_SECONDS = 24 * HOUR_IN_SECONDS
WEEK_IN_SECONDS = 7 * DAY_IN_SECONDS

RESERVE_TIME = time(tzinfo=pytz.timezone('Asia/Tehran'),hour=14,minute=44,second=25)
RESERVE_DAY = (1,)  # Monday
