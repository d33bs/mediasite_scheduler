# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\My Drive\Personal\Tools\mediasite_scheduler\assets\ui\mediasite_scheduler.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(761, 651)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 170, 251, 221))
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayoutWidget_5 = QtWidgets.QWidget(self.groupBox_2)
        self.formLayoutWidget_5.setGeometry(QtCore.QRect(10, 24, 240, 71))
        self.formLayoutWidget_5.setObjectName("formLayoutWidget_5")
        self.formLayout_6 = QtWidgets.QFormLayout(self.formLayoutWidget_5)
        self.formLayout_6.setContentsMargins(0, 0, 0, 0)
        self.formLayout_6.setObjectName("formLayout_6")
        self.check_catalog_include = QtWidgets.QCheckBox(self.formLayoutWidget_5)
        self.check_catalog_include.setChecked(True)
        self.check_catalog_include.setObjectName("check_catalog_include")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.check_catalog_include)
        self.check_catalog_allow_links = QtWidgets.QCheckBox(self.formLayoutWidget_5)
        self.check_catalog_allow_links.setChecked(True)
        self.check_catalog_allow_links.setObjectName("check_catalog_allow_links")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.check_catalog_allow_links)
        self.check_catalog_downloads = QtWidgets.QCheckBox(self.formLayoutWidget_5)
        self.check_catalog_downloads.setObjectName("check_catalog_downloads")
        self.formLayout_6.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.check_catalog_downloads)
        self.formLayoutWidget_6 = QtWidgets.QWidget(self.groupBox_2)
        self.formLayoutWidget_6.setGeometry(QtCore.QRect(10, 100, 231, 118))
        self.formLayoutWidget_6.setObjectName("formLayoutWidget_6")
        self.formLayout_7 = QtWidgets.QFormLayout(self.formLayoutWidget_6)
        self.formLayout_7.setContentsMargins(0, 0, 0, 0)
        self.formLayout_7.setObjectName("formLayout_7")
        self.label_catalog_title = QtWidgets.QLabel(self.formLayoutWidget_6)
        self.label_catalog_title.setObjectName("label_catalog_title")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_catalog_title)
        self.text_catalog_title = QtWidgets.QLineEdit(self.formLayoutWidget_6)
        self.text_catalog_title.setText("")
        self.text_catalog_title.setObjectName("text_catalog_title")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.text_catalog_title)
        self.label_catalog_desc = QtWidgets.QLabel(self.formLayoutWidget_6)
        self.label_catalog_desc.setObjectName("label_catalog_desc")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_catalog_desc)
        self.text_catalog_desc = QtWidgets.QPlainTextEdit(self.formLayoutWidget_6)
        self.text_catalog_desc.setObjectName("text_catalog_desc")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.text_catalog_desc)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(270, 380, 241, 181))
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayoutWidget_12 = QtWidgets.QWidget(self.groupBox_3)
        self.formLayoutWidget_12.setGeometry(QtCore.QRect(10, 18, 221, 151))
        self.formLayoutWidget_12.setObjectName("formLayoutWidget_12")
        self.formLayout_11 = QtWidgets.QFormLayout(self.formLayoutWidget_12)
        self.formLayout_11.setContentsMargins(0, 0, 0, 0)
        self.formLayout_11.setObjectName("formLayout_11")
        self.text_folder_location = QtWidgets.QLineEdit(self.formLayoutWidget_12)
        self.text_folder_location.setText("")
        self.text_folder_location.setObjectName("text_folder_location")
        self.formLayout_11.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.text_folder_location)
        self.label_folder_location = QtWidgets.QLabel(self.formLayoutWidget_12)
        self.label_folder_location.setObjectName("label_folder_location")
        self.formLayout_11.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_folder_location)
        self.tree_folder_location = QtWidgets.QTreeWidget(self.formLayoutWidget_12)
        self.tree_folder_location.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tree_folder_location.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tree_folder_location.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tree_folder_location.setHeaderHidden(True)
        self.tree_folder_location.setObjectName("tree_folder_location")
        self.tree_folder_location.header().setVisible(False)
        self.tree_folder_location.header().setStretchLastSection(True)
        self.formLayout_11.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.tree_folder_location)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(270, 10, 481, 361))
        self.groupBox_4.setObjectName("groupBox_4")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox_4)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 160, 321, 191))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_shedule_recurrence = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_shedule_recurrence.setObjectName("label_shedule_recurrence")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_shedule_recurrence)
        self.combo_schedule_recurrence = QtWidgets.QComboBox(self.formLayoutWidget)
        self.combo_schedule_recurrence.setObjectName("combo_schedule_recurrence")
        self.combo_schedule_recurrence.addItem("")
        self.combo_schedule_recurrence.addItem("")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.combo_schedule_recurrence)
        self.label_shedule_start_date = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_shedule_start_date.setObjectName("label_shedule_start_date")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_shedule_start_date)
        self.date_schedule_start_date = QtWidgets.QDateEdit(self.formLayoutWidget)
        self.date_schedule_start_date.setCalendarPopup(True)
        self.date_schedule_start_date.setObjectName("date_schedule_start_date")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.date_schedule_start_date)
        self.label_shedule_end_date = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_shedule_end_date.setObjectName("label_shedule_end_date")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_shedule_end_date)
        self.date_schedule_end_date = QtWidgets.QDateEdit(self.formLayoutWidget)
        self.date_schedule_end_date.setCalendarPopup(True)
        self.date_schedule_end_date.setObjectName("date_schedule_end_date")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.date_schedule_end_date)
        self.label_shedule_start_time = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_shedule_start_time.setObjectName("label_shedule_start_time")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_shedule_start_time)
        self.time_schedule_start_time = QtWidgets.QTimeEdit(self.formLayoutWidget)
        self.time_schedule_start_time.setObjectName("time_schedule_start_time")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.time_schedule_start_time)
        self.label_shedule_end_time = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_shedule_end_time.setObjectName("label_shedule_end_time")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_shedule_end_time)
        self.time_schedule_end_time = QtWidgets.QTimeEdit(self.formLayoutWidget)
        self.time_schedule_end_time.setObjectName("time_schedule_end_time")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.time_schedule_end_time)
        self.label_shedule_duration = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_shedule_duration.setObjectName("label_shedule_duration")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_shedule_duration)
        self.text_schedule_duration = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.text_schedule_duration.setObjectName("text_schedule_duration")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.text_schedule_duration)
        self.label_schedule_recurrence_freq = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_schedule_recurrence_freq.setObjectName("label_schedule_recurrence_freq")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_schedule_recurrence_freq)
        self.text_schedule_recurrence_freq = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.text_schedule_recurrence_freq.setObjectName("text_schedule_recurrence_freq")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.text_schedule_recurrence_freq)
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_4)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 461, 101))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_shedule_template = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_shedule_template.setObjectName("label_shedule_template")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_shedule_template)
        self.combo_schedule_template = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.combo_schedule_template.setObjectName("combo_schedule_template")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.combo_schedule_template)
        self.label_shedule_title = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_shedule_title.setObjectName("label_shedule_title")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_shedule_title)
        self.text_schedule_title = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.text_schedule_title.setObjectName("text_schedule_title")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.text_schedule_title)
        self.label_shedule_naming_scheme = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_shedule_naming_scheme.setObjectName("label_shedule_naming_scheme")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_shedule_naming_scheme)
        self.combo_schedule_naming_scheme = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.combo_schedule_naming_scheme.setObjectName("combo_schedule_naming_scheme")
        self.combo_schedule_naming_scheme.addItem("")
        self.combo_schedule_naming_scheme.addItem("")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.combo_schedule_naming_scheme)
        self.label_shedule_recorder = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_shedule_recorder.setObjectName("label_shedule_recorder")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_shedule_recorder)
        self.combo_schedule_recorder = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.combo_schedule_recorder.setObjectName("combo_schedule_recorder")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.combo_schedule_recorder)
        self.formLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_4)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(360, 160, 111, 191))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_4 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_4.setContentsMargins(0, 3, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_schedule_days_of_week = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_schedule_days_of_week.setObjectName("label_schedule_days_of_week")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_schedule_days_of_week)
        self.check_schedule_sunday = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.check_schedule_sunday.setEnabled(True)
        self.check_schedule_sunday.setObjectName("check_schedule_sunday")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.check_schedule_sunday)
        self.check_schedule_monday = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.check_schedule_monday.setObjectName("check_schedule_monday")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.check_schedule_monday)
        self.check_schedule_tuesday = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.check_schedule_tuesday.setObjectName("check_schedule_tuesday")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.check_schedule_tuesday)
        self.check_schedule_wednesday = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.check_schedule_wednesday.setObjectName("check_schedule_wednesday")
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.check_schedule_wednesday)
        self.check_schedule_thursday = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.check_schedule_thursday.setObjectName("check_schedule_thursday")
        self.formLayout_4.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.check_schedule_thursday)
        self.check_schedule_friday = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.check_schedule_friday.setObjectName("check_schedule_friday")
        self.formLayout_4.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.check_schedule_friday)
        self.check_schedule_saturday = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.check_schedule_saturday.setObjectName("check_schedule_saturday")
        self.formLayout_4.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.check_schedule_saturday)
        self.formLayoutWidget_11 = QtWidgets.QWidget(self.groupBox_4)
        self.formLayoutWidget_11.setGeometry(QtCore.QRect(10, 130, 461, 22))
        self.formLayoutWidget_11.setObjectName("formLayoutWidget_11")
        self.formLayout_13 = QtWidgets.QFormLayout(self.formLayoutWidget_11)
        self.formLayout_13.setContentsMargins(0, 0, 0, 0)
        self.formLayout_13.setHorizontalSpacing(0)
        self.formLayout_13.setObjectName("formLayout_13")
        self.check_schedule_auto_delete = QtWidgets.QCheckBox(self.formLayoutWidget_11)
        self.check_schedule_auto_delete.setChecked(True)
        self.check_schedule_auto_delete.setObjectName("check_schedule_auto_delete")
        self.formLayout_13.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.check_schedule_auto_delete)
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 10, 251, 161))
        self.groupBox_5.setObjectName("groupBox_5")
        self.formLayoutWidget_7 = QtWidgets.QWidget(self.groupBox_5)
        self.formLayoutWidget_7.setGeometry(QtCore.QRect(10, 20, 231, 131))
        self.formLayoutWidget_7.setObjectName("formLayoutWidget_7")
        self.formLayout_8 = QtWidgets.QFormLayout(self.formLayoutWidget_7)
        self.formLayout_8.setContentsMargins(0, 0, 0, 0)
        self.formLayout_8.setObjectName("formLayout_8")
        self.label_course_semester = QtWidgets.QLabel(self.formLayoutWidget_7)
        self.label_course_semester.setObjectName("label_course_semester")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_course_semester)
        self.text_course_semester = QtWidgets.QLineEdit(self.formLayoutWidget_7)
        self.text_course_semester.setObjectName("text_course_semester")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.text_course_semester)
        self.label_course_subject = QtWidgets.QLabel(self.formLayoutWidget_7)
        self.label_course_subject.setObjectName("label_course_subject")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_course_subject)
        self.text_course_subject = QtWidgets.QLineEdit(self.formLayoutWidget_7)
        self.text_course_subject.setObjectName("text_course_subject")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.text_course_subject)
        self.label_course_number = QtWidgets.QLabel(self.formLayoutWidget_7)
        self.label_course_number.setObjectName("label_course_number")
        self.formLayout_8.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_course_number)
        self.text_course_number = QtWidgets.QLineEdit(self.formLayoutWidget_7)
        self.text_course_number.setObjectName("text_course_number")
        self.formLayout_8.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.text_course_number)
        self.label_course_section = QtWidgets.QLabel(self.formLayoutWidget_7)
        self.label_course_section.setObjectName("label_course_section")
        self.formLayout_8.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_course_section)
        self.text_course_section = QtWidgets.QLineEdit(self.formLayoutWidget_7)
        self.text_course_section.setObjectName("text_course_section")
        self.formLayout_8.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.text_course_section)
        self.label_course_title = QtWidgets.QLabel(self.formLayoutWidget_7)
        self.label_course_title.setObjectName("label_course_title")
        self.formLayout_8.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_course_title)
        self.text_course_title = QtWidgets.QLineEdit(self.formLayoutWidget_7)
        self.text_course_title.setObjectName("text_course_title")
        self.formLayout_8.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.text_course_title)
        self.button_submit = QtWidgets.QPushButton(self.centralwidget)
        self.button_submit.setGeometry(QtCore.QRect(650, 570, 101, 31))
        self.button_submit.setObjectName("button_submit")
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setGeometry(QtCore.QRect(520, 380, 231, 181))
        self.groupBox_6.setObjectName("groupBox_6")
        self.formLayoutWidget_8 = QtWidgets.QWidget(self.groupBox_6)
        self.formLayoutWidget_8.setGeometry(QtCore.QRect(10, 20, 211, 151))
        self.formLayoutWidget_8.setObjectName("formLayoutWidget_8")
        self.formLayout_9 = QtWidgets.QFormLayout(self.formLayoutWidget_8)
        self.formLayout_9.setContentsMargins(0, 0, 0, 0)
        self.formLayout_9.setObjectName("formLayout_9")
        self.text_output = QtWidgets.QPlainTextEdit(self.formLayoutWidget_8)
        self.text_output.setObjectName("text_output")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.text_output)
        self.groupBox_7 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_7.setGeometry(QtCore.QRect(10, 400, 251, 161))
        self.groupBox_7.setObjectName("groupBox_7")
        self.formLayoutWidget_9 = QtWidgets.QWidget(self.groupBox_7)
        self.formLayoutWidget_9.setGeometry(QtCore.QRect(10, 47, 231, 51))
        self.formLayoutWidget_9.setObjectName("formLayoutWidget_9")
        self.formLayout_10 = QtWidgets.QFormLayout(self.formLayoutWidget_9)
        self.formLayout_10.setContentsMargins(0, 0, 0, 0)
        self.formLayout_10.setObjectName("formLayout_10")
        self.label_module_name = QtWidgets.QLabel(self.formLayoutWidget_9)
        self.label_module_name.setObjectName("label_module_name")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_module_name)
        self.text_module_name = QtWidgets.QLineEdit(self.formLayoutWidget_9)
        self.text_module_name.setText("")
        self.text_module_name.setObjectName("text_module_name")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.text_module_name)
        self.label_module_moduleid = QtWidgets.QLabel(self.formLayoutWidget_9)
        self.label_module_moduleid.setObjectName("label_module_moduleid")
        self.formLayout_10.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_module_moduleid)
        self.text_module_moduleid = QtWidgets.QLineEdit(self.formLayoutWidget_9)
        self.text_module_moduleid.setText("")
        self.text_module_moduleid.setObjectName("text_module_moduleid")
        self.formLayout_10.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.text_module_moduleid)
        self.formLayoutWidget_10 = QtWidgets.QWidget(self.groupBox_7)
        self.formLayoutWidget_10.setGeometry(QtCore.QRect(10, 20, 131, 22))
        self.formLayoutWidget_10.setObjectName("formLayoutWidget_10")
        self.formLayout_12 = QtWidgets.QFormLayout(self.formLayoutWidget_10)
        self.formLayout_12.setContentsMargins(0, 0, 0, 0)
        self.formLayout_12.setObjectName("formLayout_12")
        self.check_module_include = QtWidgets.QCheckBox(self.formLayoutWidget_10)
        self.check_module_include.setChecked(True)
        self.check_module_include.setObjectName("check_module_include")
        self.formLayout_12.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.check_module_include)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 761, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menu_help_about = QtWidgets.QAction(MainWindow)
        self.menu_help_about.setCheckable(False)
        self.menu_help_about.setObjectName("menu_help_about")
        self.menu_file_batch_import = QtWidgets.QAction(MainWindow)
        self.menu_file_batch_import.setObjectName("menu_file_batch_import")
        self.menu_file_reconnect = QtWidgets.QAction(MainWindow)
        self.menu_file_reconnect.setObjectName("menu_file_reconnect")
        self.menuFile.addAction(self.menu_file_batch_import)
        self.menuFile.addAction(self.menu_file_reconnect)
        self.menuHelp.addAction(self.menu_help_about)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Catalog"))
        self.check_catalog_include.setText(_translate("MainWindow", "Include Catalog"))
        self.check_catalog_allow_links.setText(_translate("MainWindow", "Allow Catalog Links"))
        self.check_catalog_downloads.setText(_translate("MainWindow", "Downloads Enabled"))
        self.label_catalog_title.setText(_translate("MainWindow", "Title"))
        self.label_catalog_desc.setText(_translate("MainWindow", "Description"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Folder"))
        self.label_folder_location.setText(_translate("MainWindow", "Name"))
        self.tree_folder_location.headerItem().setText(0, _translate("MainWindow", "Location"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Schedule"))
        self.label_shedule_recurrence.setText(_translate("MainWindow", "Recurrence"))
        self.combo_schedule_recurrence.setItemText(0, _translate("MainWindow", "Weekly"))
        self.combo_schedule_recurrence.setItemText(1, _translate("MainWindow", "One Time Only"))
        self.label_shedule_start_date.setText(_translate("MainWindow", "Start Date"))
        self.label_shedule_end_date.setText(_translate("MainWindow", "End Date"))
        self.label_shedule_start_time.setText(_translate("MainWindow", "Start Time"))
        self.label_shedule_end_time.setText(_translate("MainWindow", "End Time"))
        self.label_shedule_duration.setText(_translate("MainWindow", "Duration (min)"))
        self.text_schedule_duration.setText(_translate("MainWindow", "0"))
        self.label_schedule_recurrence_freq.setText(_translate("MainWindow", "Recurrence Freq."))
        self.text_schedule_recurrence_freq.setText(_translate("MainWindow", "1"))
        self.label_shedule_template.setText(_translate("MainWindow", "Template"))
        self.label_shedule_title.setText(_translate("MainWindow", "Title"))
        self.label_shedule_naming_scheme.setText(_translate("MainWindow", "Naming Scheme"))
        self.combo_schedule_naming_scheme.setItemText(0, _translate("MainWindow", "Record Date"))
        self.combo_schedule_naming_scheme.setItemText(1, _translate("MainWindow", "Incremental Number"))
        self.label_shedule_recorder.setText(_translate("MainWindow", "Recorder"))
        self.label_schedule_days_of_week.setText(_translate("MainWindow", "Days of the Week"))
        self.check_schedule_sunday.setText(_translate("MainWindow", "Sunday"))
        self.check_schedule_monday.setText(_translate("MainWindow", "Monday"))
        self.check_schedule_tuesday.setText(_translate("MainWindow", "Tuesday"))
        self.check_schedule_wednesday.setText(_translate("MainWindow", "Wednesday"))
        self.check_schedule_thursday.setText(_translate("MainWindow", "Thursday"))
        self.check_schedule_friday.setText(_translate("MainWindow", "Frdiay"))
        self.check_schedule_saturday.setText(_translate("MainWindow", "Saturday"))
        self.check_schedule_auto_delete.setText(_translate("MainWindow", "Automatically delete schedule once occurrences have ended"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Course Information"))
        self.label_course_semester.setText(_translate("MainWindow", "Semester"))
        self.label_course_subject.setText(_translate("MainWindow", "Subject"))
        self.label_course_number.setText(_translate("MainWindow", "Number"))
        self.label_course_section.setText(_translate("MainWindow", "Section"))
        self.label_course_title.setText(_translate("MainWindow", "Title"))
        self.button_submit.setText(_translate("MainWindow", "Submit"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Result"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Module"))
        self.label_module_name.setText(_translate("MainWindow", "Name"))
        self.label_module_moduleid.setText(_translate("MainWindow", "ModuleId"))
        self.check_module_include.setText(_translate("MainWindow", "Include Module"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menu_help_about.setText(_translate("MainWindow", "About"))
        self.menu_file_batch_import.setText(_translate("MainWindow", "Batch import..."))
        self.menu_file_reconnect.setText(_translate("MainWindow", "Reconnect..."))

