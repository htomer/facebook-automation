
from typing import Optional
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


def dump_default_config_to_file(file_name: str):
    default_config = {"keyword": "israel", "count": 30}
    default_creds = {"credentials": {"email": "EMAIL", "password": "PASSWORD"}}
    with open(file_name, "w") as file:
        yaml.dump(default_config, file)
        yaml.dump(default_creds, file)


def load_config_from_file(file_name: str = 'config.yml') -> Optional[Config]:
    try:
        # Load configs file.
        with open('config.yml', 'r') as yaml_file:
            config_data = yaml.load(yaml_file, Loader=yaml.FullLoader)

        # Load data from file into config intance.
        return Config(**config_data)
    except OSError as e:

        # Dump default configs.
        dump_default_config_to_file(file_name)

        return None


def main():
    # Read configs from file.
    config = load_config_from_file()

    if config is None:
        return

    # Initialize the Facebook class
    with Facebook(config.credentials) as facebook:
        # Login to Facebook.
        facebook.login()

        # Search for groups containing the requested keyword and get group names.
        group_names = facebook.search_groups(config.keyword, config.count)

        # Save the group names to a file.
        save_group_names_to_file(group_names)


if __name__ == "__main__":
    main()
