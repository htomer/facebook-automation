from dataclasses import dataclass
from typing import Iterator
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import re

GROUP_CLASS_NAME = "x1yztbdb"


@dataclass
class Group:
    name: str
    privacy: str
    members: str
    posts: str

    @property
    def members_int(self) -> int:
        # Use regular expressions to extract the number and the multiplier (if any)
        match = re.search(r'(\d+(\.\d+)?)([Kk]?)\s+members', self.members)

        if match:
            number_str, _, multiplier = match.groups()

            # Convert the number to a float (if there's a decimal point)
            number = float(number_str)

            # Adjust the number based on the multiplier
            if multiplier.lower() == 'k':
                number *= 1000  # 1K means 1000
            return int(number)  # Convert the result to an integer

        return None  # Return None if no match is found

    @classmethod
    def _get_group_from_element(cls, group: WebElement):
        # Get the raw inner text of the group and split to lines.
        lines = group.get_property("innerText").splitlines()

        # Extract the name of the group from the first line.
        name = lines[0]

        # Extract basic data of the group from the second line.
        [privacy, members, posts, *_] = lines[1].split('·') + [None]*2

        # Return a group instance containing the extracted data.
        return cls(name, privacy, members, posts)

    @classmethod
    def get_groups(cls, driver: WebDriver) -> Iterator:
        ''' Funtion that reads all available groups and creates a group instance for each one. '''
        groups = driver.find_elements(By.CLASS_NAME, GROUP_CLASS_NAME)

        for group in groups:
            # Extract group data line from the group.
            yield cls._get_group_from_element(group)

    def __hash__(self):
        return hash(tuple(self))

    def __iter__(self):
        return iter([self.name, self.privacy, self.members, self.posts, self.members_int])
