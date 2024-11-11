import customtkinter
import datetime
import vibration_patterns
import inspect
import random
import serial
import atexit
import time
import pandas as pd
from tkinter import filedialog
import os
from serial.tools import list_ports

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
        self.begin_experiment_frame.grid(row=0, column=1, columnspan = 2, rowspan = 2, padx=(20, 0), pady=(10, 10), sticky="nsew")
        self.begin_experiment_frame.rowconfigure(4, weight = 1)

        #add label at top of frame
        self.experiment_frame_label = customtkinter.CTkLabel(self.begin_experiment_frame, text = "Experiment Setup", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.experiment_frame_label.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2, sticky ="nsew")

        # Add subject id with input textbox
        self.ID_entry_label = customtkinter.CTkLabel(self.begin_experiment_frame, text = "Subject ID:")
        self.ID_entry_label.grid(row = 1, column = 0, padx = 20, pady = 10, sticky ="nsew")
        self.ID_entry = customtkinter.CTkEntry(self.begin_experiment_frame, placeholder_text="Subject ID")
        self.ID_entry.grid(row=1, column=1, padx=(20, 20), pady=(10), sticky="nsew")

        # Get a list of all the collections of vibration types found in vibration_patterns
        self.trial_groups = [name for name, obj in inspect.getmembers(vibration_patterns) 
              if isinstance(obj, dict) and not name.startswith('__')]
        
        # add a trial group dropdown
        self.trial_group_label = customtkinter.CTkLabel(self.begin_experiment_frame, text = "Trial Group")
        self.trial_group_label.grid(row = 2, column = 0, padx = 20, pady = 10, sticky ="nsew")
        self.trial_group_dropdown = customtkinter.CTkComboBox(self.begin_experiment_frame, values=self.trial_groups, state="readonly")
        self.trial_group_dropdown.grid (row = 2, column = 1, padx = 20, pady = 10, sticky= "nsew")

        # Add session dropbox (in pocket or in hand)
        self.session_selection_label = customtkinter.CTkLabel(self.begin_experiment_frame, text = "Session Type:")
        self.session_selection_label.grid(row = 3, column = 0, padx = 20, pady = 10, sticky ="nsew")
        self.session_selection_dropdown = customtkinter.CTkComboBox(self.begin_experiment_frame, values=["Pocket", "Hand"], state="readonly")
        self.session_selection_dropdown.grid (row = 3, column = 1, padx = 20, pady = 10, sticky= "nsew")

        #TODO: Maybe add other parameters, age, Height, Weight, etc. Any other info you want in the header.

        # Begin experiment button
        self.begin_experiment_button = customtkinter.CTkButton(master=self.begin_experiment_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Begin Experiment", command=self.begin_experiment)
        self.begin_experiment_button.grid(row=5, column=0, columnspan = 2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #create the experiment frame
        self.experiment_frame = customtkinter.CTkFrame(self)
        self.experiment_frame.grid(row=0, column=3, columnspan = 2, rowspan = 2, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.experiment_frame.rowconfigure((0,3), weight = 1)
        self.experiment_frame.columnconfigure((0,3), weight = 1)

        # Set default values
        self.number_of_trials = 40

        # Set empty variables to fill later
        self.subject_ID = None
        self.selected_trial_group = None
        self.session = None
        self.export_results_directory = None
 
        self.buttons_list = []

        # create an empty dataframe to store results
        self.results = pd.DataFrame(columns = ["ID", "Trial Group", "Session", "Ground Truth", "Response"])

        # establish serial communication with Arduino
        self.com_port = "COM9"
        self.baud_rate = 9600

        self.establish_serial_com()
        #ensure that serial connection is properly closed when GUI is closed
        atexit.register(self.cleanup)

    def establish_serial_com(self):
        try:
            self.ser = serial.Serial(self.com_port, self.baud_rate)
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            popup = COMPortSelectorPopup(self)

    def cleanup(self):
        try:
            self.ser.close()
            print("Serial Connection Closed")
        except AttributeError as e:
            print(e)

    def open_settings_menu(self):
        self.settingsMenu = SettingsMenu(self)

    def begin_experiment(self):

        # Take the values from each input box and set them as the appropriate attribute

        #check if ID has been entered into Subject ID box. If not, stop and require user to enter ID before proceeding
        if self.ID_entry.get() != "":
            self.subject_ID = self.ID_entry.get()
        else:
            text = "Please enter subject ID."
            popup = MessagePopup(self, text)
            return
        
        if self.trial_group_dropdown.get() != "":
            self.selected_trial_group = self.trial_group_dropdown.get()
        else:
            text = "Please select trial group."
            popup = MessagePopup(self, text)
            return
        

        if self.session_selection_dropdown.get() != "":
            self.session = self.session_selection_dropdown.get()
        else:
            text = "Please select session type."
            popup = MessagePopup(self, text)
            return
        
        if self.export_results_directory is None:
            text = "Set directory to save results file in settings menu"
            popup = MessagePopup(self, text)
            return

        # Dynamically access the dictionary using the trial_group string
        self.trial_dict = getattr(vibration_patterns, self.trial_group_dropdown.get(), None)

        # Generate a list of trials, randomized order and roughly equal
        self.trial_list = self.create_trials(list(self.trial_dict.keys()), self.number_of_trials)

        # Disable the experiment setup pane so that you cannot change these values
        self.ID_entry.configure(state = "disabled")
        self.trial_group_dropdown.configure(state = "disabled")
        self.session_selection_dropdown.configure(state = "disabled")
        self.begin_experiment_button.configure(state = "disabled")
        self.vibration_demo_button.configure(state = "disabled")

        # Generate the name of the log file (.txt or .csv) for that experiment and store it as an attribute (ID_date_{training or testing})
        self.export_log_file_name = "TrialLog_" + self.subject_ID + "_" + self.selected_trial_group + "_" + self.session + "_" + datetime.datetime.now().strftime("%Y_%m_%d")  + ".csv"

        # Begin a countdown to starting the experiment
        self.beginning_experiment_text = customtkinter.CTkLabel(self.experiment_frame, text="Starting Experiment In:", font = ('CTkFont',50))
        self.beginning_experiment_text.grid(row=1, column = 1)

        # Schedule the update of the text after 1000 milliseconds (1 second)
        self.experiment_frame.after(1000, lambda: self.beginning_experiment_text.configure(text="3"))
        self.experiment_frame.after(2000, lambda: self.beginning_experiment_text.configure(text="2"))
        self.experiment_frame.after(3000, lambda: self.beginning_experiment_text.configure(text="1"))
        self.experiment_frame.after(4000, lambda: self.beginning_experiment_text.destroy())

        # Call the method to start the experiment after countdown
        self.experiment_frame.after(5000, lambda: self.run_trial(0))

    def run_trial(self, trial_index):
        if trial_index >= len(self.trial_list):
            self.export_log()
            return # All trials have been completed
        
        trial = self.trial_list[trial_index]
        delay = random.uniform(3, 7) # Generate a random delay between 3 and 7 seconds

        # Use after() to schedule the vibration sending after the delay
        self.experiment_frame.after(int(delay * 1000), lambda: self.send_vibration(trial, self.trial_dict))

        # Create buttons and wait for a response from the user
        self.experiment_frame.after(int((delay + 1) * 1000), lambda: self.create_buttons_and_wait_for_response(trial_index))

    def vibration_demo(self):
        self.vibration_demo_popup = VibrationDemoPopup(self)

    def export_log(self):
        file_path = os.path.join(self.export_results_directory, self.export_log_file_name)
        self.results.to_csv(file_path, index=False)
        message = "Experiment Complete! Results saved to:\n" + file_path.replace('\\', '/')
        popup = MessagePopup(self, message)
        popup.geometry("700x275")
        popup.title("Experiment Complete!")

        print("Results saved to: " + file_path)

    def send_vibration(self, notification_type, trial_dict):
        for i in trial_dict[notification_type]:
            
            # Try to send data to arduino
            try:
                self.ser.write(bytes([i[1]]))  # Send each value as a single byte
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                # TODO: Add a popup telling you what happened and allowing you to save results before study ends. Maybe allow you to attempt to reconnect?
                # Need to either make this end the actual study, or give you a chance to reconnect and reopen the serial port
                self.cleanup()
                break
            # print("Send '" + str(i[1]) + "' to arduino over serial")
            time.sleep(i[0]/1000)


    def create_trials(self, string_list, x):
        # Calculate the base number of repetitions for each string
        base_repetitions = x // len(string_list)
        
        # Calculate the remainder (extra strings to distribute)
        remainder = x % len(string_list)
        
        # Create a list where each string appears `base_repetitions` times
        trials = [s for s in string_list for _ in range(base_repetitions)]
        
        # Add one extra occurrence of some strings to handle the remainder
        trials.extend(string_list[:remainder])

        # Shuffle the list to randomize the order
        random.shuffle(trials)

        return trials

    def create_buttons_and_wait_for_response(self, trial_index):

        # Remove any previous buttons from the list
        for button in self.buttons_list:
            button.destroy()
        
        #clear the list
        self.buttons_list = []

        # Ensure the dictionary exists
        if self.trial_dict is not None:
            for i in self.trial_dict.keys():
                button = customtkinter.CTkButton(self.experiment_frame, text=i, command=lambda i=i: self.on_button_click(trial_index, i))
                button.pack(pady=10)
                self.buttons_list.append(button)  # Add button to the list
        else:
            print(f"Error: '{self.trial_dict}' is not a valid attribute in vibration_patterns.")



    def on_button_click(self, trial_index, button_text):
        # Handle the button click and proceed to the next trial
        # print(f"User clicked: {button_text}")

        # add trial to log
        self.results.loc[len(self.results)] = [self.subject_ID, self.selected_trial_group, self.session, self.trial_list[trial_index], button_text]

        # Remove the buttons
        for button in self.buttons_list:
            button.destroy()

        # Proceed to the next trial after a short delay
        self.experiment_frame.after(500, self.run_trial, trial_index + 1)
    


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
        self.title("Vibrations Demo")

        # Add a label
        self.label = customtkinter.CTkLabel(self, text="Select a Vibration Tone:", font=("Arial", 18))
        self.label.pack(pady=(20,10))

        # Select phone type
        self.dictionary_selection = customtkinter.CTkComboBox(self, values=self.main.trial_groups, state="readonly", command=self.create_buttons)
        self.dictionary_selection.pack(pady=10)

        #initialize empty button list
        self.buttons_list = []

        # Add a cancel button to the popup
        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.destroy)
        self.cancel_button.pack(pady=(30,10))
        self.buttons_list.append(self.cancel_button) # add to button list
        
        # Make sure the popup is modal (disables main window interaction)
        self.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)
        # self.transient(self.main) # set to be on top of the main window

    def create_buttons(self, trial_group):
        for i in self.buttons_list:
            i.destroy()
        
        #clear the list
        self.buttons_list = []

        # Dynamically access the dictionary using the trial_group string
        trial_dict = getattr(vibration_patterns, trial_group, None)

        # Ensure the dictionary exists
        if trial_dict is not None:
            for i in trial_dict.keys():
                button = customtkinter.CTkButton(self, text=i, command=lambda i=i: self.main.send_vibration(i, trial_dict))
                button.pack(pady=10)
                self.buttons_list.append(button)  # Add button to the list
        else:
            print(f"Error: '{trial_group}' is not a valid attribute in vibration_patterns.")

        # Regenerate the cancel button
        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.destroy)
        self.cancel_button.pack(pady=(30,10))
        self.buttons_list.append(self.cancel_button) # add to button list

class SettingsMenu(customtkinter.CTkToplevel):
    '''
    A popup to allow you to change settings
    '''
    def __init__(self, main):
        super().__init__()

        # make the main window an attribute of the popup so that it can access attributes of main window
        self.main = main

        # set size and title of popup
        self.geometry("450x275")
        self.title("Settings")

        # Number of Trials
        self.number_of_trials_label = customtkinter.CTkLabel(self, text="Number Of Trials:")
        self.number_of_trials_label.grid(row=0, column=0, padx=10, pady=20)

        self.number_of_trials_entry = customtkinter.CTkEntry(self)
        self.number_of_trials_entry.insert(0, self.main.number_of_trials)
        self.number_of_trials_entry.grid(row=0, column=1, padx=10, pady=20)

        # Directory to save results file
        self.data_export_directory_label = customtkinter.CTkLabel(self, text = "Save Results to:")
        self.data_export_directory_label.grid(row=1, column=0, padx=10, pady=20)

        self.data_export_directory_entry = customtkinter.CTkEntry(self)
        self.data_export_directory_entry.grid(row=1, column=1, padx=10, pady=20)
        
        self.select_data_export_directory_button = customtkinter.CTkButton(self, text="...", width=10, command= lambda: self.select_directory(self.data_export_directory_entry))
        self.select_data_export_directory_button.grid(row=1, column =2, padx=0, pady=20)


        # Add a save button to the popup
        self.save_button = customtkinter.CTkButton(self, text="Save", command=self.save_settings)
        self.save_button.grid(row = 3, column = 0, padx = 20, pady = 20)

        # Add a cancel button to the popup
        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row = 3, column = 1, padx = 20, pady = 20)



        # Make sure the popup is modal (disables main window interaction)
        self.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)
        # self.transient(self.main) # set to be on top of the main window

    def select_directory(self, directory_entry):

        file_path = filedialog.askdirectory(title="Select Folder:", mustexist=True)

        if file_path:
            directory_entry.delete(0, customtkinter.END) 
            directory_entry.insert(0, file_path)
        else:
            print("No folder chosen")


    def save_settings(self):
        '''
        for each setting, change the corresponding GUI variable to the new value
        set in the settings menu.

        Raise an error if data is wrong type before applying
        
        
        '''
        try:
            self.main.number_of_trials = int(self.number_of_trials_entry.get())
        except ValueError:
            text = "Number of Trials must be an integer"
            popup = MessagePopup(self, text)
            return
        
        if os.path.exists(self.data_export_directory_entry.get()):
            self.main.export_results_directory = self.data_export_directory_entry.get()
        else:
            text = "The directory provided is not valid. Please provide a valid directory."
            popup = MessagePopup(self, text)
            return


        # close the settings popup
        self.destroy()


class MessagePopup(customtkinter.CTkToplevel):
    '''
    A popup to allow you to provide a message
    '''
    def __init__(self, main, message):
        super().__init__()

        # make the main window an attribute of the popup so that it can access attributes of main window
        self.main = main

        # set size and title of popup
        self.geometry("450x275")
        self.title("Error")

        self.message = customtkinter.CTkLabel(self, text=message)
        self.message.pack(pady=10)

        # Add an "OK"  button to the popup
        self.cancel_button = customtkinter.CTkButton(self, text="OK", command=self.closeWindow)
        self.cancel_button.pack(pady=10)

        # Make sure the popup is modal (disables main window interaction)
        self.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)
        # self.transient(self.main) # set to be on top of the main window

    def closeWindow(self):
        '''Close the window and set grab_set() to appropriate precursor window'''
        self.main.grab_set()
        self.destroy()

class COMPortSelectorPopup(customtkinter.CTkToplevel):
    def __init__(self, main):
        super().__init__()

        # make the main window an attribute of the popup so that it can access attributes of main window
        self.main = main

        # set size and title of popup
        self.geometry("450x275")
        self.title("Select COM Port")

        self.protocol('WM_DELETE_WINDOW', exit)

        #initialize empty COM Port List
        self.COMPortList = []

        self.getCOMPorts()

        # Add the message
        self.message = customtkinter.CTkLabel(self, text="Select COM Port for Arduino Nano")
        self.message.pack(pady=10)

        # Select com port
        self.COMPort_selection = customtkinter.CTkComboBox(self, values=self.COMPortList, state="readonly")
        self.COMPort_selection.pack(pady=10)

        # Add a "Refresh List"  button to the popup
        self.refresh_list_button = customtkinter.CTkButton(self, text="Refresh List", command=self.refreshList)
        self.refresh_list_button.pack(pady=10)

        # Add Select button
        self.select_button = customtkinter.CTkButton(self, text="Select", command=self.selectCOM)
        self.select_button.pack(pady=10)

        # Add Cancel button
        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=exit)
        self.cancel_button.pack(pady=10)

        # Make sure the popup is modal (disables main window interaction)
        self.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)
        # self.transient(self.main) # set to be on top of the main window

    def getCOMPorts(self):
        # Now you can use list_ports to get available COM ports
        ports = list_ports.comports()
        self.COMPortList = [port.device for port in ports]

    def refreshList(self):
        self.getCOMPorts()
        self.COMPort_selection.configure(values=self.COMPortList)
    
    def selectCOM(self):
        self.main.com_port = self.COMPort_selection.get()
        self.destroy()
        self.main.establish_serial_com()






if __name__ == "__main__":
    app = App()
    app.mainloop()