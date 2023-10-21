import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from facebook_automation.credentials import Credentials
from facebook_automation.group import Group

FACEBOOK_URL = "https://www.facebook.com"


class Facebook:

    def __init__(self, credentials: Credentials):

        self.credentials = credentials

    def __enter__(self):
        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 2}
        )

        self.driver = webdriver.Chrome(options=option)
        self.driver.get(FACEBOOK_URL)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def login(self):
        self.driver.maximize_window()
        wait = WebDriverWait(self.driver, 30)
        email_field = wait.until(
            EC.presence_of_element_located((By.NAME, 'email')))
        time.sleep(1)
        email_field.send_keys(self.credentials.email)
        pass_field = wait.until(
            EC.presence_of_element_located((By.NAME, 'pass'))
        )
        time.sleep(1)
        pass_field.send_keys(self.credentials.password)
        pass_field.send_keys(Keys.RETURN)
        time.sleep(2)

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
            try:
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

            except Exception as e:
                print(f"Error collecting group names: {e}")
                break

        return sorted(groups, key=lambda item: item.members_int, reverse=True)
