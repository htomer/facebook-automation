
from facebook_automation.facebook import Credentials, Facebook
import yaml


class Config(yaml.YAMLObject):
    yaml_tag = u'!Config'

    def __init__(self, keyword: str, count: str, email: str, password: str):
        self.email = email
        self.password = password
        self.keyword = keyword
        self.count = count

    def __repr__(self) -> str:
        return "%s(keyword=%r, count=%r)" % (self.__class__.__name__, self.keyword, self.count)


def save_group_names_to_file(group_names: list, file_name: str = "group_names.txt"):
    with open(file_name, 'w', encoding="utf-8") as file:
        for name in group_names:
            file.write(name + '\n')


def main():
    # Load options file.
    config = yaml.load(open("config.yml"), Loader=yaml.Loader)
    print(config)

    # Load facebook credentials from config.
    creds = Credentials(config.email, config.password)

    # Initialize the Facebook class
    with Facebook(creds) as facebook:
        # Login to Facebook.
        facebook.login()

        # Search for groups containing the keyword "israel" and get group names.
        group_names = facebook.search_groups(config.keyword, config.count)

        # Save the group names to a file.
        save_group_names_to_file(group_names)


if __name__ == "__main__":
    main()
