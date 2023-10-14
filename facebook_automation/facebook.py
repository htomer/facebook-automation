import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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
        email_field.send_keys(self.credentials.email)
        pass_field = wait.until(
            EC.presence_of_element_located((By.NAME, 'pass'))
        )
        pass_field.send_keys(self.credentials.password)
        pass_field.send_keys(Keys.RETURN)

        time.sleep(2)

    def search_groups(self, keyword: str, count: int = 3) -> list:
        self.driver.get(FACEBOOK_URL + "/groups/feed/")

        wait = WebDriverWait(self.driver, 30)
        search_bar = self.driver.find_element(
            By.XPATH, "//input[@aria-label='Search groups']")

        search_bar.clear()
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)

        group_names = set()

        while len(group_names) < count:
            try:
                # Wait for the search results to load
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@role, 'feed')]")))

                group_elements = self.driver.find_elements(
                    By.XPATH, f"//a[contains(text(), '{keyword}')]")
                for group_element in group_elements:
                    group_name = group_element.text
                    group_names.add(group_name)
                    if len(group_names) >= count:
                        break

                # Scroll down to load more results
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")

                # Allow time for new results to load
                time.sleep(2)

            except Exception as e:
                print(f"Error collecting group names: {e}")
                break

        return list(group_names)
