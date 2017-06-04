# basic functions

import requests
import json
from datetime import datetime

# print functions
def print_time(resultsFile, StartDate, EndDate, Version):
    date = str(datetime.now().date())
    time = str(datetime.now().time())
    time_print = str(time).split(".")[0]
    resultsFile.write("date: " + date)
    resultsFile.write("\t")
    resultsFile.write("time: " + time_print)
    resultsFile.write("\n")
    resultsFile.write("start date: " + str(StartDate) + " end date: " + str(EndDate))
    resultsFile.write("\n")
    resultsFile.write("version: " + Version)
    resultsFile.write("\n")

def print_numeric_data (resultsFile, text_value, list_value):
    resultsFile.write(text_value)
    resultsFile.write(" len: " + str(len(list_value)))
    resultsFile.write("\n")
    return

def print_values(resultsFile, text_value, list_value):
    resultsFile.write(text_value)
    resultsFile.write(" : ")
    resultsFile.write(str(list_value))
    resultsFile.write("\n")
    return

def print_dict(resultsFile, data):
    json.dump(data, resultsFile)
    resultsFile.write('\n')
    resultsFile.write('\n')
    return

# print report countries set
def return_countries(set_name):
    countries = ''
    if set_name == 'US':
        countries = 'US'
    if set_name == 'Latm':
        countries = 'Latm'
    return countries

# print countries
def print_countries(resultsFile, countries_code):
    resultsFile.write("countries: ")
    resultsFile.write(return_countries(countries_code))
    resultsFile.write("\n")

# extract data from api
def extract_api(pages_num, StartDate, EndDate, UserId, EventName, Version, Platform):
    REQUEST_URL_SESSIONS = 'https://api.appsee.com/sessions'
    REEL_API_KEY = 'a8e66d00f6c54a65a3d65c1ff15aedf7'
    API_SECRET = '73f95ae4f566490ba8ba89bef0f6e5ea'
    results = []
    for i in range(1, pages_num):
        url_Template_i = '?apikey=' + REEL_API_KEY + '&apisecret=' + API_SECRET + '&fromdate=' + str(StartDate) + '&todate=' \
                         + str(EndDate) + '&userid=' + str(UserId) + '&eventname=' + str(EventName) + '&appversion=' + str(Version) + '&page=%d' % i + '&platform=' + str(Platform)
        url = REQUEST_URL_SESSIONS + url_Template_i
        response = requests.get(url).text
        response_js = json.loads(response)
        results.append(response_js)
    return results


# extract data from file
def extract_file(path):
    with open(path, 'r') as data_file:
        response_js = json.loads(data_file.read())
    return response_js

#write data to json file
def write_json_results(file_name, data):
    with open(file_name, 'a') as datafile:
        # print data
        print_dict(datafile, data)


#
def calc_pages(StartDate, EndDate, UserId, EventName, Version, Platform):
    REQUEST_URL_SESSIONS = 'https://api.appsee.com/sessions'
    REEL_API_KEY = 'a8e66d00f6c54a65a3d65c1ff15aedf7'
    API_SECRET = '73f95ae4f566490ba8ba89bef0f6e5ea'
    # values of the 1st page
    page = 1
    pages_num = 0

    url_Template_1 = '?apikey=' + REEL_API_KEY + '&apisecret=' + API_SECRET + '&fromdate=' + str(StartDate) + '&todate=' \
                     + str(EndDate) + '&userid=' + str(UserId) + '&eventname=' + str(EventName) + '&appversion=' + str(Version) + '&page=%d' % page + '&platform=' + str(Platform)
    url = REQUEST_URL_SESSIONS + url_Template_1
    response = requests.get(url).text
    response_js = json.loads(response)
    # number of sessions=> number of lists need to access
    len_res_js = len(response_js['Sessions'])
    if len_res_js == 0:
        print('No data for the requested dates')
        exit()
    # extract data while page is not empty
    while (len_res_js) > 0:
        pages_num += 1

        page += 1
        url_Template_2 = '?apikey=' + REEL_API_KEY + '&apisecret=' + API_SECRET + '&fromdate=' + str(StartDate) + '&todate=' + \
                         str(EndDate) + '&userid=' + str(UserId) + '&eventname=' + str(EventName) + '&appversion=' + str(Version) + '&page=%d' % page + '&platform=' + str(Platform)
        url = REQUEST_URL_SESSIONS + url_Template_2
        response = requests.get(url).text
        response_js = json.loads(response)
        len_res_js = len(response_js['Sessions'])
    return pages_num

# countries
def countries_set(set_name):
    countries_set = []
    if set_name == 'US':
        countries_set = ['US', 'GB', 'ZA', 'AU', 'CA']
    if set_name == 'Latm':
        countries_set = ['AR', 'BO', 'BR', 'CL', 'CO', 'EC', 'JM', 'MX', 'PA', 'PE', 'PR', 'ES', 'UY']
    return countries_set


def merge_jsons(path_1, path_2):
    data_temp = []
    data = {}
    data["Sessions"] = []
    file_1 = extract_file(path_1)
    file_1_values = file_1['Sessions']
    file_2 = extract_file(path_2)
    file_2_values = file_2['Sessions']
    #file_3 = extract_file(path_3)
    #file_3_values = file_3['Sessions']
    data_temp.extend(file_1_values)
    data_temp.extend(file_2_values)
    #data_temp.extend(file_3_values)
    data["Sessions"] = data_temp
    return data