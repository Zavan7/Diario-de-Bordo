import os
import logging
from selenium import webdriver
from dotenv import load_dotenv
from config.logging_config import setup_logging
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.main_pagem import MainPage
from pages.login_page import LoginPage
from pages.mainling_page import MailingPage
from base_tratament import MailingProcessor

load_dotenv()
setup_logging()

user = os.getenv('USER')
password = os.getenv('PASSWORD')
github_token = os.getenv("GITHUB_TOKEN")

acd_list = (
    'LISTA DE ACDS'
)

def service():
    """
    Initializes the Selenium Chrome WebDriver, performs the automated mailing data
    extraction process, and processes the collected data.

    Workflow:
    - Starts the Chrome browser with chromedriver managed automatically.
    - Navigates to the target site.
    - Logs in using credentials from environment variables.
    - Navigates through the main page to the mailing menu.
    - Interacts with the mailing page to collect campaign data.
    - Saves the raw mailing data to an Excel file.
    - Processes the raw data using MailingProcessor to clean and filter it.
    - Ensures browser closes properly after execution.

    Logs warnings if GitHub token is missing, which may affect API limits.

    Raises:
        Various exceptions depending on failure points in WebDriver or page interactions.
    """
    logging.basicConfig(level=logging.INFO)

    # Configura a variável de ambiente para autenticar o webdriver_manager no GitHub
    if github_token:
        os.environ['GH_TOKEN'] = github_token
    else:
        logging.warning("⚠️  GITHUB_TOKEN not found. You may have reached the GitHub API limit.")


    # Inicia o Chrome com chromedriver gerenciado automaticamente
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
    )

    try:
        driver.get('URL')

        login_page = LoginPage(driver, user, password)
        login_page.login()

        main_page = MainPage(driver)
        main_page.switch_to_latest_tab()
        main_page.open_mailing_menu()

        mailing_page = MailingPage(driver)
        mailing_page.switch_to_iframe()
        mailing_page.select_position('C')
        mailing_page.search_campaign(acd_list)
        mailing_page.save_raw_info('mailing_info_raw.xlsx')

        logging.info("✅ Mailing data saved in mailing_info_raw.xlsx")

        processor = MailingProcessor(
            input_file='mailing_info_raw.xlsx',
            output_file='Diario de Bordo.xlsx'
        )
        processor.process()
        logging.info('✅ Processing completed successfully.')

    finally:
        driver.quit()


if __name__ == '__main__':

    try:
        service()

    except ValueError as e:
        print(f'Error {e}')
