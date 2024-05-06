# importing libraries
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from companyScrapper import Company
from gptControler import company_evaluation


# Defining variables
URL = r"https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22100506914%22%5D&companySize=%5B%22D%22%2C%22E%22%2C%22F%22%2C%22G%22%5D&industryCompanyVertical=%5B%221810%22%5D&origin=FACETED_SEARCH&sid=%2C0g"

def login() -> webdriver.Chrome:
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


def company_listing(driver:webdriver.Chrome, n_pages:int = 100) -> list:
    """
    Navigates through LinkedIn search result pages by scrolling to the bottom, clicking on the 'Next' button,
    and extracts company listing URLs from all available pages.
    """
    hrefs = []
    driver.get(URL)
    wait = WebDriverWait(driver, 10)
    loop = 0
    while True:
        # Checking whether the number of pages has been reached
        if loop >= n_pages:
            break
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
                time.sleep(1)
                loop = loop +1
            else:
                print("El botón 'Siguiente' está deshabilitado o no se encontró.")
                break
        except Exception as e:
            driver.save_screenshot('error_screenshot.png')
            print(f"Ocurrió un error: {str(e)}")
            break

    return hrefs

def company_scrapping(url_link: str, driver: webdriver.Chrome) -> dict:
    """
    Scrapes detailed information from a LinkedIn company page using a webdriver.

    Args:
    url_link (str): The URL link to the LinkedIn company page.
    driver (webdriver.Chrome): A webdriver instance used to perform web scraping.

    Returns:
    dict: A dictionary containing the company information.
    """
    # Initialize a Company object to scrape data
    company_info = Company(linkedin_url=url_link, driver=driver, get_employees=False,close_on_complete=False)
    # Return the company information (here assuming it's a dict)
    return company_info

def company_orchestrator(driver:webdriver.Chrome, companies:list, requirements:str, threshold:float = 0.7)->tuple:
    """
    Orchestrates the process of scraping, evaluating, and filtering LinkedIn company pages based on given requirements and a suitability threshold.

    Args:
    driver (WebDriver): A webdriver instance used to perform web scraping.
    companies (list): A list of URLs to LinkedIn company pages.
    requirements (str): Description of the desired company profile for evaluation.
    threshold (float): The score threshold to determine if a company is suitable for selection.

    Returns:
    tuple: A tuple containing two dictionaries:
           1. Dictionary with all company names as keys and their scraped information as values.
           2. Dictionary with only suitable company names (based on the threshold) as keys and their scraped information as values.
    """
    # Initialize a dictionary to store company information
    companies_db = dict()

    # Loop over each company URL in the list
    for url in companies:
        # Scrape the company information using the company_scrapping function
        company_info = company_scrapping(url, driver)
        # Extract the company name from the URL
        name = url.split('/company/')[-1].rstrip('/')
        # Store the company information in the dictionary with the company name as the key
        companies_db[name] = company_info

        # grabbing company information
        name = company_info['about_us']
        about_us = company_info['about_us']
        specialties = company_info['specialties']
        industry = company_info['industry']
        # Putting all info together
        company_description = f"Company Name: {name}\nAbout Us: {about_us}\nSpecialties: {specialties}\nIndustry: {industry}"
        # Performing company evaluation
        score,reason = company_evaluation(requirements=requirements, company_description=company_description)
        # Saving data into data structure
        company_info['potential_customer'] = score
        company_info['reason'] = reason
    
    # filtering not-suitable companies
    selected_companies = {}
    for name, info in companies_db.items():
        # Check if the score is greater than the threshold and if so, add to the new dictionary
        if info['potential_customer'] > threshold:
            selected_companies[name] = info

    # Return the dictionary containing all the scraped company data
    return companies_db, selected_companies



if __name__ == "__main__":
    driver = login()
    hrefs = company_listing(driver=driver,n_pages=1)
    print(f"The amount of companies scrapped is: {len(hrefs)}")
    company_db, selected_companies = company_orchestrator(driver=driver, companies=hrefs)
    print(selected_companies)