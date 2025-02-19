from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from utils.time_utils import load_schedule, save_schedule, generate_daily_schedule, is_point_registered, update_registered_point
from services.browser_service import register_point
from services.notification_service import send_telegram_notification
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)-7s: %(message)s",
    handlers=[
        logging.FileHandler("scheduler.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

def parse_time(time_str):
    """
    Converts a time string or datetime object into a datetime object.

    Args:
        time_str (str or datetime): The time to parse.

    Returns:
        datetime: The parsed datetime object.

    Raises:
        SystemExit: If the time format is invalid.
    """
    if isinstance(time_str, datetime):
        return time_str  # Already a datetime object, return as-is

    if isinstance(time_str, str):
        try:
            # Try parsing as 'HH:MM'
            return datetime.strptime(time_str, "%H:%M").replace(
                year=datetime.now().year,
                month=datetime.now().month,
                day=datetime.now().day
            )
        except ValueError:
            try:
                # Try parsing as 'YYYY-MM-DD HH:MM:SS'
                return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                logging.error(f"Invalid time format: {time_str}")
                sys.exit(1)

    logging.error(f"Invalid time type: {type(time_str)}")
    sys.exit(1)

def schedule_points():
    """
    Loads or generates a daily schedule and schedules the points to be registered.
    """
    logging.debug("-- Starting the schedule_points function.")

    # Load the schedule
    schedule = load_schedule()

    # If no schedule exists, generate a new one
    if not schedule:
        logging.warning("-- No schedule found. Generating a new daily schedule...")
        schedule = generate_daily_schedule()
        save_schedule(schedule)

    # Initialize the scheduler
    scheduler = BackgroundScheduler()
    today = datetime.now().strftime("%Y-%m-%d")

    for point_name, point_time in schedule.items():
        try:
            logging.debug(f"-- Processing schedule: {point_name} at {point_time}.")

            # Parse the time
            point_time = parse_time(point_time)

            # Check if the time has passed and if the point has already been registered
            if datetime.now() < point_time and not is_point_registered(today, point_name):
                logging.info(f"-- Scheduling '{point_name}' for {point_time}.")
                
                scheduler.add_job(
                    execute_point,
                    DateTrigger(run_date=point_time),
                    args=[point_name]
                )
            else:
                if datetime.now() >= point_time:
                    logging.warning(f"-- The time for '{point_name}' ({point_time}) has already passed. Skipping...")
                else:
                    logging.warning(f"-- Point '{point_name}' has already been registered. Skipping...")
        except Exception as e:
            logging.error(f"-- Error processing schedule for '{point_name}': {e}")
            sys.exit(1)

    # Start the scheduler
    logging.debug("-- Starting the scheduler...")
    scheduler.start()
    logging.info("-- Scheduler started successfully.")

def execute_point(point_name):
    """
    Executes the point registration and sends a Telegram notification.

    Args:
        point_name (str): The name of the point to register (e.g., 'check_in', 'check_out').
    """
    logging.debug("--- Starting execute_point")
    if register_point(point_name):
        message = f"✅ Point registered: {point_name} - {datetime.now().strftime('%H:%M')}"
        update_registered_point(datetime.now().strftime("%Y-%m-%d"), point_name)
    else:
        message = f"❌ Failed to register: {point_name} - {datetime.now().strftime('%H:%M')} ❌"
    
    # Send a Telegram notification
    send_telegram_notification(message)

    logging.debug("--- execute_point finished.")
