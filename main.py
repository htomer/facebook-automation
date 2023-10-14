
import time
from facebook_automation.facebook import Facebook


def main():
    with Facebook() as facebook:
        # Login to facebook.
        facebook.login()

        # Search for groups.
        groups = facebook.search_groups("Israel")

        time.sleep(300)
