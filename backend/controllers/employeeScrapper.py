# importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.linkedin import Experience, Education, Scraper, Interest, Accomplishment, Contact


class Person(Scraper):
    """Represents a LinkedIn profile scraper with extended attributes and methods
    to extract detailed personal information including job experiences and education."""

    __TOP_CARD = "pv-top-card"
    __WAIT_FOR_ELEMENT_TIMEOUT = 5

    def __init__(
        self,
        linkedin_url=None,
        name=None,
        about=None,
        position=None,
        educations=None,
        interests=None,
        accomplishments=None,
        company=None,
        job_title=None,
        contacts=None,
        driver=None,
        get=True,
        scrape=True,
        close_on_complete=True,
        time_to_wait_after_login=0,
    ):
        self.linkedin_url = linkedin_url
        self.name = name
        self.about = about or []
        self.position = position or []
        self.educations = educations or []
        self.interests = interests or []
        self.accomplishments = accomplishments or []
        self.also_viewed_urls = []
        self.contacts = contacts or []
        self.contact_of_interest = None
        self.image = None

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(
                        os.path.dirname(__file__), "drivers/chromedriver"
                    )
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        if get:
            driver.get(linkedin_url)

        self.driver = driver

        if scrape:
            self.scrape(close_on_complete)

    def add_about(self, about):
        self.about.append(about)

    def add_experience(self, experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    def add_interest(self, interest):
        self.interests.append(interest)

    def add_accomplishment(self, accomplishment):
        self.accomplishments.append(accomplishment)

    def add_location(self, location):
        self.location = location

    def add_contact(self, contact):
        self.contacts.append(contact)

    def scrape(self, close_on_complete=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete)
        else:
            print("you are not logged in!")

    def _click_see_more_by_class_name(self, class_name):
        try:
            _ = WebDriverWait(self.driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            div = self.driver.find_element(By.CLASS_NAME, class_name)
            div.find_element(By.TAG_NAME, "button").click()
        except Exception as e:
            pass

    def is_open_to_work(self):
        try:
            return "#OPEN_TO_WORK" in self.driver.find_element(By.CLASS_NAME,"pv-top-card-profile-picture").find_element(By.TAG_NAME,"img").get_attribute("title")
        except:
            return False

    def get_educations(self):
        """
            Extracts education details from a LinkedIn profile and stores them in a list.
            This method navigates to the education section of a LinkedIn profile,
            waits for elements to load, and scrapes the education details such as
            institution name and degree. Each entry is then stored as an Education object.
        """
        url = os.path.join(self.linkedin_url, "details/education")
        self.driver.get(url)
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        self.scroll_to_half()
        self.scroll_to_bottom()
        # Locating the container that holds the education information.
        education_container = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'pvs-list__container')]//div[contains(@class, 'scaffold-finite-scroll__content')]"))
            )
        # Extracting individual education entries.
        education_items = education_container.find_elements(By.XPATH, ".//li[contains(@class, 'pvs-list__paged-list-item')]")
        for item in education_items:
            text = item.text.split("\n")
            institution_name = text[0]
            degree = text[2] if len(text) > 2 else "No degree information"

            # Crear el objeto Education y añadirlo a la lista
            self.educations.append(Education(
                from_date=None,
                to_date=None,
                description=None,
                degree=degree,
                institution_name=institution_name,
                linkedin_url=None,
            ))

    def get_name_and_location(self):
        """
            Extracts the name, location, and current position from a LinkedIn profile.

            This method navigates to specific elements on a LinkedIn profile page to extract:
            - The user's name,
            - Their location,
            - Their current position (job title).
            
            If any element is not found, it captures the exception and sets the corresponding attribute to None.
        """
        # Extract the full name from the profile.
        try:
            name_element = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'text-heading-xlarge')]")
            self.name = name_element.text.strip()
        except Exception as e:
            print(f"Error finding name: {e}")
            self.name = None

        # Extract the location from the profile.
        try:
            location_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'lkGISlehKsxOwfsxIBpWUCjGoPJjerBOeQXnwk')]/span[contains(@class, 't-black--light') and contains(@class, 'break-words')]")
            self.location = location_element.text.strip()
        except Exception as e:
            print(f"Error finding location: {e}")
            self.location = None

        # Extract the current position (job title) from the profile.
        try:
            position_element = self.driver.find_element(By.XPATH, "//div[@data-generated-suggestion-target][contains(@class, 'text-body-medium')]")
            self.position = position_element.text.strip()
        except Exception as e:
            print(f"Error finding position: {e}")
            self.position = None
    
    def get_profile_image(self):
        """
        Extracts the profile image URL from a LinkedIn profile.

        This method navigates to specific elements on a LinkedIn profile page to extract:
        - The user's profile image URL.
        
        If the image element is not found, it captures the exception and sets the image URL attribute to None.
        """
        # Attempt to extract the profile image URL from the profile.
        try:
            image_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'pv-top-card__non-self-photo-wrapper')]//img[contains(@class, 'pv-top-card-profile-picture__image--show')]")
            self.image = image_element.get_attribute('src').strip()
            print(self.image)
        except Exception as e:
            print(f"Error finding profile image: {e}")
            self.image = None

    def scrape_logged_in(self, close_on_complete=True):
        """
            Performs a sequence of actions to scrape data from a LinkedIn profile.

            This method sequentially executes data scraping for the user's name, location,
            and educational background. It includes scrolling actions to ensure all relevant
            data is loaded on the page. The browser is optionally closed upon completion.

            Args:
                close_on_complete (bool): If True, the web driver will close after scraping.
        """
        # Ensure the page is fully loaded.
        self.wait(1)

        # Scrape name and location information from the profile.
        self.get_name_and_location()

        # Scrolling to ensure all parts of the page are loaded.
        self.driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")
        self.driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));")

        # Scrape the education section of the LinkedIn profile.
        self.get_educations()

        # Reload the LinkedIn profile page to reset any state changed by scrolling.
        self.driver.get(self.linkedin_url)

        # Grab image
        self.get_profile_image()

        # Close the driver if specified to do so.
        if close_on_complete:
            self.driver.quit()

    @property
    def company(self):
        if self.experiences:
            return (
                self.experiences[0].institution_name
                if self.experiences[0].institution_name
                else None
            )
        else:
            return None

    @property
    def job_title(self):
        if self.experiences:
            return (
                self.experiences[0].position_title
                if self.experiences[0].position_title
                else None
            )
        else:
            return None

    def __repr__(self):
        return "<Person {name}\n\nExperience\n{pos}\n\nEducation\n{edu}\n\Image\n{image}>".format(
            name=self.name,
            about=self.about,
            pos=self.position,
            edu=self.educations,
            int=self.interests,
            acc=self.accomplishments,
            conn=self.contacts,
            of_interest=self.contact_of_interest,
            image=self.image
        )
    
if __name__ == "__main__":
    pass