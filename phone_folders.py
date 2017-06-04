# extract users phone folders


import requests
import json
from datetime import datetime
import base_func

StartDate = '2017-05-01'
EndDate = '2017-05-20'
UserId = ''
EventName = ''
Version = '0.9.2.2'
countries_code = ''

# function to extract users
def extract_users():
    data_users = {}

    response_js = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\May_17\\01_200517.json')

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
            if (country == 'UA') or (country == 'IL') or (response_js['Sessions'][i]['AppVersion'] != Version):
                continue
            else:
                # find user id
                user_id = response_js['Sessions'][i]['UserId']
                if user_id not in data_users.keys():
                    data_users[user_id] = {}
    print(data_users)
    return data_users


#function to extract gallery and folders per user
def extract_data(data_users):
    data = data_users

    response_js = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\May_17\\01_200517.json')

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
            if (country == 'UA') or (country == 'IL') or (response_js['Sessions'][i]['AppVersion'] != Version):
                continue
            else:
                # find user id
                user_id = response_js['Sessions'][i]['UserId']
                if 'Events' in response_js['Sessions'][i]:
                    event = response_js['Sessions'][i]['Events']
                    # number of events need to review
                    len_event = len(event)
                    # enter every event
                    for j in range(len_event):
                        if (event[j]['Name'] == 'gallery_size') and ('Properties' in event[j]) and ('gallery_size' in event[j]['Properties']):
                            data[user_id]['gallery_size'] = event[j]['Properties']['gallery_size']
                        if (event[j]['Name'] == 'photo_folders') and ('Properties' in event[j]):
                                for key_folder, value_folder in event[j]['Properties'].items():
                                    # print(event[j]['Properties'][key])
                                    # if the folder doesn't exist yet in the dictionary, create it, otherwise, add the user id
                                    if key_folder not in data[user_id].keys():
                                        data[user_id][key_folder] = {}
                                        # populate dictionary value with the key, user id and value, number of folder photos
                                    data[user_id][key_folder] = value_folder
    print(data)
    return data


#function to extract users per folders
def extract_folders():
    phone_folders = {}

    response_js = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\May_17\\01_200517.json')

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
            if (country == 'UA') or (country == 'IL') or (response_js['Sessions'][i]['AppVersion'] != Version):
                continue
            else:
                # find user id
                user_id = response_js['Sessions'][i]['UserId']
                if 'Events' in response_js['Sessions'][i]:
                    event = response_js['Sessions'][i]['Events']
                    # number of events need to review
                    len_event = len(event)
                    # enter every event
                    for j in range(len_event):
                        if event[j]['Name'] == 'photo_folders':
                            if 'Properties' in event[j]:
                                for key_folder, value_folder in event[j]['Properties'].items():
                                    # print(event[j]['Properties'][key])
                                    # if the folder doesn't exist yet in the dictionary, create it, otherwise, add the user id
                                    if key_folder not in phone_folders:
                                        phone_folders[key_folder] = {}
                                        # populate dictionary value with the key, user id and value, number of folder photos
                                    phone_folders[key_folder][user_id] = value_folder
    print(phone_folders)
    return phone_folders


# func to calc avg number of photos per folder
def calc_avg_num_photos_folder(phone_folders):
    avg_phone_folders = {}
    for key_folder, value_folder in phone_folders.items():
        avg_phone_folders[key_folder] = "{:.2f}".format(sum(phone_folders[key_folder].values()) / float(len(list(phone_folders[key_folder].values()))))
    print(avg_phone_folders)
    return avg_phone_folders

# func to calc number of unique users per folder
def phone_folder_users(phone_folders):
    phone_folders_users = {}
    for key, value in phone_folders.items():
        phone_folders_users[key] = len(set(phone_folders[key]))
    #print(phone_folders_users)
    return phone_folders_users

#open a file to write the data
def write_results(data):
    with open('phone_folders.txt', 'a') as datafile:
        # print date and time
        base_func.print_time(datafile, StartDate, EndDate, Version)
        # print countries
        base_func.print_countries(datafile, countries_code)
        # print data
        base_func.print_dict(datafile, data)


#extract_data(extract_users())
#calc_avg_num_photos_folder(extract_folders())

write_results(extract_folders())
write_results(calc_avg_num_photos_folder(extract_folders()))
write_results(phone_folder_users(extract_folders()))