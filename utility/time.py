from datetime import datetime
import pytz

tehran_tz = pytz.timezone('Asia/Tehran')

def get_tehran_time():
    tehran_time = datetime.now(tehran_tz)
    formatted_time = tehran_time.strftime('%H:%M:%S')
    return formatted_time
