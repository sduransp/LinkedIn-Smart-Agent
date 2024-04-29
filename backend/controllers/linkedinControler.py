# importing libraries
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Defining variables
URL = r"https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22100506914%22%5D&companySize=%5B%22D%22%2C%22E%22%2C%22F%22%2C%22G%22%5D&industryCompanyVertical=%5B%221810%22%5D&origin=FACETED_SEARCH&sid=%2C0g"

# Defining functionality
def login():
    """
    Logs into LinkedIn using environmental variables for credentials.

    This function initializes a new instance of Chrome WebDriver, navigates
    to the LinkedIn login page, and logs in using credentials stored in
    environment variables. It assumes the LinkedIn login fields have specific
    IDs and a particular CSS selector for the login button.

    Returns:
        webdriver.Chrome: An instance of the Chrome WebDriver with an active
        session logged into LinkedIn.
    """
    
    driver = webdriver.Chrome()  # Ensure you have the Chrome WebDriver installed and in PATH

    # Navigating to the LinkedIn login page
    driver.get('https://www.linkedin.com/login')

    # Setting up WebDriverWait to handle timeouts and wait for elements to be present
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds before timing out

    # Wait and find the username field, then send keys
    username = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    username.send_keys(os.getenv("LINKEDIN_USER"))

    # Wait and find the password field, then send keys
    password = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password.send_keys(os.getenv("LINKEDIN_KEY"))

    # Wait and find the login button, then click it
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.login__form_action_container button')))
    login_button.click()

    # Returning the driver instance with an active session
    return driver

def company_listing(driver):
    """
    Navigates to a specified LinkedIn URL and extracts company listing URLs.

    Args:
        driver (webdriver.Chrome): An instance of the Chrome WebDriver.
        url (str): URL to navigate to, which contains specific LinkedIn search filters or criteria.

    Returns:
        list of str: A list of company profile URLs.
    """
    try:
        driver.get(URL)
        # Wait for the page elements to load using Selenium's WebDriverWait
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.entity-result__title-text a.app-aware-link')))

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        company_links = soup.select('span.entity-result__title-text a.app-aware-link')

        # Collect href attributes of the links
        hrefs = [link.get('href') for link in company_links]

    except Exception as e:
        print(f"An error occurred: {e}")
        hrefs = []  # Return an empty list in case of an error

    finally:
        # Consider whether you should close the driver here or elsewhere
        # driver.quit()

        return hrefs

if __name__ == "__main__":
    driver = login()
    hrefs = company_listing(driver=driver)
    print(hrefs)