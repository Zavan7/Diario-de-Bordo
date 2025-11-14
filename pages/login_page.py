import time
import logging
from selenium.webdriver.common.by import By
from config.logging_config import setup_logging

setup_logging()

# Class to perform successful login
class LoginPage:
    """
    Automates the login process using Selenium WebDriver.

    This class locates the username and password input fields by their 'name'
    attributes, fills them with the provided credentials, and submits the login form.

    Attributes:
        driver: A Selenium WebDriver instance used to interact with the web page.
        user: The username to be entered into the login form.
        password: The password to be entered into the login form.
        wait_time: Time in seconds to wait after submitting the form (default is 1).

    Usage:
        login_page = LoginPage(driver, "my_user", "my_pass")
        login_page.login()
    """
    def __init__(self, driver, user, password, wait_time=1):
        """
        Initializes the LoginPage with the WebDriver and user credentials.

        Args:
            driver: Selenium WebDriver instance.
            user: Username as a string.
            password: Password as a string.
            wait_time: Optional; number of seconds to wait after login (default is 1).
        """
        self.driver = driver
        self.user = user
        self.password = password
        self.wait_time = wait_time

    def login(self):
        """
        Performs the login by entering the username and password into the appropriate
        input fields and submitting the form.

        Waits for a short period after submitting the form. Logs any exceptions
        that occur during the process for debugging purposes.

        Raises:
            Exception: Any error encountered during the login attempt.
        """
        try:
            self.driver.find_element(By.NAME, 'nome').send_keys(self.user)
            self.driver.find_element(By.NAME, 'senha').send_keys(self.password)
            self.driver.find_element(By.NAME, 'senha').submit()
            time.sleep(self.wait_time)
        except Exception as e:
            logging.error(f"{__name__}: Login error: {e}")
            raise