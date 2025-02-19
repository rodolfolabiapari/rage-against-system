from datetime import datetime, timedelta, date
from pathlib import Path
import random
import json
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)-7s: %(message)s",
    handlers=[
        logging.FileHandler("time_utils.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

def load_registered_points():
    """
    Loads the registered points from a JSON file.

    Returns:
        dict: A dictionary containing the registered points.
    """
    file_path = "schedules/registered_points.json"
    if Path(file_path).exists():
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def generate_time_with_variation(base_hour, base_minute, variation=3):
    """
    Generates a time with a random variation.

    Args:
        base_hour (int): The base hour.
        base_minute (int): The base minute.
        variation (int): The maximum variation in minutes.

    Returns:
        datetime: The generated time with variation.
    """
    variation_min = random.randint(-variation, variation)
    return datetime.now().replace(
        hour=base_hour,
        minute=base_minute,
        second=0,
        microsecond=0
    ) + timedelta(minutes=variation_min)

def is_lunch_valid(lunch_out, lunch_in):
    """
    Checks if the lunch duration is valid (at least 70 minutes).

    Args:
        lunch_out (datetime): The time when lunch starts.
        lunch_in (datetime): The time when lunch ends.

    Returns:
        bool: True if the lunch duration is valid, False otherwise.
    """
    return (lunch_in - lunch_out) >= timedelta(minutes=70)

def generate_daily_schedule():
    """
    Generates a daily schedule with random variations.

    Returns:
        dict: A dictionary containing the daily schedule.
    """
    # Base times
    schedule = {
        "check_in": generate_time_with_variation(8, 0),
        "lunch_out": generate_time_with_variation(12, 50),
        "lunch_in": generate_time_with_variation(14, 0),
        "check_out": generate_time_with_variation(18, 6)
    }
    
    # Ensure the lunch duration is valid
    while not is_lunch_valid(schedule["lunch_out"], schedule["lunch_in"]):
        schedule["lunch_in"] += timedelta(minutes=5)
    
    return schedule

def generate_advanced_variation():
    """
    Generates a more advanced time variation.

    Returns:
        int: A random variation in minutes.
    """
    return random.choice([
        random.randint(-3, 3),
        random.randint(-5, 0),
        random.randint(0, 5)
    ])

def is_workday():
    """
    Checks if today is a workday (Monday to Friday).

    Returns:
        bool: True if today is a workday, False otherwise.
    """
    today = date.today()
    return today.weekday() < 5  # 0-4 = Monday to Friday

def json_serializer(obj):
    """
    Serializes non-JSON-serializable objects, such as datetime.

    Args:
        obj: The object to serialize.

    Returns:
        str: The serialized object.

    Raises:
        TypeError: If the object type is not supported.
    """
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
    raise TypeError(f"Type {type(obj)} is not JSON serializable")

def save_schedule(schedule, file_path="schedules/today_schedule.json"):
    """
    Saves a schedule to a JSON file.

    Args:
        schedule (dict): The schedule to save.
        file_path (str): The path to the JSON file.
    """
    try:
        logging.debug(f"Attempting to save the schedule to {file_path}...")
        with open(file_path, "w") as f:
            json.dump(schedule, f, indent=4, default=json_serializer)
        logging.info(f"Schedule successfully saved to {file_path}.")
    except Exception as e:
        logging.error(f"Error saving the schedule: {e}")
        sys.exit(1)

def load_schedule(file_path="schedules/today_schedule.json"):
    """
    Loads a schedule from a JSON file, if it exists.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded schedule, or None if the file does not exist.
    """
    try:
        if Path(file_path).exists():
            logging.debug(f"File {file_path} found. Attempting to load...")
            with open(file_path, "r") as f:
                data = json.load(f)
            logging.info(f"Schedule successfully loaded from {file_path}.")
            return data
        else:
            logging.warning(f"File {file_path} not found.")
            return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from file {file_path}: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error loading the schedule: {e}")
        sys.exit(1)

def is_point_registered(date_str, point_name):
    """
    Checks if a point has already been registered on a specific date.

    Args:
        date_str (str): The date in 'YYYY-MM-DD' format.
        point_name (str): The name of the point (e.g., 'check_in').

    Returns:
        bool: True if the point has been registered, False otherwise.
    """
    registered_points = load_registered_points()
    return registered_points.get(date_str, {}).get(point_name, False)

def update_registered_point(date_str, point_name):
    """
    Updates the registered points with a new point.

    Args:
        date_str (str): The date in 'YYYY-MM-DD' format.
        point_name (str): The name of the point (e.g., 'check_in').
    """
    registered_points = load_registered_points()
    if date_str not in registered_points:
        registered_points[date_str] = {}
    registered_points[date_str][point_name] = True
    with open("schedules/registered_points.json", "w") as f:
        json.dump(registered_points, f, indent=4)
