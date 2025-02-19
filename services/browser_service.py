from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-7s: %(message)s",
    handlers=[
        logging.FileHandler("selenium.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

def setup_driver():
    """
    Configures and returns a Selenium WebDriver instance.
    """
    try:
        # Set up Chrome options
        chrome_options = webdriver.ChromeOptions()

        # Desabilita a câmera e o microfone
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        
        # Desabilita a permissão de localização
        chrome_options.add_argument("--disable-geolocation")
               
        # Modo Headless (sem interface gráfica)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")  # Para evitar erros em alguns ambientes

        chrome_options.binary_location = os.getenv("CHROMIUM_PATH", "/usr/bin/chromium")

        # Initialize the WebDriver
        driver_path = ChromeDriverManager().install()
        logging.info(f"----- Initializing WebDriver with Chrome options and driver path: {driver_path}")
        return webdriver.Chrome(
            service=Service(driver_path),
            options=chrome_options
        )
    except Exception as e:
        logging.error(f"----- Failed to set up WebDriver: {e}")
        sys.exit(1)
        raise

def register_point(point_type):
    """
    Registers a point (e.g., check-in, check-out) on the web portal.
    
    Args:
        point_type (str): The type of point to register (e.g., "check_in", "check_out").
    
    Returns:
        bool: True if the point was registered successfully, False otherwise.
    """
    driver = None
    logging.debug("---- Starting register_point execute_point.")
    try:
        # Set up the WebDriver
        logging.info(f"---- Setting up WebDriver for {point_type}...")
        driver = setup_driver()
        
        # Navigate to the web portal
        portal_url = os.getenv("URL")
        logging.info(f"---- Navigating to the web portal: {portal_url}")
        driver.get(portal_url)
        
        # Fill in the username and password fields
        logging.info("---- Filling in the username and password fields...")
        driver.find_element(By.ID, "codigoEmpregador").send_keys(os.getenv("USERNAME"))
        driver.find_element(By.ID, "codigoPin").send_keys(os.getenv("PASSWORD"))
        
        # Simulate clicking the register button
        logging.info(f"---- Simulating click for {point_type}...")

        driver.find_element(By.ID, "registraPonto").click()  # Uncomment this line to enable actual clicking
        logging.info(f"---- Click simulation for {point_type} completed.")
        
        # Wait for 3 seconds to simulate processing time
        time.sleep(3)
        logging.info(f"----- Point registration for {point_type} completed successfully.")
        return True
    except WebDriverException as e:
        logging.error(f"---- WebDriver error during {point_type} registration: {e}")
        return False
    except Exception as e:
        logging.error(f"---- Unexpected error during {point_type} registration: {e}")
        return False
    finally:
        # Close the WebDriver
        if driver:
            logging.info("---- Closing the WebDriver...")
            driver.quit()

        logging.debug("---- Starting register_point execute_point.")
