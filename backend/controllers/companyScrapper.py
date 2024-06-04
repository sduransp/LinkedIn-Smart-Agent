# Importing libraries
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.linkedin import Scraper
import time
import json
from bs4 import BeautifulSoup

# Constants used for ad banner detection
AD_BANNER_CLASSNAME = ('ad-banner-container', '__ad')

def getchildren(elem):
    """ Retrieve all child elements of a given web element.
    
    Parameters:
        elem (selenium.webdriver.remote.webelement.WebElement): The parent element.
        
    Returns:
        list: A list of WebElement found under the parent element.
    """
    return elem.find_elements(By.XPATH, ".//*")

class CompanySummary(object):
    """ Represents a brief summary of a company's LinkedIn profile including its name and follower count.

    Attributes:
        linkedin_url (str): LinkedIn URL of the company.
        name (str): Name of the company.
        followers (int): Number of followers the company has on LinkedIn.
    """
    linkedin_url = None
    name = None
    followers = None

    def __init__(self, linkedin_url = None, name = None, followers = None):
        self.linkedin_url = linkedin_url
        self.name = name
        self.followers = followers

    def __repr__(self):
        if self.followers == None:
            return """ {name} """.format(name = self.name)
        else:
            return """ {name} {followers} """.format(name = self.name, followers = self.followers)

class Company(Scraper):
    """ Represents a detailed LinkedIn company profile page scraper.

    Attributes:
        linkedin_url (str): LinkedIn URL of the company.
        name (str): Name of the company.
        about_us (str): Description of the company from LinkedIn.
        website (str): Company website URL.
        headquarters (str): Location of the company headquarters.
        founded (int): Year the company was founded.
        industry (str): Industry the company belongs to.
        company_type (str): Type of company (e.g., Public, Private).
        company_size (str): Range of number of employees.
        specialties (str): Specialties of the company.
        showcase_pages (list): List of related pages shown as showcase.
        affiliated_companies (list): List of affiliated companies.
        employees (list): List of employees scraped.
        headcount (int): Number of employees listed on LinkedIn.
    """
    linkedin_url = None
    name = None
    about_us =None
    website = None
    headquarters = None
    founded = None
    industry = None
    company_type = None
    company_size = None
    specialties = None
    showcase_pages = []
    affiliated_companies = []
    employees = []
    headcount = None
    potential_customer=None
    reason=None
    contact_people=None

    def __init__(self, potential_customer=None, reason=None, contact_people=None, linkedin_url = None, name = None, about_us =None, website = None, headquarters = None, founded = None, industry = None, company_type = None, company_size = None, specialties = None, showcase_pages =[], affiliated_companies = [], driver = None, scrape = True, get_employees = True, close_on_complete = True):
        """ Initialize the Company object with various attributes and optionally start the scraping process. """
        self.linkedin_url = linkedin_url
        self.name = name
        self.about_us = about_us
        self.website = website
        self.headquarters = headquarters
        self.founded = founded
        self.industry = industry
        self.company_type = company_type
        self.company_size = company_size
        self.specialties = specialties
        self.showcase_pages = showcase_pages
        self.affiliated_companies = affiliated_companies
        self.image = None
        self.potential_customer = potential_customer
        self.reason = reason
        self.contact_people = contact_people

        # Initialize or set up the web driver
        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(os.path.dirname(__file__), 'drivers/chromedriver')
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        driver.get(linkedin_url)
        self.driver = driver

        # Start the scraping process if specified
        if scrape:
            self.scrape(get_employees=get_employees, close_on_complete=close_on_complete)

    def __get_text_under_subtitle(self, elem):
        """ Retrieve text under a subtitle by skipping the first line which is usually the title. """
        return "\n".join(elem.text.split("\n")[1:])

    def __get_text_under_subtitle_by_class(self, driver, class_name):
        """ Find an element by class name and retrieve the text under its subtitle. """
        return self.__get_text_under_subtitle(driver.find_element(By.CLASS_NAME, class_name))

    def scrape(self, get_employees=True, close_on_complete=True):
        """Scrape the LinkedIn page for company data."""
        if self.is_signed_in():
            self.scrape_logged_in(get_employees = get_employees, close_on_complete = close_on_complete)
        else:
            self.scrape_not_logged_in(get_employees = get_employees, close_on_complete = close_on_complete)

    def __parse_employee__(self, employee_raw):

        try:
            # print()
            employee_object = {}
            employee_object['name'] = (employee_raw.text.split("\n") or [""])[0].strip()
            employee_object['designation'] = (employee_raw.text.split("\n") or [""])[3].strip()
            employee_object['linkedin_url'] = employee_raw.find_element(By.TAG_NAME, "a").get_attribute("href")
            return employee_object
        except Exception as e:
            # print(e)
            return None

    
    def get_employees(self, wait_time=10):
        """
            Retrieve and return a list of employee profile URLs from a company's LinkedIn page.

            This function navigates to a specific LinkedIn company page, ensures that the page is
            fully loaded, and then navigates to the employees' section. It collects all employee
            profile URLs across all pages of the listing.

            Args:
                wait_time (int): Time in seconds to wait for page elements to load fully, default is 10 seconds.

            Returns:
                list: A list of URLs to employee profiles.
        """
        employee_urls = []  # List to hold employee profile URLs
        driver = self.driver  # Selenium WebDriver instance

        # Scroll to the top of the page to ensure visibility of all elements
        driver.execute_script("window.scrollTo(0, 0);")
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Attempt to find the link to the employees listing page
        employee_links = driver.find_elements(By.CSS_SELECTOR, "a.ember-view.org-top-card-summary-info-list__info-item")
        href = None
        for link in employee_links:
            if 'employees' in link.find_element(By.TAG_NAME, "span").text.lower():
                href = link.get_attribute('href')
                break

        if href:
            driver.get(href)
            wait = WebDriverWait(driver, wait_time)

            while True:
                # Wait for the presence of employee list elements
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.reusable-search__entity-result-list")))

                # Extract all profile links that contain '/in/' in the current page
                profile_elements = driver.find_elements(By.CSS_SELECTOR, "li.reusable-search__result-container")
                for profile in profile_elements:
                    profile_link = profile.find_element(By.CSS_SELECTOR, "a.app-aware-link[data-test-app-aware-link]:not([aria-hidden='true'])")
                    profile_url = profile_link.get_attribute('href')
                    
                    if "/in/" in profile_url and profile_url not in employee_urls:
                        employee_urls.append(profile_url)

                # Scroll down to the bottom of the page to load more results
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

                # Check if there is a 'Next' button to navigate to the next page
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "button.artdeco-pagination__button--next")
                    if "disabled" in next_button.get_attribute("class"):
                        break  # Stop if 'Next' button is disabled
                    next_button.click()
                except NoSuchElementException:
                    print("No next page button found. Ending pagination.")
                    break
        else:
            print("Employee link not found on the page.")

        return employee_urls


    def scrape_logged_in(self, get_employees = True, close_on_complete = True):
        """Scrape LinkedIn when the user is logged in."""
        driver = self.driver

        driver.get(self.linkedin_url)
        wait = WebDriverWait(driver, 30)
        try:
            _  = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@dir="ltr"]')))
        except:
            return None
        # _ = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//span[@dir="ltr"]')))

        navigation = driver.find_element(By.CLASS_NAME, "org-page-navigation__items ")

        self.name = driver.find_element(By.XPATH,'//span[@dir="ltr"]').text.strip()

        # Click About Tab or View All Link
        try:
          self.__find_first_available_element__(
            navigation.find_elements(By.XPATH, "//a[@data-control-name='page_member_main_nav_about_tab']"),
            navigation.find_elements(By.XPATH, "//a[@data-control-name='org_about_module_see_all_view_link']"),
          ).click()
        except:
          driver.get(os.path.join(self.linkedin_url, "about"))

        _ = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'section')))
        time.sleep(3)

        try:
            logo_container = driver.find_element(By.CLASS_NAME, "org-top-card-primary-content__logo-container")
            self.image = logo_container.find_element(By.TAG_NAME, "img").get_attribute('src')
        except Exception as e:
            print("Not image found")
            self.image = None

        if 'Cookie Policy' in driver.find_elements(By.TAG_NAME, "section")[1].text or any(classname in driver.find_elements(By.TAG_NAME, "section")[1].get_attribute('class') for classname in AD_BANNER_CLASSNAME):
            section_id = 4
        else:
            section_id = 3
       #section ID is no longer needed, we are using class name now.
        #grid = driver.find_elements_by_tag_name("section")[section_id]
        grid = driver.find_element(By.CLASS_NAME, "artdeco-card.org-page-details-module__card-spacing.artdeco-card.org-about-module__margin-bottom")
        descWrapper = grid.find_elements(By.TAG_NAME, "p")
        if len(descWrapper) > 0:
            self.about_us = descWrapper[0].text.strip()
        labels = grid.find_elements(By.TAG_NAME, "dt")
        values = grid.find_elements(By.TAG_NAME, "dd")
        num_attributes = min(len(labels), len(values))
        x_off = 0
        for i in range(num_attributes):
            txt = labels[i].text.strip()
            if txt == 'Website':
                self.website = values[i+x_off].text.strip()
            elif txt == 'Industry':
                self.industry = values[i+x_off].text.strip()
            elif txt == 'Company size':
                self.company_size = values[i+x_off].text.strip()
                if len(values) > len(labels):
                    x_off = 1
            elif txt == 'Headquarters':
                    self.headquarters = values[i+x_off].text.strip()
            elif txt == 'Type':
                self.company_type = values[i+x_off].text.strip()
            elif txt == 'Founded':
                self.founded = values[i+x_off].text.strip()
            elif txt == 'Specialties':
                self.specialties = "\n".join(values[i+x_off].text.strip().split(", "))

        try:
            grid = driver.find_element(By.CLASS_NAME, "mt1")
            spans = grid.find_elements(By.TAG_NAME, "span")
            for span in spans:
                txt = span.text.strip()
                if "See all" in txt and "employees on LinkedIn" in txt:
                    self.headcount = int(txt.replace("See all", "").replace("employees on LinkedIn", "").strip())
        except NoSuchElementException: # Does not exist in page, skip it
            pass

        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")


        try:
            _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'company-list')))
            showcase, affiliated = driver.find_elements(By.CLASS_NAME, "company-list")
            driver.find_element(By.ID,"org-related-companies-module__show-more-btn").click()

            # get showcase
            for showcase_company in showcase.find_elements(By.CLASS_NAME, "org-company-card"):
                companySummary = CompanySummary(
                        linkedin_url = showcase_company.find_element(By.CLASS_NAME, "company-name-link").get_attribute("href"),
                        name = showcase_company.find_element(By.CLASS_NAME, "company-name-link").text.strip(),
                        followers = showcase_company.find_element(By.CLASS_NAME, "company-followers-count").text.strip()
                    )
                self.showcase_pages.append(companySummary)

            # affiliated company

            for affiliated_company in showcase.find_element(By.CLASS_NAME, "org-company-card"):
                companySummary = CompanySummary(
                         linkedin_url = affiliated_company.find_element(By.CLASS_NAME, "company-name-link").get_attribute("href"),
                        name = affiliated_company.find_element(By.CLASS_NAME, "company-name-link").text.strip(),
                        followers = affiliated_company.find_element(By.CLASS_NAME, "company-followers-count").text.strip()
                        )
                self.affiliated_companies.append(companySummary)

        except:
            pass

        if get_employees:
            self.employees = self.get_employees()

        driver.get(self.linkedin_url)

        if close_on_complete:
            driver.close()

    def scrape_not_logged_in(self, close_on_complete = True, retry_limit = 10, get_employees = True):
        """Attempt scraping when the user is not logged in, retrying up to 'retry_limit' times."""
        driver = self.driver
        retry_times = 0
        while self.is_signed_in() and retry_times <= retry_limit:
            page = driver.get(self.linkedin_url)
            retry_times = retry_times + 1

        self.name = driver.find_element(By.CLASS_NAME, "name").text.strip()

        self.about_us = driver.find_element(By.CLASS_NAME, "basic-info-description").text.strip()
        self.specialties = self.__get_text_under_subtitle_by_class(driver, "specialties")
        self.website = self.__get_text_under_subtitle_by_class(driver, "website")
        self.headquarters = driver.find_element(By.CLASS_NAME, "adr").text.strip()
        self.industry = driver.find_element(By.CLASS_NAME, "industry").text.strip()
        self.company_size = driver.find_element(By.CLASS_NAME, "company-size").text.strip()
        self.company_type = self.__get_text_under_subtitle_by_class(driver, "type")
        self.founded = self.__get_text_under_subtitle_by_class(driver, "founded")

        # get showcase
        try:
            driver.find_element(By.ID,"view-other-showcase-pages-dialog").click()
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'dialog')))

            showcase_pages = driver.find_elements(By.CLASS_NAME, "company-showcase-pages")[1]
            for showcase_company in showcase_pages.find_elements(By.TAG_NAME, "li"):
                name_elem = showcase_company.find_element(By.CLASS_NAME, "name")
                companySummary = CompanySummary(
                    linkedin_url = name_elem.find_element(By.TAG_NAME, "a").get_attribute("href"),
                    name = name_elem.text.strip(),
                    followers = showcase_company.text.strip().split("\n")[1]
                )
                self.showcase_pages.append(companySummary)
            driver.find_element(By.CLASS_NAME, "dialog-close").click()
        except:
            pass

        # affiliated company
        try:
            affiliated_pages = driver.find_element(By.CLASS_NAME, "affiliated-companies")
            for i, affiliated_page in enumerate(affiliated_pages.find_elements(By.CLASS_NAME, "affiliated-company-name")):
                if i % 3 == 0:
                    affiliated_pages.find_element(By.CLASS_NAME, "carousel-control-next").click()

                companySummary = CompanySummary(
                    linkedin_url = affiliated_page.find_element(By.TAG_NAME, "a").get_attribute("href"),
                    name = affiliated_page.text.strip()
                )
                self.affiliated_companies.append(companySummary)
        except:
            pass

        if get_employees:
            self.employees = self.get_employees()

        driver.get(self.linkedin_url)

        if close_on_complete:
            driver.close()

    def __repr__(self):
        """Return a JSON string representation of the Company."""
        _output = {}
        _output['name'] = self.name
        _output['about_us'] = self.about_us
        _output['specialties'] = self.specialties
        _output['website'] = self.website
        _output['industry'] = self.industry
        _output['company_type'] = self.name
        _output['headquarters'] = self.headquarters
        _output['company_size'] = self.company_size
        _output['founded'] = self.founded
        _output['affiliated_companies'] = self.affiliated_companies
        _output['employees'] = self.employees
        _output['headcount'] = self.headcount
        _output['image']=self.image
        _output['potential_customer']=self.potential_customer
        _output['reason']=self.reason
        _output['contact_people']=self.contact_people
        _output['linkedin_url']=self.linkedin_url
        
        return json.dumps(_output).replace('\n', '')