"""
Mediasite controller for medaisite scheduler. Performs various Mediasite API
work using mediasite_web_api client.

Last modified: Feb 2018
By: Dave Bunten

License: MIT - see license.txt
"""
import os
import sys
import logging
import time
import datetime
import pytz
import tzlocal
import json
import datetime
from dateutil import rrule
from urllib.parse import quote
import assets.mediasite.mediasite_web_api as mediasite_web_api

class mediasite_controller():
    def __init__(self, mediasite_model, run_path):
        """
        params:
            mediasite_model: complementary model for storing various mediasite data related to this controller
            run_path: root path where the application is being run from on the system
        """
        self.run_path = run_path
        self.mediasite_api_client = self.create_mediasite_api_client(self.run_path+"/config/config.json")
        self.mediasite_model = mediasite_model
        self.mediasite_gather_root_folder_id()
        self.mediasite_gather_templates()
        self.mediasite_gather_recorders()
        self.mediasite_gather_folders()

    def create_mediasite_api_client(self, config_file_path):
        """
        Loads configuration file data and creates new Mediasite api client using mediasite_web_api.py

        params:
            config_file_path: file path containing configuration data for connecting to Mediasite instance

        returns:
            Configured Mediasite web api client object
        """
        #load configuration data from JSON file
        #run_path+"/config/test_config.json"

        config_file = open(config_file_path)
        config_data = json.load(config_file)

        return mediasite_web_api.client(config_data["mediasite_base_url"],
                                        config_data["mediasite_api_secret"],
                                        config_data["mediasite_api_user"],
                                        config_data["mediasite_api_pass"]
                                        )

    def mediasite_connection_validated(self):
        """
        Validates Mediasite connection through web api through request for "home" information from Mediasite

        returns:
            True if connection is confirmed to work, false if not
        """

        #request mediasite home information - contains various site-level details
        result = self.mediasite_api_client.do_request("get", "Home", "","")

        if self.experienced_request_errors(result):
            logging.error("Experienced errors while attempting to validate Mediasite connection")
            self.mediasite_model.set_current_connection_valid(False)
            return False
        else:
            self.mediasite_model.set_current_connection_valid(True)
            return True

    def mediasite_gather_templates(self):
        """
        Gathers mediasite template name listing from mediasite system

        returns:
            list of mediasite template names from mediasite system
        """

        mediasite_templates = []

        logging.info("Gathering Mediasite templates")

        #request mediasite template information from mediasite
        result = self.mediasite_api_client.do_request("get", "Templates", "$top=100", "")
        
        if self.experienced_request_errors(result):
            return result
        else:
            #for each template in the result of the request append the name to the list
            for template in result.json()["value"]:
                mediasite_templates.append(template)
            
            #add the listing of template names to the model for later use
            self.mediasite_model.set_templates(mediasite_templates)
            return mediasite_templates

    def mediasite_gather_recorders(self):
        """
        Gathers mediasite recorder name listing from mediasite system

        returns:
            list of mediasite recorder names from mediasite system
        """

        mediasite_recorders = []

        logging.info("Gathering Mediasite recorders")

        #request mediasite recorder information from mediasite
        result = self.mediasite_api_client.do_request("get", "Recorders", "$top=100", "")
        
        if self.experienced_request_errors(result):
            return result
        else:       
            #for each recorder in the result of the request append the name to the list
            for recorder in result.json()["value"]:
                mediasite_recorders.append({"name":recorder["Name"],"id":recorder["Id"]})

            #add the listing of recorder names to the model for later use
            self.mediasite_model.set_recorders(mediasite_recorders)

            return mediasite_recorders



    def mediasite_gather_folders(self, parent_id=""):
        """
        Gathers mediasite child folder name, ID, and parent ID listing from mediasite system
        based on provided parent mediasite folder ID

        params:
            parent_id: mediasite parent folder ID for use as a reference point in this function

        returns:
            list of dictionary items containing child mediasite folder names, ID's, and parent folder ID's
        """

        if parent_id == "":
            parent_id = self.mediasite_model.get_root_parent_folder_id()

        mediasite_folders = []

        logging.info("Gathering Mediasite folders")

        #request existing (non-recycled) mediasite folder information based on parent folder ID provided to function
        result = self.mediasite_api_client.do_request("get", "Folders", "$top=100&$filter=ParentFolderId eq '"+parent_id+"' and Recycled eq false","")

        if self.experienced_request_errors(result):
            return result
        else:
            #for each item in the result create a dictionary with name, ID, and parent ID elements for reference
            for folder in result.json()["value"]:
                mediasite_folders.append({"name":folder["Name"],
                                            "id":folder["Id"],
                                            "parent_id":folder["ParentFolderId"]
                                            })

            #add the listing of folder data to the model for later use
            self.mediasite_model.set_folders(mediasite_folders, parent_id)

            return mediasite_folders

    def mediasite_gather_root_folder_id(self):
        """
        Gathers mediasite root folder ID for use with other functions.

        Note: finding the root folder ID is somewhat of a workaround as normal requests for the "Mediasite" root folder
        do not appear to yield any data. The "Mediasite Users" folder appears as a standard folder on most installations
        and therefore serves as a reference point to determine the root folder. This may need to change in the future based
        on configuration changes etc.

        returns:
            the parent ID of the mediasite "Mediasite Users" folder
        """

        logging.info("Gathering Mediasite root folder id")

        #request mediasite folder information on the "Mediasite Users" folder
        result = self.mediasite_api_client.do_request("get", "Folders", "$filter=Name eq 'Mediasite Users' and Recycled eq false","")

        if self.experienced_request_errors(result):
            return result
        else:
            #return the parent ID of the mediasite "Mediasite Users" folder
            self.mediasite_model.set_root_parent_folder_id(result.json()["value"][0]["ParentFolderId"])
            return result.json()["value"][0]["ParentFolderId"]

    def experienced_request_errors(self, request_result):
        """
        Checks for errors experienced from mediasite_web_api Python requests.

        params:
            request_result: returned content from mediasite_web_api request peformed

        returns:
            true if errors were experienced, false if no errors experienced
        """

        if type(request_result) is str:
            logging.error(request_result)
            self.mediasite_model.set_current_connection_valid(False)
            return True
        else:
            return False

    def mediasite_create_folder(self, folder_name, parent_id):
        """
        Creates mediasite folder based on provided name and parent folder ID

        params:
            folder_name: name desired for the new mediasite folder
            parent_id: mediasite parent folder ID for use as a reference point in this function

        returns:
            resulting response from the mediasite web api request for folder data
        """

        folder_search_result = self.mediasite_find_folder_by_name_and_parent_id(folder_name, parent_id)

        if int(folder_search_result["odata.count"]) > 0:
            logging.info("Found existing folder '"+folder_name+"' under parent "+parent_id)
            return folder_search_result["value"][0]

        logging.info("Creating folder '"+folder_name+"' under parent "+parent_id)

        #prepare post data for use in creating the folder
        post_data = {"Name":folder_name,
                    "Description":"",
                    "ParentFolderId":parent_id
                    }

        #make the mediasite request using the post data found above to create the folder
        result = self.mediasite_api_client.do_request("post", "Folders", "", post_data).json()

        if self.experienced_request_errors(result):
            return result
        else:
            #if there is an error, log it
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])

            return result

    def mediasite_find_folder_by_name_and_parent_id(self, folder_name, parent_id):
        """
        Finds mediasite folder based on provided name and parent folder ID

        params:
            folder_name: name desired for the new mediasite folder
            parent_id: mediasite parent folder ID for use as a reference point in this function

        returns:
            resulting response from the mediasite web api request to find the folder
        """

        logging.info("Searching for folder '"+folder_name+"' under parent "+parent_id)

        #make the mediasite request using the post data found above to create the folder
        result = self.mediasite_api_client.do_request("get", "Folders", "$filter=Name eq '"+folder_name+"' and ParentFolderId eq '"+parent_id+"'and Recycled eq false", "").json()
        
        if self.experienced_request_errors(result):
            return result
        else:
            #if there is an error, log it
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])

            return result

    def mediasite_find_folder_by_name(self, folder_name):
        """
        Gathers mediasite root folder ID for use with other functions.

        Note: finding the root folder ID is somewhat of a workaround as normal requests for the "Mediasite" root folder
        do not appear to yield any data. The "Mediasite Users" folder appears as a standard folder on most installations
        and therefore serves as a reference point to determine the root folder. This may need to change in the future based
        on configuration changes etc.

        returns:
            the parent ID of the mediasite "Mediasite Users" folder
        """

        logging.info("Finding Mediasite folder information with name of: "+folder_name)

        #request mediasite folder information on the "Mediasite Users" folder
        result = self.mediasite_api_client.do_request("get", "Folders", "$filter=Name eq '"+folder_name+"' and Recycled eq false","")
        
        if self.experienced_request_errors(result):
            return result
        else:
            #return the parent ID of the mediasite "Mediasite Users" folder
            return ""

    def mediasite_find_template_by_name(self, template_name):
        """
        Gathers mediasite root folder ID for use with other functions.

        Note: finding the root folder ID is somewhat of a workaround as normal requests for the "Mediasite" root folder
        do not appear to yield any data. The "Mediasite Users" folder appears as a standard folder on most installations
        and therefore serves as a reference point to determine the root folder. This may need to change in the future based
        on configuration changes etc.

        returns:
            the parent ID of the mediasite "Mediasite Users" folder
        """

        logging.info("Finding Mediasite template information with name of: "+template_name)

        #request mediasite folder information on the "Mediasite Users" folder
        result = self.mediasite_api_client.do_request("get", "Templates", "$filter=Name eq '"+quote(template_name)+"'","")
        
        if self.experienced_request_errors(result):
            return result
        else:
            #if there is an error, log it
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])

            return result

    def mediasite_enable_catalog_downloads(self, catalog_id):
        """
        Enables mediasite catalog downloads using provided catalog ID

        Note: seems to only return a 204 http code on success

        params:
            catalog_id: mediasite catalog ID to enable downloads on

        returns:
            resulting response from the mediasite web api request to enable downloads on the folder
        """

        logging.info("Enabling catalog downloads for catalog: '"+catalog_id)

        #prepare patch data to be sent to mediasite
        patch_data = {"AllowPresentationDownload":"True"}

        #make the mediasite request using the catalog id and the patch data found above to enable downloads
        result = self.mediasite_api_client.do_request("patch", "Catalogs('"+catalog_id+"')/Settings", "", patch_data)
        
        if self.experienced_request_errors(result):
            return result
        else:
            return result

    def mediasite_add_module_to_catalog(self, catalog_id, module_guid):
        """
        Add mediasite module to catalog by catalog id and module guid

        params:
            catalog_id: mediasite catalog id which will have the module added
            module_guid: mediasite module GUID (not to be confused with a module ID)

        returns:
            resulting response from the mediasite web api request
        """

        logging.info("Associating catalog: "+catalog_id+" to module: "+module_guid)

        #prepare patch data to be sent to mediasite
        post_data = {"MediasiteId":catalog_id}

        #make the mediasite request using the catalog id and the patch data found above to enable downloads
        result = self.mediasite_api_client.do_request("post", "Modules('"+module_guid+"')/AddAssociation", "", post_data)

        if self.experienced_request_errors(result):
            return result
        else:
            return result

    def mediasite_enable_catalog_public(self, folder_id):
        """
        NON-FUNCTIONING AT THIS TIME
        Modify an existing catalog to enable public access
        
        Note: modifies the folder as opposed to the catalog as it provides authorization to the

        params:
            folder_id: mediasite folder ID associated with the catalog 
        """
        """
        returns:
            resulting response from the mediasite web api request to enable downloads on the folder

        logging.info("Enabling public access for folder "+folder_id)
    
        post_data = {"InheritFromParent":"False",
                    "Permissions":permissions,
                    "LinkedFolderId":parent_id
                    }

        result = self.mediasite_api_client.do_request("post", "Folders('"+folder_id+"')/UpdatePermissions", "", post_data).json()
        
        if "odata.error" in result:
            logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])
        """
        return

    def mediasite_create_module(self, module_name, module_id):
        """
        Creates mediasite module using provided module name and module id

        params:
            module_name: name which will appear for the module
            module_id: moduleid associated with module in mediasite

        returns:
            resulting response from the mediasite web api request
        """

        logging.info("Creating module '"+module_name+"' with module id "+module_id)
    
        post_data = {"Name":module_name,
                    "ModuleId":module_id
                    }

        result = self.mediasite_api_client.do_request("post", "Modules", "", post_data).json()

        if self.experienced_request_errors(result):
            return result
        else:
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])

            return result

    def mediasite_create_catalog(self, catalog_name, description, parent_id):
        """
        Creates mediasite catalog using provided catalog name, description, and parent folder id

        params:
            catalog_name: name which will appear for the catalog
            description: description which will appear for the catalog (beneath name)
            folder_id: mediasite folder ID associated with the catalog

        returns:
            resulting response from the mediasite web api request
        """

        logging.info("Creating catalog '"+catalog_name+"' under parent folder "+parent_id)
    
        post_data = {"Name":catalog_name,
                    "Description":description,
                    "LinkedFolderId":parent_id
                    }

        result = self.mediasite_api_client.do_request("post", "Catalogs", "", post_data).json()
        
        if self.experienced_request_errors(result):
            return result
        else:        
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])

            return result

    def mediasite_create_schedule(self, schedule_data):
        """
        Creates mediasite schedule using provided schedule data

        params:
            schedule_data: dictionary containing various necessary data for creating mediasite scheduling

        Expects schedule_data to contain the following keys:
        schedule_data = {
            "mediasite_folder_root_id":string,
            "mediasite_folders":string,
            "catalog_include":boolean,
            "catalog_name":string,
            "catalog_description":string,
            "catalog_enable_download":boolean,
            "module_include":boolean,
            "module_name":string,
            "module_id":string,
            "schedule_parent_folder_id":string,
            "schedule_template":string,
            "schedule_name":string,
            "schedule_naming_scheme":string,
            "schedule_recorder":string,
            "schedule_recurrence":string,
            "schedule_auto_delete":string,
            "schedule_start_datetime_utc_string":string,
            "schedule_end_datetime_utc_string":string,
            "schedule_start_datetime_utc":datetime,
            "schedule_end_datetime_utc":datetime,
            "schedule_start_datetime_local_string":string,
            "schedule_end_datetime_local_string":string,
            "schedule_start_datetime_local":datetime,
            "schedule_end_datetime_local":datetime,
            "schedule_duration":string,
            "schedule_recurrence_freq":string,
            "schedule_days_of_week":{
                "Sunday":boolean,
                "Monday":boolean,
                "Tuesday":boolean,
                "Wednesday":boolean,
                "Thursday":boolean,
                "Friday":boolean,
                "Saturday":boolean
                }
            }

        returns:
            resulting response from the mediasite web api request
        """

        logging.info("Creating schedule '"+schedule_data["schedule_name"])
    
        schedule_naming_scheme = self.mediasite_model.translate_schedule_recurrence_naming(schedule_data["schedule_naming_scheme"])
        schedule_template_id = self.mediasite_model.translate_template_id(schedule_data["schedule_template"])
        schedule_recorder_id = self.mediasite_model.translate_recorder_id(schedule_data["schedule_recorder"])

        post_data = {"Name":schedule_data["schedule_name"],
                    "FolderId":schedule_data["schedule_parent_folder_id"],
                    "TitleType":schedule_naming_scheme,
                    "ScheduleTemplateId":schedule_template_id,
                    "IsUploadAutomatic":"True",
                    "RecorderId":schedule_recorder_id,
                    "RecorderName":schedule_data["schedule_recorder"],
                    "CreatePresentation":"True",
                    "LoadPresentation":"True",
                    "AutoStart":"True",
                    "AutoStop":"True",
                    "NotifyPresenter":"False",
                    "DeleteInactive":schedule_data["schedule_auto_delete"]
                    }

        result = self.mediasite_api_client.do_request("post", "Schedules", "", post_data).json()
        
        if self.experienced_request_errors(result):
            return result
        else:
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])
            else:
                self.mediasite_model.add_schedule(result)

            return result

    def mediasite_translate_schedule_days_of_week(self, schedule_data):
        """
        Translates days of the week to schedule into Mediasite-friendly format as per API documentation

        params:
            schedule_data: dictionary containing various necessary data for creating mediasite scheduling

        returns:
            string which is ready to be sent to Mediasite for schedule recurrences
        """
        result_string = ""
        count = 0

        #for each day of week element, see if value is true, and if so append to a string containing all other days in order
        for key,val in schedule_data["schedule_days_of_week"].items():
            if val == True:
                if count > 0:
                    result_string += "|"

                result_string += key
                count += 1

        return result_string

    def mediasite_to_dateutil_weekdays(self, recurrence_days_of_week):
        """
        Translates days of week from Mediasite-friendly convention to Dateutil-friendly format

        params:
            recurrence_days_of_week: Mediasite-friendly days of the week string

        returns:
            string which is ready to be sent to Dateutil for schedule dates recurrences
        """

        result_list = []

        if "Sunday" in recurrence_days_of_week:
            result_list.append(rrule.SU)
        if "Monday" in recurrence_days_of_week:
            result_list.append(rrule.MO)
        if "Tuesday" in recurrence_days_of_week:
            result_list.append(rrule.TU)
        if "Wednesday" in recurrence_days_of_week:
            result_list.append(rrule.WE)
        if "Thursday" in recurrence_days_of_week:
            result_list.append(rrule.TH)
        if "Friday" in recurrence_days_of_week:
            result_list.append(rrule.FR)            
        if "Saturday" in recurrence_days_of_week:
            result_list.append(rrule.SA)

        return result_list

    def convert_datetime_local_to_utc(self, datetime_local):
        """
        Translate local datetime to utc for use by internal Mediasite system

        params:
            datetime_local: local datetime object

        returns:
            converted utc datetime object
        """

        #find UTC times for datetimes due to Mediasite requirements
        UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()

        return datetime_local + UTC_OFFSET_TIMEDELTA

    def recurrence_datelist_generator(self, schedule_data):
        """
        Create a list of dates based on schedule data gathered for Mediasite recording scheduling

        params:
            schedule_data: dictionary containing various necessary data for creating mediasite scheduling

        returns:
            list of recurrence datetimes based on the schedule data
        """
        days_of_week = self.mediasite_translate_schedule_days_of_week(schedule_data)

        #check that we have days of the week specified - dateutil returns all dates if none are specified (unwanted in this case)
        if days_of_week == "":
            return []

        rule = rrule.rrule(dtstart = schedule_data["schedule_start_datetime_local"], 
                            freq = rrule.DAILY,
                            byweekday = self.mediasite_to_dateutil_weekdays(days_of_week)
                            )

        datelist = rule.between(schedule_data["schedule_start_datetime_local"],
                                schedule_data["schedule_end_datetime_local"],
                                inc = True
                                )

        return datelist

    def mediasite_module_moduleid_already_exists(self, module_id):
        """
        Determine whether the provided moduleid already exists

        returns:
            true if it already exists, false if it does not
        """
        result = self.mediasite_api_client.do_request("get", "Modules", "$filter=ModuleId eq '"+module_id+"'", "").json()

        if self.experienced_request_errors(result):
            return result
        else:
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])

            if int(result["odata.count"]) > 0:
                logging.error("Found more than one occurrence of ModuleId "+module_id)
                return True
            else:
                logging.info("Verified moduleId "+module_id+" does not already exist.")
                return False

    def schedule_data_has_0_occurrences(self, schedule_data):
        """
        Determine whether the current schedule data contains 0 occurrences to avoid errors

        returns:
            true if there are 0 occurrences in the schedule data, false if there are more than 0 occurrences
        """
        datelist = self.recurrence_datelist_generator(schedule_data)

        if len(datelist) <= 0:
            logging.error("Submitted schedule data does not contain at least one occurrence.")
            return True
        else:
            return False

    def mediasite_create_recurrence(self, schedule_data, schedule_result):
        """
        Creates Mediasite schedule recurrence. Specifically, this is the datetimes which a recording schedule
        will produce presentations with.

        params:
            schedule_data: dictionary containing various necessary data for creating mediasite scheduling
            schedule_result: data provided from Mediasite after a schedule is produced

        returns:
            resulting response from the mediasite web api request
        """
        logging.info("Creating schedule recurrence(s) for '"+schedule_data["schedule_name"])

        #convert duration minutes to milliseconds as required by Mediasite system
        recurrence_duration = int(schedule_data["schedule_duration"])*60*1000

        #translate various values gathered from the UI to Mediasite-friendly conventions
        recurrence_type = self.mediasite_model.translate_schedule_recurrence_pattern(schedule_data["schedule_recurrence"])

        #creates a recurrence using post_data created below
        def request_create_recurrence(post_data):
            result = self.mediasite_api_client.do_request("post", "Schedules('"+schedule_result["Id"]+"')/Recurrences", "", post_data).json()

            if self.experienced_request_errors(result):
                return result
            else:
                if "odata.error" in result:
                    logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])
                else:
                    self.mediasite_model.add_recurrence(result)

        result = ""

        #for one-time recurrence creation
        if recurrence_type == "None":
            post_data = {"MediasiteId":schedule_result["Id"],
                "RecordDuration":recurrence_duration,
                "StartRecordDateTime":schedule_data["schedule_start_datetime_utc_string"],
                "EndRecordDateTime":schedule_data["schedule_end_datetime_utc_string"],
                "RecurrencePattern":recurrence_type,
                "RecurrenceFrequency":schedule_data["schedule_recurrence_freq"],
                "DaysOfTheWeek":self.mediasite_translate_schedule_days_of_week(schedule_data)
                }

            result = request_create_recurrence(post_data)

        elif recurrence_type == "Weekly":
            #for weekly recurrence creation
            """
            NOTE: due to bugs in Mediasite system we defer to using one-time schedules for each day of the week
            specified within the provided time frame. This produces more accurate and stable results as of the time
            of writing this in Feb 2018.
            """

            #determine date range for use in creating single instances which are less error-prone
            datelist = self.recurrence_datelist_generator(schedule_data)

            #for each date in the list produced above, we create post data and request a one-time schedule recurrence
            for date in datelist:

                mediasite_friendly_datetime_start_utc = self.convert_datetime_local_to_utc(date)
                mediasite_friendly_datetime_start = mediasite_friendly_datetime_start_utc.strftime("%Y-%m-%dT%H:%M:%S")

                #find our current timezone
                local_tz = tzlocal.get_localzone()

                #check if current datetime is dst or not
                now = datetime.datetime.now()
                #is_now_dst = now.astimezone(local_tz).dst() != datetime.timedelta(0)
                is_now_dst = local_tz.localize(now).dst() != datetime.timedelta(0)

                #check if future datetime is dst or not
                #is_later_dst = date.astimezone(local_tz).dst() != datetime.timedelta(0)
                is_later_dst = local_tz.localize(date).dst() != datetime.timedelta(0)

                #compare between the current and future datetimes to find differences and adjust
                if is_now_dst != is_later_dst:

                    #convert future datetime to be an hour more or less bast on dst comparison above
                    if is_now_dst and not is_later_dst:
                        mediasite_friendly_datetime_start = (mediasite_friendly_datetime_start_utc + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
                    
                    elif not is_now_dst and is_later_dst:
                        mediasite_friendly_datetime_start = (mediasite_friendly_datetime_start_utc - datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")

                post_data = {"MediasiteId":schedule_result["Id"],
                            "RecordDuration":recurrence_duration,
                            "StartRecordDateTime":mediasite_friendly_datetime_start,
                            "RecurrencePattern":"None",
                            }
                
                request_create_recurrence(post_data)

            return result

        return result

    def mediasite_gather_recurrences(self, schedule_id):
        """
        Gathers recurrences for specified Mediasite schedule by ID

        params:
            schedule_id: Mediasite schedule ID which you would like to find recurrences for.

        returns:
            resulting response from the mediasite web api request
        """
        result = self.mediasite_api_client.do_request("get", "Schedules('"+schedule_id+"')/Recurrences", "", "").json()
        
        if self.experienced_request_errors(result):
            return result
        else:
            if "odata.error" in result:
                logging.error(result["odata.error"]["code"]+": "+result["odata.error"]["message"]["value"])

            return result

    def process_batch_scheduling_data(self, batch_scheduling_data):
        """
        Process batch scheduling data provided in pre-specified format.

        params:
            batch_scheduling_data: list of dictionaries which contain pertinent mediasite scheduling data

        returns:
            output indicating which rows of scheduling information were successfully scheduled
        """

        result_list = []

        #parse each row of scheduling data
        for row in batch_scheduling_data:

            #gather and organize schedule data
            schedule_data = self.gather_mediasite_import_schedule_data(row)

            #perform mediasite-specific work using schedule_data for row
            row_result = self.process_scheduling_data_row(schedule_data)

            #append results to the overall list
            result_list.append(row_result)

        return result_list

    def process_scheduling_data_row(self, schedule_data):
            """
            Process scheduling data provided in pre-specified format.

            params:
                schedule_data: list which contain pertinent mediasite scheduling data

            returns:
                output indicating which rows of scheduling information were successfully scheduled
            """

            row_result = {}

            validation_result = self.validate_scheduling_data(schedule_data)

            #validate the scheduling data
            if "error" in validation_result.keys():
                row_result["error"] = validation_result["error"]
                return row_result

            #parse and create folders
            parent_folder_id = self.parse_and_create_mediasite_folders(schedule_data["mediasite_folders"], schedule_data["mediasite_folder_root_id"])
            
            #set the current schedule data parent folder id
            schedule_data["schedule_parent_folder_id"] = parent_folder_id

            #parse and create module
            if schedule_data["module_include"]:
                module_result = self.mediasite_create_module(schedule_data["module_name"], schedule_data["module_id"])
                row_result["module_result"] = module_result

            #parse and create catalog
            if schedule_data["catalog_include"]:
                catalog_result = self.mediasite_create_catalog(schedule_data["catalog_name"], schedule_data["catalog_description"], schedule_data["schedule_parent_folder_id"])
                row_result["catalog_result"] = catalog_result

            #enable catalog downloads
            if schedule_data["catalog_enable_download"]:
                self.mediasite_enable_catalog_downloads(catalog_result["Id"])

            #link module to catalog
            if schedule_data["module_include"] and schedule_data["catalog_include"]:
                self.mediasite_add_module_to_catalog(catalog_result["Id"], module_result["Id"])

            schedule_result = self.mediasite_create_schedule(schedule_data)
            row_result["schedule_result"] = schedule_result

            if "odata.error" not in schedule_result:
                recurrence_result = self.mediasite_create_recurrence(schedule_data, schedule_result)
                row_result["recurrence_result"] = recurrence_result

            return row_result

    def validate_scheduling_data(self, schedule_data):
        """
        Validate user entered data and notify them of any corrections using error dialogs

        returns:
            true if no errors were encountered, false if any errors were encountered
        """

        if self.schedule_data_has_0_occurrences(schedule_data):
            result = {"error":"Error: " + schedule_data["schedule_name"] + " - Submitted schedule data does not contain at least one occurrence."}
            logging.error(result["error"])
            return result

        if schedule_data["module_include"] and self.mediasite_module_moduleid_already_exists(schedule_data["module_id"]):
            result = {"error":"Error: " + schedule_data["schedule_name"] + " - Submitted ModuleId already exists."}
            logging.error(result["error"])
            return result

        if schedule_data["schedule_template"] in self.mediasite_model.get_templates():
            result = {"error":"Error: " + schedule_data["schedule_name"] + " - Submitted template name does not exist."}
            logging.error(result["error"])
            return result

        return {"Success":""}

    def fix_12_hour_time_padding(self, time_string):
        """
        Ensure 12 hour times have additional 0 in front of single digit numbers for later conversions

        params:
            time_string: 12 hour time string, for example "1:00 PM"

        returns:
            true if no errors were encountered, false if any errors were encountered
        """
        if len(time_string) == 7:
            time_string = "0" + time_string

        return time_string

    def gather_mediasite_import_schedule_data(self, scheduling_data):
        """
        Parse, convert, and request mediasite schedule creation

        Note - default date time formats:
            Mediasite: 9999-12-31T23:59:59

        scheduling_data keys:
        -------------------
        Presentation Title
        Recorder
        Template
        Naming Scheme
        Delete Schedule After Occurrences
        Include Catalog
        Enable Catalog Download
        Catalog Name
        Catalog Description
        Include Module
        Module Name
        Module ID
        Mediasite Folder
        Recurrence
        Start Date
        End Date
        Start Time
        End Time
        Recurrence Frequency
        Sun
        Mon
        Tue
        Wed
        Thu
        Fri
        Sat

        params:
            parent_folder_id: mediasite folder id which the schedule will be associated with
        returns:
            mediasite api output for schedule creation
        """

        #scheduling_data["Start Time"] = self.fix_12_hour_time_padding(scheduling_data["Start Time"])
        #scheduling_data["End Time"] = self.fix_12_hour_time_padding(scheduling_data["End Time"])

        local_start_datetime_string_intake = scheduling_data["Start Date"] + "T" + scheduling_data["Start Time"]
        local_end_datetime_string_intake = scheduling_data["End Date"] + "T" + scheduling_data["End Time"]

        #find duration in minutes from provided data
        local_start_time = datetime.datetime.strptime(scheduling_data["Start Time"], "%I:%M %p")
        local_end_time = datetime.datetime.strptime(scheduling_data["End Time"], "%I:%M %p")
        duration_in_minutes = int((local_end_time - local_start_time).seconds/60)

        #find UTC times for datetimes due to Mediasite requirements
        local_start_datetime = datetime.datetime.strptime(local_start_datetime_string_intake, "%m/%d/%yT%I:%M %p").replace(second=10)
        local_end_datetime = datetime.datetime.strptime(local_end_datetime_string_intake, "%m/%d/%yT%I:%M %p").replace(second=10)
        utc_start_datetime = self.convert_datetime_local_to_utc(local_start_datetime).replace(second=10)
        utc_end_datetime = self.convert_datetime_local_to_utc(local_end_datetime).replace(second=10)
        utc_start_datetime_string = utc_start_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        utc_end_datetime_string = utc_end_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        local_start_datetime_string = local_start_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        local_end_datetime_string = local_end_datetime.strftime("%Y-%m-%dT%H:%M:%S")

        schedule_data_submit = {
            "mediasite_folder_root_id":"",
            "mediasite_folders":scheduling_data["Mediasite Folder"],
            "catalog_include":True if scheduling_data["Include Catalog"] == "TRUE" else False,
            "catalog_name":scheduling_data["Catalog Name"],
            "catalog_description":scheduling_data["Catalog Description"],
            "catalog_enable_download":True if scheduling_data["Enable Catalog Download"] == "TRUE" else False,
            "module_include":True if scheduling_data["Include Module"] == "TRUE" else False,
            "module_name":scheduling_data["Module Name"],
            "module_id":scheduling_data["Module ID"],
            "schedule_parent_folder_id":"",
            "schedule_template":scheduling_data["Template"],
            "schedule_name":scheduling_data["Presentation Title"],
            "schedule_naming_scheme":scheduling_data["Naming Scheme"],
            "schedule_recorder":scheduling_data["Recorder"],
            "schedule_recurrence":scheduling_data["Recurrence"],
            "schedule_auto_delete":"True" if scheduling_data["Delete Schedule After Occurrences"] == "TRUE" else "False",
            "schedule_start_datetime_utc_string":utc_start_datetime_string,
            "schedule_end_datetime_utc_string":utc_end_datetime_string,
            "schedule_start_datetime_utc":utc_start_datetime,
            "schedule_end_datetime_utc":utc_end_datetime,
            "schedule_start_datetime_local_string":local_start_datetime_string,
            "schedule_end_datetime_local_string":local_end_datetime_string,
            "schedule_start_datetime_local":local_start_datetime,
            "schedule_end_datetime_local":local_end_datetime,
            "schedule_duration":str(duration_in_minutes),
            "schedule_recurrence_freq":scheduling_data["Recurrence Frequency"],
            "schedule_days_of_week":{
                                    "Sunday":True if scheduling_data["Sun"] == "TRUE" else False,
                                    "Monday":True if scheduling_data["Mon"] == "TRUE" else False,
                                    "Tuesday":True if scheduling_data["Tue"] == "TRUE" else False,
                                    "Wednesday":True if scheduling_data["Wed"] == "TRUE" else False,
                                    "Thursday":True if scheduling_data["Thu"] == "TRUE" else False,
                                    "Friday":True if scheduling_data["Fri"] == "TRUE" else False,
                                    "Saturday":True if scheduling_data["Sat"] == "TRUE" else False
                                    }
            }

        return schedule_data_submit

    def parse_and_create_mediasite_folders(self, folders, parent_id=""):
        """
        Parse the provided path of folders in the GUI, delimeted by "/" and create each
        under the selected existing root folder within mediasite.

        returns:
            final mediasite folder id (lowest level folder)
        """
        if parent_id == "":
            parent_id = self.mediasite_model.get_root_parent_folder_id()

        folders_list = folders.split("/")

        #loop through our folders list creating each folder using the parent of the last
        for folder in folders_list:
            if folder != "":
                result = self.mediasite_create_folder(folder, parent_id)
                if "Id" in result:
                    parent_id = result["Id"]
                else:
                    break

        return parent_id

    def wait_for_job_to_complete(self, job_link_url):
        """
        Function for checking on and waiting for completion or error status of jobs in
        Mediasite system using Mediasite API.

        arguments:
            job_link_url: unique link to Mediasite job which can be used for gathering status
        """
        while 1:
            #gather information on the job status
            job_result = self.mediasite_api_client.do_request("get job", job_link_url, "", "")
            
            if self.experienced_request_errors(result):
                return result
            else:
                job_result_status = json.loads(job_result)["Status"]

                #if successful we return
                if job_result_status == "Successful":
                    logging.info("Job was successful")
                    return

                #if the job fails or is canceled for some reason exit
                elif job_result_status == "Disabled" or job_result_status == "Failed" or job_result_status == "Cancelled":
                    logging.error("Job "+presentation_report_execute_id+" did not complete successfully. Exiting.")
                    sys.exit()

                #if the job is queued or working we wait for the job to finish or fail
                else:
                    logging.info("Waiting for job to complete. Job status: "+job_result_status)
                    time.sleep(5)