"""
Mediasite Scheduler

Application used for automating various scheduling tasks within Mediasite using a Mediasite
web API client.

pre-reqs: Python 3.x, PyQt5, pytz, requests, dateutil, and google-api-python-client libraries
Last modified: Feb 2018
By: Dave Bunten

License: MIT - see license.txt
"""

import os
import sys
import logging
import datetime
import tempfile
from PyQt5 import QtWidgets
import assets.app.app_view as app_view
import assets.app.app_controller as app_controller

if __name__ == "__main__":

    VERSION = "1.2.0"
    print("here")
    if getattr(sys,'frozen',False):
        run_path = sys._MEIPASS
    else:
        run_path = os.path.dirname(os.path.realpath(__file__))
    #gather our runpath for future use with various files
    #run_path = os.path.dirname(os.path.realpath(__file__))

    #log file datetime
    current_datetime_string = '{dt.month}-{dt.day}-{dt.year}_{dt.hour}-{dt.minute}-{dt.second}'.format(dt = datetime.datetime.now())
    
    if not os.path.exists(tempfile.gettempdir()+"/mediasite_scheduler/"):
        os.makedirs(tempfile.gettempdir()+"/mediasite_scheduler/")

    logfile_path = tempfile.gettempdir()+'/mediasite_scheduler/mediasite_scheduler_'+current_datetime_string+'.log'

    #logger for log file
    
    logging_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging_datefmt = '%m/%d/%Y - %I:%M:%S %p'

    logging.basicConfig(filename=logfile_path,
                        filemode='w',
                        format=logging_format,
                        datefmt=logging_datefmt,
                        level=logging.INFO
                        )

    #logger for console
    """
    console = logging.StreamHandler()
    formatter = logging.Formatter(logging_format,
                                    datefmt=logging_datefmt)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
    """

    logging.info("Began application session with user: "+ os.getlogin())
    logging.info("Application version: "+VERSION)

    #preparing to execute the QT application
    app = QtWidgets.QApplication(sys.argv)

    #creating the app view and controller to communicate with mediasite controller
    app_view_instance = app_view.app_view(run_path)
    app_controller_instance = app_controller.app_controller(app_view_instance, logfile_path)

    #executing the QT application
    sys.exit(app.exec_())
