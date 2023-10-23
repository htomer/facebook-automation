import tkinter as tk
import yaml
from ttkthemes import ThemedStyle

from facebook_automation.launcher import launch


class ConfigGUI:
    def __init__(self, root):
        self.root = root
        root.title("Facebook Group Scraper Config")

        # Set the initial size of the window (width x height)
        root.geometry("500x350")  # Adjust the size as needed

        # Create a themed style for widgets
        self.style = ThemedStyle(root)
        # You can change the theme to one you prefer
        self.style.set_theme("plastik")

        # Create a title label
        title_font = ("Arial", 20, "bold")  # Larger and bold
        bottom_font = ("Arial", 15, "bold")  # Larger and bold
        title_color = "red"  # Change title color
        title_label = tk.Label(
            root, text="Facebook Groups Scraper", font=title_font, fg=title_color)
        title_label.grid(row=0, column=0, columnspan=4,
                         pady=(20, 10), padx=10, sticky="ew")

        # Create labels and entry fields for each configuration parameter
        label_font = ("Arial", 14)  # Change font and size
        label_color = "blue"  # Change label color

        # Create labels
        labels = ["Username", "Password", "Search Word", "Number of Groups"]
        self.label_entries = []
        for i, label_text in enumerate(labels):
            label = tk.Label(root, text=label_text,
                             font=label_font, fg=label_color)
            label.grid(row=i + 1, column=0, pady=(5, 0))
            self.label_entries.append(label)

        # Create entry fields
        entry_font = ("Arial", 14)
        self.entries = []
        for i in range(len(labels)):
            entry = tk.Entry(root, font=entry_font)
            entry.grid(row=i + 1, column=1, pady=(5, 0))
            self.entries.append(entry)

        # Create an "Execute" button with custom style
        button_font = ("Arial", 16, "bold")  # Larger and bold
        button_bg = "#4CAF50"  # Green background color
        button_fg = "white"  # White text color

        self.execute_button = tk.Button(
            root, text="Execute", command=self.execute, font=button_font, bg=button_bg, fg=button_fg)
        self.execute_button.grid(
            row=len(labels) + 1, column=0, columnspan=4, pady=(20, 0))

        # Create a label at the bottom of the window
        bottom_label = tk.Label(
            root, text="Made in the Upper Galilee", font=bottom_font, fg="green")
        bottom_label.grid(row=len(labels) + 2, column=0,
                          columnspan=4, pady=(20, 10))

        # Configure grid layout to centralize widgets
        for i in range(len(labels) + 3):
            root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(2, weight=1)

    def execute(self):
        # Get values from the GUI fields
        username = self.entries[0].get()
        password = self.entries[1].get()
        search_word = self.entries[2].get()
        num_groups = int(self.entries[3].get())

        # Create a dictionary with the updated configuration
        config_data = {
            "keyword": search_word,
            "count": num_groups,
            "credentials": {
                "email": username,
                "password": password
            }
        }

        # Write the updated configuration to the config file
        with open("config.yml", "w") as config_file:
            yaml.dump(config_data, config_file)

        # Close the GUI
        self.root.destroy()

        # Now you can launch the main program with the updated config file
        self.launch_main_program()

    def launch_main_program(self):
        launch()


if __name__ == "__main__":
    root = tk.Tk()
    config_gui = ConfigGUI(root)
    root.mainloop()
