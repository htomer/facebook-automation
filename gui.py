import threading
import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from tkinter import ttk
from tkinter import messagebox
from typing import Callable
from ttkthemes import ThemedStyle

from facebook_automation.config import Config
from facebook_automation.credentials import Credentials
from facebook_automation.facebook import Facebook
from facebook_automation.groups import groups_save_to_file


class BarFrame(tk.Frame):
    def __init__(self, parent, button_command, button_text):
        super().__init__(parent)

        self.config(pady=0)  # Set frame parameters.

        self.button_text = button_text
        if (button_command is not None):
            # Add button.
            self.button = tk.Button(self, text=button_text, padx=5, pady=5,
                                    command=button_command)
        else:
            self.button = None

    def button_set_text(self, text: str):
        self.button['text'] = text

    def button_set_state(self, enable: bool):
        if enable:
            state = tk.NORMAL
        else:
            state = tk.DISABLED

        if self.button is not None:
            # Set button state.
            self.button['state'] = state


class TopBarFrame(BarFrame):
    def __init__(self, parent, controller, button_command=None, button_text=""):
        super().__init__(parent, button_command=button_command, button_text=button_text)

        self.config(pady=0)  # Set frame parameters.

        if (self.button is not None):
            # Place button.
            self.button.place(x=5, y=5)

        self.controller = controller

        title_label = tk.Label(
            self, text="Facebook Groups Scraper", font=controller.boldfont, fg="red")
        title_label.pack(side=tk.TOP, pady=20)


class BottomBarFrame(BarFrame):
    def __init__(self, parent, controller, button_command=None, button_text="", mode='indeterminate'):
        super().__init__(parent, button_command=button_command, button_text=button_text)

        self.config(pady=0)  # Set frame parameters.
        self.mode = mode

        # Create a label at the bottom of the window
        bottom_label = tk.Label(
            self, text="Made in the Upper Galilee", font=controller.boldfont, fg="green")
        bottom_label.pack(side=tk.BOTTOM, pady=20)

        if (self.button is not None):
            # Place button.
            self.button.pack(side=tk.BOTTOM, pady=20)

        # save root reference
        self.bounce_speed = 18
        self.pb_length = 200

        # the progress bar will be referenced in the "bar handling" and "work" threads
        self.load_bar = ttk.Progressbar(self)
        # self.load_bar.pack(side="bottom", padx=10, pady=(0, 15))

        # the load_bar needs to be configured for indeterminate amount of bouncing
        self.load_bar.config(mode=self.mode,
                             maximum=200, value=0, length=self.pb_length)

        # Precentage label.
        self.precent_label = tk.Label(self, text="", font=controller.bigfont)

        # Version string.
        # app_version = tk.Label(self, text=__version__,
        #                       fg='#808080', padx=5, pady=5)
        # .pack(side=tk.LEFT,padx=5, pady=5)#
        # app_version.place(x=5, rely=1.0, y=-35)

    def start_bar(self):
        if (self.button is not None):
            # Remove button.
            self.button.pack_forget()

            # Disable button.
            self.button_set_state(False)

        # stop the indeterminate bouncing
        self.load_bar.stop()

        self.load_bar.pack(side=tk.BOTTOM, pady=(10, 30))
        self.load_bar.config(mode=self.mode, value=0, maximum=100)

        if self.mode == 'indeterminate':

            # Start the indeterminate bouncing
            self.load_bar.start(self.bounce_speed)
        else:

            self.precent_label.pack(side=tk.BOTTOM, pady=(5, 0))
            self.update_percentage(0)

    def stop_bar(self, enable_button=True):
        # stop the indeterminate bouncing
        self.load_bar.stop()

        # reconfigure the bar so it appears reset
        self.load_bar.config(value=0, maximum=0)

        if (self.button is not None):
            self.load_bar.pack_forget()
            self.precent_label.pack_forget()

            self.button.pack(side=tk.BOTTOM, pady=20)

            if enable_button:
                self.button_set_text(self.button_text)

            # Set button state.
            self.button_set_state(enable_button)

    def update_percentage(self, percent: float):
        # Update percantage of load bar.
        self.load_bar['value'] = percent

        # Update progress text.
        self.precent_label['text'] = f"{int(percent)}%"


class FbAutomationkApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Helvetica', size=20, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Setting the geometry i.e Dimensions
        self.geometry("500x400")

        # Setting the title.
        self.title("Facebook Groups Automation")

        # Create a themed style for widgets
        self.style = ThemedStyle(self)
        # You can change the theme to one you prefer
        self.style.set_theme("plastik")

        # Thread lists.
        self.threads_list: list[threading.Thread] = list()

        # Facebook instance.
        # self.facebook: Facebook = None
        self.facebook: Facebook = Facebook()
        self.config: Config = Config.load_from_file_yaml() or Config()
        print(self.config)

        # Padding.
        self.grid_padx = 30
        self.grid_pady = 20

        self.boldfont = tkfont.Font(family="Helvetica", size=16, weight='bold')
        self.bigfont = tkfont.Font(family="Helvetica", size=14)
        self.smallfont = tkfont.Font(family="Helvetica", size=10)
        self.option_add("*Font", self.bigfont)

        # Ad exit operation.
        self.protocol("WM_DELETE_WINDOW", self.exit)

        self.frames = {}
        for F in (LoginPage, GroupPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    @staticmethod
    def _thread_method(work: Callable, event: threading.Event, bar: BottomBarFrame):

        while True:
            try:
                event.wait()

                # Start bar.
                bar.start_bar()

                # Run thread work.
                work()

            except Exception as e:
                # Show error message.
                messagebox.showerror(type(e).__name__, e)

            finally:
                # Stop bar.
                bar.stop_bar()

                event.clear()

    def thread_init(self, work: Callable, event: threading.Event, bar: BottomBarFrame) -> Callable:
        # Initialize the work thread.
        work_thread = threading.Thread(
            target=lambda wrk=work, evt=event, br=bar: self._thread_method(wrk, evt, br), daemon=True, args=())

        # start the word handling thread.
        work_thread.start()

        # Add to threads list.
        self.threads_list.append(work_thread)

    def exit(self):
        print("exit")

        # Logout from facebook.
        self.facebook.logout()

        # Quit the program.
        self.quit()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller: FbAutomationkApp):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        top_bar_frame = TopBarFrame(
            self, controller)
        # Add the top bar frame to the window
        top_bar_frame.pack(side=tk.TOP, fill=tk.X)

        # Create event to trigger the work thread.
        login_event = threading.Event()

        bottom_bar_frame = BottomBarFrame(
            self, controller, login_event.set, "Login")
        # Add the top bar frame to the window
        bottom_bar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # init background thread.
        controller.thread_init(
            self.login, login_event, bottom_bar_frame)

        # Grid frame.
        app_frame = tk.Frame(self)
        app_frame.pack(side=tk.TOP,  padx=10, pady=20, fill=tk.Y, expand=True)

        # Email.
        self.email = tk.StringVar()
        inp_email = tk.Entry(
            app_frame, textvariable=self.email, font=controller.bigfont)
        inp_email.grid(column=1, row=0, sticky=tk.W,
                       padx=controller.grid_padx, pady=controller.grid_pady)

        lb_email = tk.Label(
            app_frame, text="Email", font=controller.bigfont)
        lb_email.grid(column=0, row=0, sticky=tk.W,
                      padx=controller.grid_padx, pady=controller.grid_pady)

        # Password.
        self.password = tk.StringVar()
        password_entry = tk.Entry(
            app_frame, textvariable=self.password, show="*", font=controller.bigfont)
        password_entry.grid(column=1, row=1, sticky=tk.W,
                            padx=controller.grid_padx, pady=controller.grid_pady)

        password_label = tk.Label(
            app_frame, text="Password", font=controller.bigfont)
        password_label.grid(column=0, row=1, sticky=tk.W,
                            padx=controller.grid_padx, pady=controller.grid_pady)

        app_frame.grid_columnconfigure(0)
        app_frame.grid_columnconfigure(1)

    def tkraise(self, aboveThis=None):
        # Load credentials from file.
        credentials = self.controller.config.credentials
        self.email.set(credentials.email)
        self.password.set(credentials.password)

        return super().tkraise(aboveThis)

    def login(self):

        # Get credentials from gui entries.
        credentials = Credentials(
            email=self.email.get(),
            password=self.password.get())

        # Login using credentials.
        self.controller.facebook.login(credentials)

        print("Login to facebook sucesfully.")
        self.controller.show_frame("GroupPage")

        # Set new credentials to the file.
        self.controller.config.credentials = credentials
        self.controller.config.dump_to_file_yaml()


class GroupPage(tk.Frame):

    def __init__(self, parent, controller: FbAutomationkApp):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        top_bar_frame = TopBarFrame(
            self, controller, self.logout, "Logout")
        # Add the top bar frame to the window
        top_bar_frame.pack(side=tk.TOP, fill=tk.X)

        # Create event to trigger the work thread.
        search_event = threading.Event()

        bottom_bar_frame = BottomBarFrame(
            self, controller, search_event.set, "Search")
        # Add the top bar frame to the window
        bottom_bar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # init background thread.
        controller.thread_init(
            self.search_groups, search_event, bottom_bar_frame)

        # Grid frame.
        app_frame = tk.Frame(self)
        app_frame.pack(side=tk.TOP,  padx=10, pady=20, fill=tk.Y, expand=True)

        # Search word.
        self.search_word = tk.StringVar()
        search_entry = tk.Entry(
            app_frame, textvariable=self.search_word, font=controller.bigfont)
        search_entry.grid(column=1, row=0, sticky=tk.W,
                          padx=controller.grid_padx, pady=controller.grid_pady)

        search_label = tk.Label(
            app_frame, text="Search Word", font=controller.bigfont)
        search_label.grid(column=0, row=0, sticky=tk.W,
                          padx=controller.grid_padx, pady=controller.grid_pady)

        # Number of groups.
        self.group_number = tk.StringVar()
        groups_entry = tk.Entry(
            app_frame, textvariable=self.group_number, font=controller.bigfont)
        groups_entry.grid(column=1, row=1, sticky=tk.W,
                          padx=controller.grid_padx, pady=controller.grid_pady)

        groups_label = tk.Label(
            app_frame, text="Number of groups", font=controller.bigfont)
        groups_label.grid(column=0, row=1, sticky=tk.W,
                          padx=controller.grid_padx, pady=controller.grid_pady)

        app_frame.grid_columnconfigure(0)
        app_frame.grid_columnconfigure(1)

    def tkraise(self, aboveThis=None):

        # Load credentials from file.
        config = self.controller.config
        self.search_word.set(config.keyword)
        self.group_number.set(config.count)

        return super().tkraise(aboveThis)

    def search_groups(self):
        print("Search for groups")

        # Get values from the GUI fields
        keyword = self.search_word.get()
        count = int(self.group_number.get())

        # Search for groups containing the requested keyword and get group names.
        group_data = self.controller.facebook.search_groups(keyword, count)

        # Save the group names to a file.
        groups_save_to_file(group_data)

    def logout(self):
        print("Logout")

        # Logout from facebook.
        self.controller.facebook.logout()

        # Go to login frame.
        self.controller.show_frame("LoginPage")


def run():
    # Run application.
    app = FbAutomationkApp()
    app.mainloop()


if __name__ == '__main__':
    run()
