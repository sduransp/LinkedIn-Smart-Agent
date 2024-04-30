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

def login():
    """
    Logs into LinkedIn using environmental variables for credentials.

    This function initializes a new instance of Chrome WebDriver, navigates
    to the LinkedIn login page, and logs in using credentials stored in
    environment variables. It allows the user to manually complete a CAPTCHA challenge.

    Returns:
        webdriver.Chrome: An instance of the Chrome WebDriver with an active
        session logged into LinkedIn.
    """

    driver = webdriver.Chrome()  # Ensure you have the Chrome WebDriver installed and in PATH
    driver.get('https://www.linkedin.com/login')
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds before timing out

    # Logging in
    username = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    username.send_keys(os.getenv("LINKEDIN_USER"))
    password = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password.send_keys(os.getenv("LINKEDIN_KEY"))
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.login__form_action_container button')))
    login_button.click()

    # Wait for user to complete the CAPTCHA manually or for redirection to the feed page
    try:
        WebDriverWait(driver, 120).until(
            EC.url_to_be('https://www.linkedin.com/feed/')
        )
        print("Redirected to LinkedIn feed, continuing with the script.")
    except Exception as e:
        print("CAPTCHA was not solved in time, please check the browser.")
        print(e)

    return driver


def company_listing(driver):
    """
    Navigates through LinkedIn search result pages by scrolling to the bottom, clicking on the 'Next' button,
    and extracts company listing URLs from all available pages.
    """
    hrefs = []
    driver.get(URL)
    wait = WebDriverWait(driver, 10)
    loop = 0
    while True:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Allow time for any lazy-loaded content to load

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        company_links = soup.select('span.entity-result__title-text a.app-aware-link')
        hrefs.extend(link.get('href') for link in company_links)

        try:
            print(f"On loop: {loop}")
            # Wait for the 'Next' button to be present and visible
            next_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view.artdeco-pagination__button.artdeco-pagination__button--next"))
            )
            print(next_btn)
            if next_btn:
                print("Clicking")
                # driver.execute_script("arguments[0].click();", next_btn)
                next_btn.click()
                print("Clicked")
                # Wait for page transition to complete before continuing to parse
                # wait.until(EC.staleness_of(company_links[0]))
                time.sleep(2)
                loop = loop +1
            else:
                print("El botón 'Siguiente' está deshabilitado o no se encontró.")
                break
        except Exception as e:
            driver.save_screenshot('error_screenshot.png')
            print(f"Ocurrió un error: {str(e)}")
            break

    return hrefs

if __name__ == "__main__":
    driver = login()
    hrefs = company_listing(driver=driver)
    print(hrefs)