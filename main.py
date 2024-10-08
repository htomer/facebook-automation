
import csv
import os
from typing import Any, Iterable

from facebook_automation.config import Config
from facebook_automation.facebook import Facebook


def save_groups_to_file(group_data: Iterable[Iterable[Any]], file_name: str = "groups_output.csv"):
    def next_non_exists(f):
        fnew = f
        root, ext = os.path.splitext(f)
        i = 0
        while os.path.exists(fnew):
            i += 1
            fnew = '%s_%i%s' % (root, i, ext)
        return fnew

    with open(next_non_exists(file_name), 'w', encoding="utf-8-sig", newline='') as file:
        # create the csv writer
        writer = csv.writer(file)

        # write header.
        # writer.writerow("[name", "option", "members", "posts", "members_int"])

        # write data.
        writer.writerows(group_data)


def main():
    # Read configs from file.
    config = Config.load_from_file_yaml()
    if config is None:

        # Dump default configs.
        Config().dump_to_file_yaml()
        return

    # Initialize the Facebook class
    with Facebook(config.credentials) as facebook:
        # Login to Facebook.
        facebook.login()

        # Search for groups containing the requested keyword and get group names.
        group_data = facebook.search_groups(config.keyword, config.count)

    # Save the group names to a file.
    save_groups_to_file(group_data)


if __name__ == "__main__":
    main()
