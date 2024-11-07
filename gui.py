import tkinter
import tkinter.messagebox
import customtkinter
import datetime
import time


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Vibration Test")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure((0,1,2), weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Vibration Test", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.vibration_demo_button = customtkinter.CTkButton(self.sidebar_frame, command = self.vibration_demo, text="Vibration Demo")
        self.vibration_demo_button.grid(row=1, column=0, padx=20, pady=10)

        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, command=self.open_settings_menu, text="Settings")
        self.settings_button.grid(row=8, column=0, padx=20, pady=10)


        ##################################################################################################################
        #  This creates the experiment frame which allows you to input the subject ID, phone type, etc

        #create the frame
        self.begin_experiment_frame = customtkinter.CTkFrame(self)
        self.begin_experiment_frame.grid(row=0, column=1, columnspan = 2, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.begin_experiment_frame.rowconfigure(4, weight = 1)

        #add label at top of frame
        self.experiment_frame_label = customtkinter.CTkLabel(self.begin_experiment_frame, text = "Experiment Setup", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.experiment_frame_label.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2, sticky ="nsew")

        # Add subject id with input textbox
        self.ID_entry_label = customtkinter.CTkLabel(self.begin_experiment_frame, text = "Subject ID:")
        self.ID_entry_label.grid(row = 1, column = 0, padx = 20, pady = 10, sticky ="nsew")
        self.ID_entry = customtkinter.CTkEntry(self.begin_experiment_frame, placeholder_text="Subject ID")
        self.ID_entry.grid(row=1, column=1, padx=(20, 20), pady=(10), sticky="nsew")

        # Add phone type dropbox (iPhone or Android)
        self.phone_selection_label = customtkinter.CTkLabel(self.begin_experiment_frame, text = "Phone Type:")
        self.phone_selection_label.grid(row = 2, column = 0, padx = 20, pady = 10, sticky ="nsew")
        self.phone_selection_dropdown = customtkinter.CTkComboBox(self.begin_experiment_frame, values=["iPhone", "Android"], state="readonly")
        self.phone_selection_dropdown.grid (row = 2, column = 1, padx = 20, pady = 10, sticky= "nsew")

        #TODO: Maybe add other parameters, age, Height, Weight, etc. Any other info you want in the header.

        # Begin experiment button
        self.begin_experiment_button = customtkinter.CTkButton(master=self.begin_experiment_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Begin Experiment", command=self.begin_experiment)
        self.begin_experiment_button.grid(row=5, column=0, columnspan = 2, padx=(20, 20), pady=(20, 20), sticky="nsew")



        # TODO: set default values
        self.number_of_trials = 80 # TODO: Need to make this configurable in the settings menu

        # Set empty variables to fill later
        self.subject_ID = None
        self.phone_type = None
 

        self.current_trial = None





    def open_settings_menu(self):
        print("Open the settings menu")
        #TODO: Create a settings menu class that opens a separate popup

        
        # TODO: Make a Settings Menu Class that contains these items as well as the directories and saves them to a .txt file
        # self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        # self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        # self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
        #                                                                command=self.change_appearance_mode_event)
        # self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        # self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        # self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        # self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
        #                                                        command=self.change_scaling_event)
        # self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        #settings should also contain a default value for number of trials for a training session

    def begin_experiment(self):

        # Take the values from each input box and set them as the appropriate attribute

        #check if ID has been entered into Subject ID box. If not, stop and require user to enter ID before proceeding
        if self.ID_entry.get() != "":
            self.subject_ID = self.ID_entry.get()
        else:
            print("Must provide ID.")
            # TODO: add a popup here taht says "Please enter Subject ID"
            return
        

        if self.phone_selection_dropdown.get() != "":
            self.phone_type = self.phone_selection_dropdown.get()
        else:
            print("Must select phone type")
            # TODO: Add a popup here
            return

        #TODO: Import the proper dictionary from other file based on phone type. This will set the number of trial types based on the size of this dictionary.

        #TODO: generate a list of trials? - Needs to be equal number of trials and needs to be length of 

        # Set the trial counter to 0
        self.current_trial = 0

        # Disable the experiment setup pane so that you cannot change these values
        self.ID_entry.configure(state = "disabled")
        self.phone_selection_dropdown.configure(state = "disabled")
        self.begin_experiment_button.configure(state = "disabled")
        self.vibration_demo_button.configure(state = "disabled")

        # Generate the name of the log file (.txt or .csv) for that experiment and store it as an attribute (ID_date_{training or testing})
        self.export_log_file_name = "TrialLog_" + self.subject_ID + "_" + self.phone_type + "_" + datetime.datetime.now().strftime("%Y_%m_%d")  + ".csv"

        # TODO: Make second panel apear saying experiment beginning

        #create the frame
        self.experiment_frame = customtkinter.CTkFrame(self)
        self.experiment_frame.grid(row=0, column=3, columnspan = 2, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.experiment_frame.rowconfigure((0,3), weight = 1)
        self.experiment_frame.columnconfigure((0,3), weight = 1)
        self.beginning_experiment_text = customtkinter.CTkLabel(self.experiment_frame, text="Starting Experiment")
        self.beginning_experiment_text.grid(row=1, column = 1)


        # TODO: Begin experiment



    def vibration_demo(self):
        self.vibration_demo_popup = VibrationDemoPopup(self)

    def remove_trial(self):
        self.remove_trial_popup = RemoveTrialPopup(self)

    def export_log(self):
        print("exporting log")
        # TODO: Get directory from settings and file name from attribute
        # Determine if file exists
        # Need to figure out how to append data in real time so that you can continuously update throughout the study.
    


class VibrationDemoPopup(customtkinter.CTkToplevel):
    '''
    A popup to allow you to demo each vibration mode
    '''
    def __init__(self, main):
        super().__init__()

        # make the main window an attribute of the popup so that it can access attributes of main window
        self.main = main

        # set size and title of popup
        self.geometry("400x500")
        self.title("Add Trial")

        # Add a label
        self.label = customtkinter.CTkLabel(self, text="Select a Vibration Tone:", font=("Arial", 18))
        self.label.pack(pady=(20,10))

        # Select phone type
        self.phone_selection = customtkinter.CTkComboBox(self, values=["iPhone", "Android"], state="readonly")
        self.phone_selection.pack(pady=10)


        # Add a "Text" button to the popup
        self.add_button = customtkinter.CTkButton(self, text="Text Message")
        self.add_button.pack(pady=10)

        # Add an "Email" button to the popup
        self.add_button = customtkinter.CTkButton(self, text="Email")
        self.add_button.pack(pady=10)

        # Add an "Groupme" button to the popup
        self.add_button = customtkinter.CTkButton(self, text="GroupMe")
        self.add_button.pack(pady=10)

        # Add an "WhatsApp" button to the popup
        self.add_button = customtkinter.CTkButton(self, text="WhatsApp")
        self.add_button.pack(pady=10)
        

        # Add a cancel button to the popup
        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.destroy)
        self.cancel_button.pack(pady=(30,10))
        
        # Make sure the popup is modal (disables main window interaction)
        self.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)
        # self.transient(self.main) # set to be on top of the main window

    def send_vibration(self):
        # send the vibration to the esp with serial
        print("Sending Vibration")



if __name__ == "__main__":
    app = App()
    app.mainloop()