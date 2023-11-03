
from facebook_automation.config import Config
from facebook_automation.facebook import Facebook
from facebook_automation.groups import groups_save_to_file


def main():
    # Read configs from file.
    config = Config.load_from_file_yaml()
    if config is None:

        # Dump default configs.
        Config().dump_to_file_yaml()
        return

    # Initialize the Facebook class
    facebook = Facebook()

    # Login to Facebook.
    facebook.login(config.credentials)

    # Search for groups containing the requested keyword and get group names.
    group_data = facebook.search_groups(config.keyword, config.count)

    # Save the group names to a file.
    groups_save_to_file(group_data)


if __name__ == "__main__":
    main()
