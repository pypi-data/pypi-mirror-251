# This module is simply to provide a basic working example of data_access module. It is primitive and relies only on the
#   built error handling of the 'data_access.py' module. The basic command prompt is binded to these two functions below.  

#import needed libraries
import data_access
import time

# initialize classes from the data_access module
api_access = data_access.GetApiData()
export_api = data_access.ExportApiData()
tools = data_access.DataAccessToolkit()

# declaring some static global variables for storing parameters
export_file_path = "" 
api_key = ""
date = ""
ticker = ""
options_ticker = ""
base_url = ""

# generating the respective parameters into a python dict via library functions
settings = tools.settings()
req_params = tools.req_params()
file_paths = tools.file_paths()

# loading the required values into the global variables using the generated python dict
export_file_path = file_paths["api_files"]["api_export"]
api_key = settings["static"]["api_key"]
interval_time = settings["static"]["request_rate"]
dat = req_params['asset_parameters']["date"]
ticker = req_params["asset_parameters"]["ticker"]
options_ticker = req_params["asset_parameters"]["options_ticker"]

# function to test a basic implementation of the program. This will make one request and then write the sorted response to a .yaml AND a .json file
def test(endpoint_yaml) -> None:
    '''Just a test'''
    # dynamic parameter allocation with our generated dictionaries
    parameters = req_params[endpoint_yaml]["parameters"]
    base_url = req_params[endpoint_yaml]["url"]

    # create request url, make the request and then sort/stamp the response object in that order
    # Modules make a good one liner easy!
    # Can easily make the next three lines a one-liner 
    url = api_access.generate_request_url2(base_url, options_ticker, ticker, date, parameters)
    api_data = api_access.request_data(url, api_key)
    sorted_data = export_api.sort_api_data(api_data, url)

    # write data to .yaml and .json respectively
    export_api.write_yaml(export_file_path, sorted_data, "test.yaml")
    export_api.write_json(export_file_path, sorted_data, "test.json")
    return

# A more advanced example of how we can use pagination to automatically gather large amounts of data
def test_pagination(endpoint_yaml: str) -> None:
    '''Just a test'''

    parameters = req_params[endpoint_yaml]["parameters"]
    file_series_id = "test"
    loop = True

    base_url = req_params[endpoint_yaml]["url"]

    print("Accessing initial API call...")

    next_page_url = ""
    api_data = {}
    file_count = 0
    primary_url = ""
    file_name = "{}{}".format(file_series_id, str(file_count))

    primary_url = api_access.generate_request_url2(base_url, options_ticker, ticker, date, parameters)
    api_data = api_access.request_data(primary_url, api_key)
    sorted_data = export_api.sort_api_data(api_data, primary_url)

    print("Writing data to {}...".format(file_name))

    export_api.write_yaml(export_file_path, sorted_data, file_name)
    file_count += 1

    print("Done.")
    time.sleep(interval_time)
    
    while loop == True:
        next_page_url = ""
        page_url_stamp = "page_{}_from: {}".format(str(file_count), primary_url)
        file_name = "{}{}".format(file_series_id, str(file_count))
        for key, value in api_data.items():
            if key == "next_url":
                next_page_url = value
                print("Accessing data...")
                api_data = api_access.request_data(next_page_url, api_key)
                data_sorted = export_api.sort_api_data(api_data, page_url_stamp)
                print("Writing data to {}...".format(file_name))
                export_api.write_yaml(export_file_path, data_sorted, file_name)
                file_count += 1
                print("Done.")
                time.sleep(interval_time)
            elif key != "next_url":
                pass
            else:
                print("No more pages to get, terminating pagination stream!")
                break
    return