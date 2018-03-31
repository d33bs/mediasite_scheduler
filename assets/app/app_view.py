"""
View for gui-based medaisite scheduler.

Last modified: Feb 2018
By: Dave Bunten

License: MIT - see license.txt
"""

import os
import sys
import logging
from PyQt5 import uic, QtWidgets, QtCore, QtGui

class app_view(QtWidgets.QMainWindow):
    def __init__(self, run_path):
        """
        params:
            run_path: root path where the application is being run from on the system
        """

        super(app_view, self).__init__()
        uic.loadUi(run_path+'/assets/ui/mediasite_scheduler.ui', self)

        self.run_path = run_path

        self.tree_folder_location.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents);

        self.onlyInt = QtGui.QIntValidator()
        self.text_schedule_duration.setValidator(self.onlyInt)

        self.setWindowTitle("Mediasite Scheduler")

        self.statusbar = self.statusBar()

        #self.statusbar.showMessage("Welcome to Medaisite Scheduler!")

        self.show()

    def set_mouse_cursor_wait(self):
        """
        Sets the mouse cursor to have a wait icon
        """
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

    def set_mouse_cursor_default(self):
        """
        Sets the mouse cursor to have default icon
        """
        QtWidgets.QApplication.restoreOverrideCursor()

    def set_templates(self, mediasite_templates):
        """
        Sets the templates in gui dropdown based on list of template names provided

        params:
            mediasite_templates: list of mediasite template names
        """

        for template in mediasite_templates:
            self.combo_schedule_template.addItem(template["Name"])

    def set_recorders(self, mediasite_recorders):
        """
        Sets the recorders in gui dropdown based on list of recorder names provided

        params:
            mediasite_recorders: list of mediasite recorder names
        """

        for recorder in mediasite_recorders:
            self.combo_schedule_recorder.addItem(recorder["name"])

    def set_tree_folders(self, mediasite_folders, parent_id=""):
        """
        Adds folders to gui folder tree based on parent folder selection within window.
        Note: if no folder is currently selected this assumes the root is "Mediasite"

        params:
            mediasite_folders: list of mediasite folder names
            parent_id: parent element mediasite folder id to add elements to within the gui tree
        """        

        if parent_id == "":
            parent = QtWidgets.QTreeWidgetItem(self.tree_folder_location, ["Mediasite"])
        else:
            parent = self.tree_folder_location.currentItem()

        for folder in mediasite_folders:
            tree_item = QtWidgets.QTreeWidgetItem(parent, [folder["name"]])
            tree_item.setData(1, 0, folder["id"])
        parent.setExpanded(True)
        self.tree_folder_location.sortItems(0, 0)

    def set_progressbar_main_value(self, progress_value):
        """
        Change the main progress bar visibile progress

        params:
            progress_value: value associated with the progress bar. 
        """

        self.progressbar_main.setValue(progress_value)


    def error_dialog(self, modal_title, modal_description):
        """
        Create an error message dialog box using the provided title and description

        params:
            modal_title: title of the message box
            modal_description: description within the message box
        """

        #reset mouse cursor to default
        self.set_mouse_cursor_default()

        QtWidgets.QMessageBox.critical(self, modal_title, modal_description)

    def info_dialog(self, modal_title, modal_description):
        """
        Create an error message dialog box using the provided title and description

        params:
            modal_title: title of the message box
            modal_description: description within the message box
        """

        #reset mouse cursor to default
        self.set_mouse_cursor_default()
        
        QtWidgets.QMessageBox.information(self, modal_title, modal_description)

    def csv_file_dialog(self):
        """
        Create file selection window for user to select csv file from their local machine 

        returns:
            Local machine file path for selected CSV file
        """
        return QtWidgets.QFileDialog.getOpenFileName(self, "Select CSV file for batch import...", "", "CSV (*.csv)")

    def more_info_dialog(self, window_title="", window_text="", results="Successfully created schedule"):
        """
        Create batch import dialog containing results of imported schedule data

        returns:
            Dialog displaying results of batch import
        """

        batch_import_dialog = QtWidgets.QMessageBox(self)
        batch_import_dialog.setWindowTitle(window_title);
        batch_import_dialog.setIcon(QtWidgets.QMessageBox.Information)
        batch_import_dialog.setText(window_text);
        batch_import_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok);
        batch_import_dialog.setDetailedText(results)
        batch_import_dialog.buttons()[1].click()
        batch_import_dialog.exec();
