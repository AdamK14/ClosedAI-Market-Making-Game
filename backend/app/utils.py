import random
from datetime import datetime, timedelta

def formate_datetime(dt):
    """Converts a datetime object to a string."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def parse_datetime(dt_string):
    """Converts a string to a datetime object."""
    return datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")

def generate_random_price(min_price, max_price, precesion=2):
    """Generates a random price within the given range."""
    return round(random.uniform(min_price, max_price), precesion)

def add_secs_to_datetime(dt, seconds):
    """Adds seconds to a datetime object."""
    return dt + timedelta(seconds=seconds)