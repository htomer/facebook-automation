
from facebook_automation.facebook import Credentials, Facebook
import yaml


class Config():

    def __init__(self, keyword: str, count: str, credentials):
        self.keyword = keyword
        self.count = count
        self.credentials = Credentials(**credentials)

    def __repr__(self) -> str:
        return "%s(keyword=%r, count=%r, %r)" % (self.__class__.__name__, self.keyword, self.count, self.credentials)


def save_group_names_to_file(group_names: list, file_name: str = "group_names.txt"):
    with open(file_name, 'w', encoding="utf-8") as file:
        for name in group_names:
            file.write(name + '\n')


def main():

    # Load options file.
    with open('config.yml', 'r') as yaml_file:
        config_data = yaml.load(yaml_file, Loader=yaml.FullLoader)

    # Load options into config intance.
    config = Config(**config_data)

    # Initialize the Facebook class
    with Facebook(config.credentials) as facebook:
        # Login to Facebook.
        facebook.login()

        # Search for groups containing the keyword "israel" and get group names.
        group_names = facebook.search_groups(config.keyword, config.count)

        # Save the group names to a file.
        save_group_names_to_file(group_names)


if __name__ == "__main__":
    main()
