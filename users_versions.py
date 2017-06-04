# extract users phone folders


import requests
import json
from datetime import datetime
import base_func

StartDate = '2017-05-01'
EndDate = '2017-05-01'
UserId = ''
EventName = ''
Version = ''
countries_code = ''

# function to extract users
def extract_users():
    data_users = {}

    response_js = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\April_17\\30_0417.json')

    # number of sessions=> number of lists need to access
    len_res_js = len(response_js['Sessions'])
    if len_res_js == 0:
        print('No data for the requested dates')
        exit()

    # enter each session. each session is a list of dictionaries
    for i in range(len_res_js):
        # remove internal users: Israel/ Ukraine
        if 'Location' in response_js['Sessions'][i]:
            country = response_js['Sessions'][i]['Location']['Country']
            if (country == 'UA') or (country == 'IL') or response_js['Sessions'][i]['Platform'] != 'Android':
                continue
            else:
                # find user id
                user_id = response_js['Sessions'][i]['UserId']
                if user_id not in data_users.keys():
                    data_users[user_id] = []
    print(data_users)
    return data_users


#function to extract version per user
def extract_versions(data_users):
    data_users_versions = data_users

    response_js = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\April_17\\30_0417.json')

    # number of sessions=> number of lists need to access
    len_res_js = len(response_js['Sessions'])

    # enter each session. each session is a list of dictionaries
    for i in range(len_res_js):
        # remove internal users: Israel/ Ukraine
        if 'Location' in response_js['Sessions'][i]:
            country = response_js['Sessions'][i]['Location']['Country']
            if (country == 'UA') or (country == 'IL'):
                continue
            else:
                # find user id
                user_id = response_js['Sessions'][i]['UserId']
                version = response_js['Sessions'][i]['AppVersion']
                if version not in data_users_versions[user_id]:
                    data_users_versions[user_id].append(version)
    print(data_users_versions)
    return data_users_versions


# func to calc number of users per version
def calc_users_per_version(data_users_versions):
    versions = {}
    for key_folder, value_folder in data_users_versions.items():
        if data_users_versions[key_folder] not in versions:
            versions[value_folder] = 0
        versions[value_folder] += 1
    print(versions)
    return versions

# func to calc number of users with X versions
def calc_versions_users(data_users_versions):
    num_users_in_version = {}
    for key, value in data_users_versions.items():
        num_versions = len(data_users_versions[key])
    #print(num_versions)
    return num_versions

#open a file to write the data
def write_results(data):
    with open('phone_folders.txt', 'a') as datafile:
        # print date and time
        base_func.print_time(datafile, StartDate, EndDate, Version)
        # print countries
        base_func.print_countries(datafile, countries_code)
        # print data
        base_func.print_dict(datafile, data)


extract_versions(extract_users())