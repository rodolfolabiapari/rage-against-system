from services.scheduler_service import schedule_points
from utils.time_utils import generate_daily_schedule, save_schedule
from datetime import datetime
import sys
import time
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-7s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

# Load environment variables
load_dotenv()

def main():
    """
    Main function to start the point registration system.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "/baterponto":
        current_time = datetime.now()
        
        # If it's before 8 AM, generate a new schedule for the day
        if current_time.hour < 8:
            logging.info("It's before 8 AM. Generating a new daily schedule...")
            daily_schedule = generate_daily_schedule()
            save_schedule(daily_schedule)
            logging.info("New daily schedule generated and saved.")
        
        # Load environment variables again (if needed)
        load_dotenv()
        
        # Start scheduling points
        logging.info("Starting to schedule points...")
        schedule_points()
        
        # Keep the script running
        try:
            logging.info("Script is running. Waiting for scheduled tasks...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Script interrupted by user. Exiting...")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            sys.exit(1)
    else:
        logging.info("Execute python bater_ponto.py /baterponto")

if __name__ == "__main__":
    main()
