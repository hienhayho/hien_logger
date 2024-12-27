import os
import pytz
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def convert_boolean_env_var(env_var: str) -> bool:
    """
    Convert a boolean environment variable to a boolean value.
    """
    return os.getenv(env_var, "False").lower() in [
        "true",
        "1",
    ]


def get_now():
    """
    Get the current date and time in Asia/Ho_Chi_Minh timezone
    """
    tz = os.getenv("TZ", "Asia/Singapore")
    timezone = pytz.timezone(tz)
    current_time = datetime.now(timezone)
    return current_time


def get_date_format():
    """
    Get the current date in the format "dd_mm_yyyy"
    """
    current_time = get_now()
    formatted_date = current_time.strftime("%d_%m_%Y")
    return formatted_date
