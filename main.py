
from facebook_automation.facebook import Facebook


def save_group_names_to_file(group_names: list, file_name: str = "group_names.txt"):
    with open(file_name, 'w', encoding="utf-8") as file:
        for name in group_names:
            file.write(name + '\n')


def main():
    # Initialize the Facebook class
    with Facebook() as facebook:
        # Login to Facebook.
        facebook.login()

        # Search for groups containing the keyword "israel" and get group names.
        group_names = facebook.search_groups("israel", count=30)

        # Save the group names to a file.
        save_group_names_to_file(group_names)


if __name__ == "__main__":
    main()
