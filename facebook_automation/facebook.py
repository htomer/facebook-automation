import re
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

FACEBOOK_URL = "https://www.facebook.com"


class Credentials():
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return "%s(email=%r, pass=%r)" % (self.__class__.__name__, self.email, self.password)


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

    @staticmethod
    def _extract_number(text: str):
        # Use regular expressions to extract the number and the multiplier (if any)
        match = re.search(r'(\d+(\.\d+)?)([Kk]?)\s+members', text)

        if match:
            number_str, _, multiplier = match.groups()

            # Convert the number to a float (if there's a decimal point)
            number = float(number_str)

            # Adjust the number based on the multiplier
            if multiplier.lower() == 'k':
                number *= 1000  # 1K means 1000
            return int(number)  # Convert the result to an integer

        return None  # Return None if no match is found

    def _extract_group_data(self, group: WebElement) -> tuple:
        # Get the raw inner text of the group and split to lines.
        lines = group.get_property("innerText").splitlines()

        # Extract the name of the group from the first line.
        name = lines[0]

        # Extract basic data of the group from the second line.
        [option, members, posts, *_] = lines[1].split('·') + [None]*2

        # Convert the "members" string to an integer.
        members_int = self._extract_number(members)

        # Return a tuple containing the extracted data.
        return (name, option, members, posts, members_int)

    def _get_groups_data(self):
        ''' Funtion that reads all available group data and writes it to a file. '''
        groups = self.driver.find_elements(By.CLASS_NAME, "x1yztbdb")

        for group in groups:

            # Extract group data line from the group.
            yield self._extract_group_data(group)

    def search_groups(self, keyword: str, count: int = 3) -> list:
        self.driver.get(FACEBOOK_URL + "/groups/feed/")

        wait = WebDriverWait(self.driver, 30)
        search_bar = self.driver.find_element(
            By.XPATH, "//input[@aria-label='Search groups']")

        search_bar.clear()
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)

        # Empty set for group data.
        groups = set()

        while len(groups) < count:
            try:
                # Wait for the search results to load
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@role, 'feed')]")))

                # Allow time for new results to load
                time.sleep(3)

                # Get all groups data.
                for group_data in self._get_groups_data():
                    groups.add(group_data)

                # Allow time for new results to load
                time.sleep(10 + random.randint(0, 25))

                # Scroll down to load more results
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")

            except Exception as e:
                print(f"Error collecting group names: {e}")
                break

        return sorted(groups, key=lambda item: item[-1], reverse=True)
