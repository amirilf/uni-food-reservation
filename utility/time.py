from datetime import datetime
import pytz

tehran_tz = pytz.timezone('Asia/Tehran')

def get_tehran_time():
    return datetime.now(tehran_tz)
