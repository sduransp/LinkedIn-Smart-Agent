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
        url = os.path.join(self.linkedin_url, "details/education")
        self.driver.get(url)
        print("Waiting for main")
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        print("Main is over")
        self.scroll_to_half()
        self.scroll_to_bottom()
        print("Finding education items")
        education_container = self.driver.find_element(By.XPATH, "//div[contains(@class, 'pvs-list__container')]//div[contains(@class, 'scaffold-finite-scroll__content')]")
        education_items = education_container.find_elements(By.XPATH, ".//li[contains(@class, 'pvs-list__paged-list-item')]")
        print(f"Education items: {education_items}")
        for item in education_items:
            # Extraer el nombre de la institución
            try:
                institution_name = item.find_element(By.CSS_SELECTOR, "div.display-flex a.optional-action-target-wrapper div.display-flex.align-items-center.hoverable-link-text").text.strip()
                print(f"The institution name is: {institution_name}")
            except NoSuchElementException:
                institution_name = None

            # Extraer el grado obtenido
            try:
                degree = item.find_element(By.CSS_SELECTOR, "span.t-14.t-normal").text.strip()
                print(f"The degree is {degree}")
            except NoSuchElementException:
                degree = None

            # Crear el objeto Education y añadirlo a la lista
            self.educations.append(Education(
                from_date=None,
                to_date=None,
                description=None,
                degree=degree,
                institution_name=institution_name,
                linkedin_url=None,
            ))
        
        print(f"The education is: {self.educations}")


    def get_name_and_location(self):
    # Intentar encontrar el elemento <h1> que contiene el nombre completo.
        try:
            name_element = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'text-heading-xlarge')]")
            self.name = name_element.text.strip()
        except Exception as e:
            print(f"Error finding name: {e}")
            self.name = None

        # Intentar encontrar el span que contiene la ubicación.
        try:
            location_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'lkGISlehKsxOwfsxIBpWUCjGoPJjerBOeQXnwk')]/span[contains(@class, 't-black--light') and contains(@class, 'break-words')]")
            self.location = location_element.text.strip()
        except Exception as e:
            print(f"Error finding location: {e}")
            self.location = None
        
        try:
            position_element = self.driver.find_element(By.XPATH, "//div[@data-generated-suggestion-target][contains(@class, 'text-body-medium')]")
            self.position = position_element.text.strip()
        except Exception as e:
            print(f"Error finding position: {e}")
            self.position = None

        print(f"Name is: {self.name}")
        print(f"Location is: {self.location}") 
        print(f"Position is: {self.position}") 
    

    def scrape_logged_in(self, close_on_complete=True):
        driver = self.driver
        
        self.wait(1)

        # get name and location
        self.get_name_and_location()

        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
        )
        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));"
        )

        # get education
        self.get_educations()

        driver.get(self.linkedin_url)

        # get interest
        try:

            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@class='pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view']",
                    )
                )
            )
            interestContainer = driver.find_element(By.XPATH,
                "//*[@class='pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view']"
            )
            for interestElement in interestContainer.find_elements(By.XPATH, 
                "//*[@class='pv-interest-entity pv-profile-section__card-item ember-view']"
            ):
                interest = Interest(
                    interestElement.find_element(By.TAG_NAME, "h3").text.strip()
                )
                self.add_interest(interest)
        except:
            pass

        # get accomplishment
        try:
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@class='pv-profile-section pv-accomplishments-section artdeco-container-card artdeco-card ember-view']",
                    )
                )
            )
            acc = driver.find_element(By.XPATH,
                "//*[@class='pv-profile-section pv-accomplishments-section artdeco-container-card artdeco-card ember-view']"
            )
            for block in acc.find_elements(By.XPATH, 
                "//div[@class='pv-accomplishments-block__content break-words']"
            ):
                category = block.find_element(By.TAG_NAME, "h3")
                for title in block.find_element(By.TAG_NAME, 
                    "ul"
                ).find_elements(By.TAG_NAME, "li"):
                    accomplishment = Accomplishment(category.text, title.text)
                    self.add_accomplishment(accomplishment)
        except:
            pass

        # get connections
        try:
            driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mn-connections"))
            )
            connections = driver.find_element(By.CLASS_NAME, "mn-connections")
            if connections is not None:
                for conn in connections.find_elements(By.CLASS_NAME, "mn-connection-card"):
                    anchor = conn.find_element(By.CLASS_NAME, "mn-connection-card__link")
                    url = anchor.get_attribute("href")
                    name = conn.find_element(By.CLASS_NAME, "mn-connection-card__details").find_element(By.CLASS_NAME, "mn-connection-card__name").text.strip()
                    occupation = conn.find_element(By.CLASS_NAME, "mn-connection-card__details").find_element(By.CLASS_NAME, "mn-connection-card__occupation").text.strip()

                    contact = Contact(name=name, occupation=occupation, url=url)
                    self.add_contact(contact)
        except:
            connections = None

        if close_on_complete:
            driver.quit()

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
        return "<Person {name}\n\nAbout\n{about}\n\nExperience\n{exp}\n\nEducation\n{edu}\n\nInterest\n{int}\n\nAccomplishments\n{acc}\n\nContacts\n{conn}>".format(
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