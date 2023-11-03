import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from facebook_automation.credentials import Credentials
from facebook_automation.group import Group

FACEBOOK_URL = "https://www.facebook.com"


class Facebook:

    def __init__(self):

        self.option = Options()

        self.option.add_argument("--disable-infobars")
        self.option.add_argument("start-maximized")
        self.option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        self.option.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 2}
        )

        self.login_flag = False

    '''def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()'''

    def login(self, credentials: Credentials):
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.get(FACEBOOK_URL)

        self.driver.maximize_window()
        wait = WebDriverWait(self.driver, 30)
        email_field = wait.until(
            EC.presence_of_element_located((By.NAME, 'email')))
        time.sleep(1)
        email_field.send_keys(credentials.email)
        pass_field = wait.until(
            EC.presence_of_element_located((By.NAME, 'pass'))
        )
        time.sleep(1)
        pass_field.send_keys(credentials.password)
        pass_field.send_keys(Keys.RETURN)
        time.sleep(2)

        try:
            login_container = self.driver.find_element(
                By.CLASS_NAME, "login_form_container")

            error_message = login_container.get_property(
                "innerText").splitlines()[0]

        except NoSuchElementException:
            # Make sure logging succesfully.
            self.login_flag = True

        except Exception as e:
            raise e

        else:
            raise Exception(error_message)

    def logout(self):
        if not self.login_flag:
            return

        # Logout from Facebook.
        self.login_flag = False

        try:
            self.driver.close()
        except Exception:
            pass

    def search_groups(self, keyword: str, count: int) -> list[Group]:
        ''' Function for automates a search for groups related to a specified keyword 
            and returns a list of group results.

            Parameters:
                - keyword (str): The keyword used for the search query.
                - count (int): The minimum number of group results to return.

            Returns:
                - list: A list of group objects that match the keyword search.
        '''
        self.driver.get(FACEBOOK_URL + "/groups/feed/")

        wait = WebDriverWait(self.driver, 30)
        search_bar = self.driver.find_element(
            By.XPATH, "//input[@aria-label='Search groups']")

        search_bar.clear()
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)

        # Empty set for groups.
        groups: set[Group] = set()

        while len(groups) < count:

            # Wait for the search results to load
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@role, 'feed')]")))

            # Allow time for new results to load
            time.sleep(6)

            # Add new groups to the set.
            groups.update(Group.get_groups(self.driver))

            # Allow time for new results to load
            time.sleep(10 + random.randint(0, 25))

            # Scroll down to load more results
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

        return sorted(groups, key=lambda item: item.members_int, reverse=True)
