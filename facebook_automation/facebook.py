import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FACEBOOK_URL = "https://www.facebook.com"


class Facebook:

    def __init__(self, file: str = 'facebook_credentials.txt'):

        self.file = file

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
        # extract username + password.
        with open(self.file) as file:
            EMAIL = file.readline().split('"')[1]
            PASSWORD = file.readline().split('"')[1]

        self.driver.maximize_window()
        wait = WebDriverWait(self.driver, 30)
        email_field = wait.until(
            EC.visibility_of_element_located((By.NAME, 'email')))
        email_field.send_keys(EMAIL)
        pass_field = wait.until(
            EC.visibility_of_element_located((By.NAME, 'pass')))
        pass_field.send_keys(PASSWORD)
        pass_field.send_keys(Keys.RETURN)

        time.sleep(2)

    def search_groups(self, group_name: str, group_num: int = 3):
        self.driver.get(FACEBOOK_URL + "/groups/feed/")

        # Wait for the groups page to load.
        time.sleep(5)

        search_bar = self.driver.find_element(
            By.XPATH, "//input[@aria-label='Search groups']")

        search_bar.clear()
        search_bar.send_keys(group_name)
        search_bar.send_keys(Keys.RETURN)

        # Wait for the search results to load
        time.sleep(5)

        group_names = []

        # TODO: append all groups to list.

        return group_names
