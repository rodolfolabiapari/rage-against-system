import requests
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-7s: %(message)s",
    handlers=[
        logging.FileHandler("telegram_notifications.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

def send_telegram_notification(message):
    """
    Sends a notification message to a specified Telegram chat using a bot.

    Args:
        message (str): The message to send.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    try:
        # Load Telegram bot token and chat ID from environment variables
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        if not bot_token or not chat_id:
            logging.error("Telegram bot token or chat ID is missing in environment variables.")
            return False

        # Prepare the API URL and payload
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        # Send the message via the Telegram API
        logging.info(f"Sending Telegram notification: {message}")
        response = requests.post(url, json=payload)
        
        # Check if the message was sent successfully
        if response.status_code == 200:
            logging.info("Telegram notification sent successfully.")
            return True
        else:
            logging.error(f"Failed to send Telegram notification. Status code: {response.status_code}")
            return False

    except Exception as e:
        logging.error(f"Error sending Telegram notification: {e}")
        return False
