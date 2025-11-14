import time
import logging
from selenium.webdriver.common.by import By
from config.logging_config import setup_logging

setup_logging()

class MainPage:
    """
    Encapsulates interactions with the main page of a web application using Selenium WebDriver.

    This class provides methods for switching to the most recently opened browser tab and
    for navigating through the user interface to open the mailing menu.

    Usage:
        - Initialize with a Selenium WebDriver instance.
        - Call `switch_to_latest_tab()` to switch to the newest tab.
        - Call `open_mailing_menu()` to access the mailing section via UI navigation.
    """

    def __init__(self, driver, wait_time=1):
        self.driver = driver
        self.wait_time = wait_time

    def switch_to_latest_tab(self):
        """
        Switches the WebDrive's context to the most recently opened browser tab.

        After switching, the method waits briefly to allow the page to load.
        Logs any exceptions encountered during the process.

        Raises:
            Exception: If an error occurs while switching tabs.
        """        
        try:
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])
            time.sleep(self.wait_time)
        except Exception as e:
            logging.error(f"{__name__}: Error switching tab: {e}")
            raise

    def open_mailing_menu(self):
        """
        Opens the mailing menu by clicking through a series of nested UI elements identified by XPath.

        Each UI interaction is followed by a short wait to ensure stability. Logs any errors
        encountered during navigation.

        Raises:
            Exception: If an error occurs while attempting to open the mailing menu.
        """
        try:
            self.driver.find_element(By.XPATH, '/html/body/div[6]/ul[2]/li/span').click()
            time.sleep(self.wait_time)
            self.driver.find_element(By.XPATH, '/html/body/div[6]/ul[2]/li/ul/li[5]/span').click()
            time.sleep(self.wait_time)
            self.driver.find_element(By.XPATH, '//*[@id="m_3_18_44_0"]').click()
            time.sleep(self.wait_time)
        except Exception as e:
            logging.error(f"{__name__}: Error opening mailing menu: {e}")
            raise
