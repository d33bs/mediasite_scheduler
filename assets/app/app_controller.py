"""
Class for controller of gui-based medaisite scheduler.

Last modified: Feb 2018
By: Dave Bunten

License: MIT - see license.txt
"""

import os
import sys
import logging
import datetime
import csv
import tempfile
import shutil
from PyQt5 import uic, QtWidgets, QtCore, QtGui
import assets.mediasite.controller as mediasite_controller
import config.config as config

class app_controller():
    def __init__(self, view, logfile_path):
        """
		params:
			view: application view which is related to this controller class
            logfile_path: path to the current logfile
		"""

        self.view = view
        self.logfile_path = logfile_path
        self.central_log_dir = config.config_data["app_central_log_dir"]

        #check password on open of application
        #self.check_password(self.view.password_input_dialog("Please enter the password","Password"), config.config_data["app_secret"])

        #change the mouse cursor to show a wait icon
        self.view.set_mouse_cursor_wait()

        #creating mediasite model and controller to perform various tasks using the mediasite api client
        self.mediasite_controller = mediasite_controller.controller(config.config_data)
        self.mediasite_model = self.mediasite_controller.model

        if not self.mediasite_connection_validated():
            logging.error("Encountered errors with Mediasite connection. Preventing run actions.")
        else:
            #populate gui elements with various data from mediasite system
            self.mediasite_controller.folder.gather_root_folder_id()
            self.view.set_templates(self.mediasite_controller.template.gather_templates())
            self.view.set_recorders(self.mediasite_controller.recorder.gather_recorders())
            self.view.set_tree_folders(self.mediasite_controller.folder.gather_folders())

        #gather current date and time for use as defaults within the application
        current_qtDate = QtCore.QDate.currentDate()
        current_qtTime = QtCore.QTime.currentTime()

        #set the default start and end date and times using the datetime gathered above
        self.view.date_schedule_start_date.setDate(current_qtDate)
        self.view.date_schedule_end_date.setDate(current_qtDate)
        self.view.time_schedule_start_time.setTime(current_qtTime)
        self.view.time_schedule_end_time.setTime(current_qtTime)

        #connect various listener functions for course information section based on text or index changes
        self.view.text_course_semester.textChanged.connect(self.change_course_text)
        self.view.text_course_subject.textChanged.connect(self.change_course_text)
        self.view.text_course_number.textChanged.connect(self.change_course_text)
        self.view.text_course_section.textChanged.connect(self.change_course_text)
        self.view.text_course_title.textChanged.connect(self.change_course_text)
        self.view.combo_schedule_recorder.currentIndexChanged.connect(self.change_course_text)

        #connect various listener functions for schedule information section based on text or index changes
        self.view.combo_schedule_recurrence.currentIndexChanged.connect(self.change_combo_recurrence)
        self.view.time_schedule_start_time.dateTimeChanged.connect(self.change_time)
        self.view.time_schedule_end_time.dateTimeChanged.connect(self.change_time)
        self.view.text_schedule_duration.textChanged.connect(self.change_duration)
        self.view.tree_folder_location.itemSelectionChanged.connect(self.change_folder_selection)
        self.view.check_catalog_include.stateChanged.connect(self.change_catalog_include)
        self.view.check_module_include.stateChanged.connect(self.change_module_include)

        #connect listener function for run button click
        self.view.button_submit.clicked.connect(self.click_run_button)

        #top menu item actions
        self.view.menu_help_about.triggered.connect(self.click_menu_about)
        self.view.menu_file_batch_import.triggered.connect(self.click_menu_batch_import)
        self.view.menu_file_reconnect.triggered.connect(self.click_menu_reconnect)

        #change the mouse cursor to show a wait icon
        self.view.set_mouse_cursor_default()

    def click_run_button(self):
        """
		Performs actions based on information provided through GUI
		"""

        #change the mouse cursor to show a wait icon
        self.view.set_mouse_cursor_wait()

        #gather current user-entered 
        schedule_data = self.gather_mediasite_schedule_data()

        result = self.mediasite_controller.process_scheduling_data_row(schedule_data)

        #validate user entered data, stop run actions if errors are encountered
        if "error" in result.keys():
            logging.error("Encountered errors with user entered data. Preventing run actions.")
            self.view.error_dialog("Error", result["error"])
            self.view.set_mouse_cursor_default()
            return
        else:
            results_string = self.interpret_mediasite_controller_processing_results([result])

            self.create_run_log("single",results_string)

            logging.info("Finished creating single schedule!")

            #change the mouse cursor to show a wait icon
            self.view.set_mouse_cursor_default()

            self.view.more_info_dialog("Success!", 
                                    "Schedule creation complete. Please see details for more information.", 
                                    results_string
                                    )

            self.view.text_output.setPlainText(results_string)

        self.upload_centralized_logs()

    def click_menu_about(self):
        """
        Generate a help informational dialog containing information about the application
        """
        self.view.info_dialog("About Mediasite Scheduler","Mediasite Scheduler provides an alternative interface "+
            "for creating single or multiple (batch) Mediasite schedules, folders, catalogs, and modules at once.")

    def click_menu_batch_import(self):
        """
        Perform batch import using CSV spreadsheet obtained through file dialog
        """
        logging.info("Batch import starting. Seeking input file through file dialog.")

        #gather csv file path by having user select a file from a dialog
        csv_file_path = self.view.csv_file_dialog()[0]

        #check that our csv_file_path is not empty (in case user cancels the previous dialog)
        if csv_file_path is "":
            logging.error("No CSV file selected. Halting batch import process.")
            self.view.error_dialog("Error", "No CSV file selected. Please select a CSV file to perform a batch import.")
            return

        self.view.set_mouse_cursor_wait()

        logging.info("Attempting to read data found in CSV file: "+csv_file_path)

        #read csv data into list of dictionaries based on provided file path
        csv_data = self.read_csv_data_from_filepath(csv_file_path)

        logging.info("Beginning batch processing of csv data...")

        #send csv data to mediasite controller for batch data processing
        results = self.mediasite_controller.schedule.process_batch_scheduling_data(csv_data)

        logging.info("Finished batch processing!")

        results_string = self.interpret_mediasite_controller_processing_results(results)

        self.view.set_mouse_cursor_default()

        self.create_run_log("batch",results_string)

        self.view.more_info_dialog("Batch import complete!", 
                                    "Your batch import is now complete. Please see details for more information.", 
                                    results_string
                                    )

        self.upload_centralized_logs()

    def upload_centralized_logs(self):
        """
        function for uploading logs to a centralized location for analysis
        """
        shutil.copy2(self.logfile_path, self.central_log_dir)

    def interpret_mediasite_controller_processing_results(self, results):
        """
        Helper function to organize results of mediasite controller processing into user-friendly string

        params:
            results: list of dictionaries containing various results from medaisite controller processing

        returns:
            results_string: user-friendly string with results from medaisite controller processing
        """
        results_string = ""

        for row in results:
            for key,val in row.items():
                if key == "error":
                    results_string += val + "\n\n"
                    break
                elif key == "schedule_result":
                    if val["folder_directory"] == "":
                        results_string += "Schedule: " + val["Name"] + " : " + self.view.get_folder_pathway() + "\n"
                    else:
                        results_string += "Schedule: " + val["Name"] + " : " + val["folder_directory"] + "\n"
                elif key == "catalog_result":
                    results_string += "Catalog: " + val["Name"] + " : " + val["CatalogUrl"] +"\n\n"

        if results_string == "":
            results_string = "Successfully created schedule."

        return results_string

    def read_csv_data_from_filepath(self, csv_file_path):
        """
        Read csv data into dictionary using provided file path

        params:
            csv_file_path: file path containing a csv file

        returns:
            list of dictionary data compiled from the provided csv file
        """

        #read csv data into list of dictionaries based on provided file path
        csv_data = []
        reader = csv.DictReader(open(csv_file_path, 'r'))
        for line in reader:
            csv_data.append(line)

        return csv_data

    def click_menu_reconnect(self):
        """
        Generate a help informational dialog containing information about the application
        """

        #change the mouse cursor to show a wait icon
        self.view.set_mouse_cursor_wait()

        if not self.mediasite_connection_validated():
            logging.error("Encountered errors with Mediasite connection. Preventing run actions.")
        else:
            logging.info("Successfully validated Mediasite connection.")
            self.view.info_dialog("Success","Successfully validated Mediasite connection.")

        #change the mouse cursor to show a wait icon
        self.view.set_mouse_cursor_default()

    def mediasite_connection_validated(self):
        """
        Validate Mediasite connection and return dialog if there are any issues.

        returns:
            true if no errors were encountered, false if any errors were encountered
        """

        if not self.mediasite_controller.connection_validated(): 
            self.view.error_dialog('Error',"Mediasite connection issues. Please select File -> Reconnect to validate connection. See log for more details.")
            return False

        else:
            return True

    def change_catalog_include(self):
        """
		Change the catalog section of the GUI based on catalog include checkbox
		"""

        if self.view.check_catalog_include.isChecked():
            self.view.check_catalog_downloads.setEnabled(True)
            self.view.check_catalog_allow_links.setEnabled(True)
            self.view.text_catalog_title.setEnabled(True)
            self.view.label_catalog_title.setEnabled(True)
            self.view.label_catalog_desc.setEnabled(True)
            self.view.text_catalog_desc.setEnabled(True)

        else:
            self.view.check_catalog_downloads.setEnabled(False)
            self.view.check_catalog_allow_links.setEnabled(False)
            self.view.text_catalog_title.setEnabled(False)
            self.view.label_catalog_title.setEnabled(False)
            self.view.label_catalog_desc.setEnabled(False)
            self.view.text_catalog_desc.setEnabled(False)


    def change_module_include(self):
        """
        Change the module section of the GUI based on catalog include checkbox
        """

        if self.view.check_module_include.isChecked():
            self.view.label_module_name.setEnabled(True)
            self.view.text_module_name.setEnabled(True)
            self.view.label_module_moduleid.setEnabled(True)
            self.view.text_module_moduleid.setEnabled(True)

        else:
            self.view.label_module_name.setEnabled(False)
            self.view.text_module_name.setEnabled(False)
            self.view.label_module_moduleid.setEnabled(False)
            self.view.text_module_moduleid.setEnabled(False)

    def change_course_text(self):
        """
		Performs automatic naming convention changes based on course section information changes

		Note:
			These will be specific to each individual administration practice and are subject to change.
		"""

		#create temporary placeholders which prepare the components of presentation or catalog naming
        c_semester = self.view.text_course_semester.text().upper()
        c_subject = self.view.text_course_subject.text().upper()
        c_number = self.view.text_course_number.text().upper()
        c_section_title = self.view.text_course_section.text().upper().replace(" ","_")
        c_section = self.view.text_course_section.text().upper()
        c_title = self.view.text_course_title.text()
        c_recorder = self.view.combo_schedule_recorder.currentText().replace("-","")

        #set the full versions of presentation, catalog, or folder naming based on conventions
        self.view.text_schedule_title.setText(c_subject+c_number+"_"+c_section_title+"_"+c_recorder)
        self.view.text_folder_location.setText(c_subject+"/"+c_number+"/"+c_section)
        self.view.text_catalog_title.setText(c_subject+" "+c_number+" "+c_section+" "+c_semester)
        self.view.text_module_name.setText(c_subject+" "+c_number+" "+c_section+" "+c_semester)
        self.view.text_catalog_desc.setPlainText(c_title)

    def change_time(self):
        """
		Change the catalog section of the GUI based on catalog include checkbox
		"""
        if not self.view.text_schedule_duration.hasFocus():
            time_difference_in_minutes = str(int((self.view.time_schedule_start_time.time().secsTo(self.view.time_schedule_end_time.time()))/60))
            self.view.text_schedule_duration.setText(time_difference_in_minutes)

    def change_duration(self):
        """
		Performs automatic changes to the time duration based on the provided start and end times
		"""
        if(not self.view.time_schedule_start_time.hasFocus()
            and not self.view.time_schedule_end_time.hasFocus()
            and self.view.text_schedule_duration.text() != ""):

            new_end_time = self.view.time_schedule_start_time.time().addSecs(int(self.view.text_schedule_duration.text())*60)
            self.view.time_schedule_end_time.setTime(new_end_time)

    def change_combo_recurrence(self):
        """
		Change the week dates section of the GUI based on recurrence type dropdown
		"""

        if self.view.combo_schedule_recurrence.currentText() == "One Time Only":
            self.view.label_schedule_days_of_week.setEnabled(False)
            self.view.check_schedule_sunday.setEnabled(False)
            self.view.check_schedule_monday.setEnabled(False)
            self.view.check_schedule_tuesday.setEnabled(False)
            self.view.check_schedule_wednesday.setEnabled(False)
            self.view.check_schedule_thursday.setEnabled(False)
            self.view.check_schedule_friday.setEnabled(False)
            self.view.check_schedule_saturday.setEnabled(False)
            self.view.label_schedule_recurrence_freq.setEnabled(False)
            self.view.text_schedule_recurrence_freq.setEnabled(False)
        else:
            self.view.label_schedule_days_of_week.setEnabled(True)
            self.view.check_schedule_sunday.setEnabled(True)
            self.view.check_schedule_monday.setEnabled(True)
            self.view.check_schedule_tuesday.setEnabled(True)
            self.view.check_schedule_wednesday.setEnabled(True)
            self.view.check_schedule_thursday.setEnabled(True)
            self.view.check_schedule_friday.setEnabled(True)
            self.view.check_schedule_saturday.setEnabled(True)
            self.view.label_schedule_recurrence_freq.setEnabled(True)
            self.view.text_schedule_recurrence_freq.setEnabled(True)

    def change_folder_selection(self):
        """
		Change the selected mediasite root folder ID based on changes within the GUI
		"""

        if not self.mediasite_connection_validated():
            logging.error("Encountered errors with Mediasite connection. Preventing run actions.")
            return

        current_item = self.view.tree_folder_location.currentItem()
        selected_id = current_item.data(1,0)
        if current_item.childCount() == 0 and selected_id != "None":
             self.view.set_tree_folders(self.mediasite_controller.folder.gather_folders(selected_id),selected_id)

    def gather_mediasite_schedule_data(self):
        """
        Parse, convert, and request mediasite schedule creation

        Note - default date time formats:
            QT: Wed Nov 22 14:11:32 2017
            Mediasite: 9999-12-31T23:59:59

        params:
            parent_folder_id: mediasite folder id which the schedule will be associated with
       returns:
            mediasite api output for schedule creation
        """
        local_start_datetime_string = QtCore.QDateTime(self.view.date_schedule_start_date.date(),
                                                self.view.time_schedule_start_time.time()).toString("yyyy-MM-ddTHH:mm:ss")
        local_end_datetime_string = QtCore.QDateTime(self.view.date_schedule_end_date.date(),
                                                self.view.time_schedule_end_time.time()).toString("yyyy-MM-ddTHH:mm:ss")

        #find UTC times for datetimes due to Mediasite requirements
        local_start_datetime = datetime.datetime.strptime(local_start_datetime_string, "%Y-%m-%dT%H:%M:%S")
        local_end_datetime = datetime.datetime.strptime(local_end_datetime_string, "%Y-%m-%dT%H:%M:%S")
        utc_start_datetime = self.mediasite_controller.schedule.convert_datetime_local_to_utc(local_start_datetime)
        utc_end_datetime = self.mediasite_controller.schedule.convert_datetime_local_to_utc(local_end_datetime)
        utc_start_datetime_string = utc_start_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        utc_end_datetime_string = utc_end_datetime.strftime("%Y-%m-%dT%H:%M:%S")

        schedule_data = {
            "mediasite_folder_root_id":self.view.tree_folder_location.currentItem().data(1,0) if self.view.tree_folder_location.currentItem() != None else "",
            "mediasite_folders":self.view.text_folder_location.text(),
            "catalog_include":self.view.check_catalog_include.isChecked(),
            "catalog_name":self.view.text_catalog_title.text(),
            "catalog_description":self.view.text_catalog_desc.toPlainText(),
            "catalog_enable_download":self.view.check_catalog_downloads.isChecked(),
            "catalog_allow_links":self.view.check_catalog_allow_links.isChecked(),
            "module_include":self.view.check_module_include.isChecked(),
            "module_name":self.view.text_module_name.text(),
            "module_id":self.view.text_module_moduleid.text(),
            "schedule_parent_folder_id":"",
            "schedule_template":self.view.combo_schedule_template.currentText(),
            "schedule_name":self.view.text_schedule_title.text(),
            "schedule_naming_scheme":self.view.combo_schedule_naming_scheme.currentText(),
            "schedule_recorder":self.view.combo_schedule_recorder.currentText(),
            "schedule_recurrence":self.view.combo_schedule_recurrence.currentText(),
            "schedule_auto_delete":"True" if self.view.check_schedule_auto_delete.isChecked() else "False",
            "schedule_start_datetime_utc_string":utc_start_datetime_string,
            "schedule_end_datetime_utc_string":utc_end_datetime_string,
            "schedule_start_datetime_utc":utc_start_datetime,
            "schedule_end_datetime_utc":utc_end_datetime,
            "schedule_start_datetime_local_string":local_start_datetime_string,
            "schedule_end_datetime_local_string":local_end_datetime_string,
            "schedule_start_datetime_local":local_start_datetime,
            "schedule_end_datetime_local":local_end_datetime,
            "schedule_duration":self.view.text_schedule_duration.text(),
            "schedule_recurrence_freq":self.view.text_schedule_recurrence_freq.text(),
            "schedule_days_of_week":{
                "Sunday":self.view.check_schedule_sunday.isChecked(),
                "Monday":self.view.check_schedule_monday.isChecked(),
                "Tuesday":self.view.check_schedule_tuesday.isChecked(),
                "Wednesday":self.view.check_schedule_wednesday.isChecked(),
                "Thursday":self.view.check_schedule_thursday.isChecked(),
                "Friday":self.view.check_schedule_friday.isChecked(),
                "Saturday":self.view.check_schedule_saturday.isChecked()
                }
            }

        return schedule_data

    def create_run_log(self, result_type, results_string):
        """
        Create a run log of any processed results

        params:
            result_type: "single" or "batch" depending on the nature of the results
            results_string: string which contains relevant information on processed schedule information
        """
        current_datetime_string = '{dt.month}-{dt.day}-{dt.year}_{dt.hour}-{dt.minute}-{dt.second}'.format(dt = datetime.datetime.now())

        if not os.path.exists(tempfile.gettempdir()+"/mediasite_scheduler/"):
            os.makedirs(tempfile.gettempdir()+"/mediasite_scheduler/")

        with open(tempfile.gettempdir()+"/mediasite_scheduler/"+result_type+"_process_result_"+current_datetime_string+".log", "w") as log_file:
            log_file.write(results_string)

    def check_password(self, user_answer, secret):
        """
        Performs simple check against password

        params:
            password: user-provided text for entered password
        """

        if user_answer != secret:
            self.view.error_dialog("Error","Incorrect password. Closing application.")
            sys.exit(1)
            