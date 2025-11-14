import os
import time
import logging
import pandas as pd
from selenium.webdriver.common.by import By
from config.logging_config import setup_logging
from selenium.webdriver.support.ui import Select
setup_logging()

class MailingPage:
    """
    Automates interactions with the mailing section of a web application using Selenium WebDriver.

    This class includes methods for switching to an iframe, selecting a value from a dropdown,
    searching for campaigns, extracting mailing information from a table, and saving the collected
    data into an Excel file.

    Usage:
        - Initialize with a Selenium WebDriver instance.
        - Use the provided methods to interact with the mailing interface.
    """

    def __init__(self, driver, wait_time=1):
        self.driver = driver
        self.wait_time = wait_time
        self.raw_data = []

    def switch_to_iframe(self):
        """
        Switches the WebDriver's context to the iframe containing the mailing content.

        Waits briefly after switching. Logs and raises any exceptions.

        Raises:
            Exception: If the iframe cannot be found or switched to.
        """
        try:
            iframe = self.driver.find_element(By.XPATH, '//iframe[@id="conteudo"]')
            self.driver.switch_to.frame(iframe)
            time.sleep(self.wait_time)
        except Exception as e:
            logging.error(f"Error switching to iframe: {e}")
            raise

    def select_position(self, value='C'):
        """
        Selects a position value from the dropdown menu identified by ID 'posicao'.

        Args:
            value (str): The option value to select (default is 'C').

        Raises:
            Exception: If the dropdown element cannot be found or the selection fails.
        """
        try:
            select_element = self.driver.find_element(By.ID, 'posicao')
            select = Select(select_element)
            select.select_by_value(value)
            time.sleep(self.wait_time)
        except Exception as e:
            logging.error(f"Error selecting position: {e}")
            raise

    def search_campaign(self, texts: list):
        """
        Performs a search for each term in the provided list within the campaign name input.

        For each term, it submits the form, collects results from the table, and stores
        the cleaned data in `self.raw_data`.

        Args:
            texts (list): List of search terms (strings).

        Raises:
            Exception: If any error occurs during search or data extraction.
        """
        try:
            for text in texts:
                search_box = self.driver.find_element(By.ID, 'nome_campanha')
                search_box.clear()
                search_box.send_keys(text)
                search_box.submit()
                time.sleep(self.wait_time)

                info = self.get_mailing_info()
                lines = info.splitlines()

                # Skip the first two lines if present (typically headers)
                clean_lines = lines[2:] if len(lines) > 2 else []

                # Store non-empty lines
                for line in clean_lines:
                    if line.strip():
                        self.raw_data.append(line)

        except Exception as e:
            logging.error(f"{__name__}: Error searching campaign: {e}")
            raise

    def get_mailing_info(self):
        """
        Extracts and returns the text content from the mailing information table.

        Returns:
            str: Raw text content from the table.

        Raises:
            Exception: If the table element cannot be located or accessed.
        """
        try:
            info = self.driver.find_element(By.XPATH, '/html/body/table')
            return info.text
        except Exception as e:
            logging.error(f"{__name__}: Error getting mailing info: {e}")
            raise

    def save_raw_info(self, filepath):
        """
        Saves the collected mailing data (stored in `self.raw_data`) to an Excel file.

        Args:
            filepath (str): Destination file path for the Excel file.

        Raises:
            Exception: If the data could not be saved to the file.
        """
        try:
            df = pd.DataFrame(self.raw_data, columns=['raw_text'])
            df.to_excel(filepath, index=False)
            logging.info(f"✅ Raw information saved in {filepath}")
        except Exception as e:
            logging.error(f"❌ Error saving raw info: {e}")
            raise