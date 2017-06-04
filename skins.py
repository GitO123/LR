# skins analysis

import json
from datetime import datetime
import base_func

StartDate = '2017-04-20'
EndDate = '2017-04-23'
UserId = ''
EventName = ''
Version = '0.9.1.3'

# function to extract all sessions
# data structure: dictionary of skin types, values: user ids
def extract_data(StartDate,EndDate, UserId, EventName, Version):
    pages_num = (base_func.calc_pages(StartDate, EndDate, UserId, EventName, Version)) + 1
    data = {}

    data_from_func = base_func.extract_api(pages_num, StartDate, EndDate, UserId, EventName, Version)
    response_js = data_from_func
    json_num = len(response_js)

    # enter each session. each session is a list of dictionaries
    for a in range(json_num):
        for i in range(len(response_js[a]['Sessions'])):
            # remove internal users: Israel/ Ukraine
            if 'Location' in response_js[a]['Sessions'][i]:
                loc = response_js[a]['Sessions'][i]['Location']
                country = loc['Country']
                if (country == 'UA') or (country == 'IL'):
                    continue
                else:
                    if (country == 'US') or (country == 'GB') or (country == 'ZA') or (country == 'AU') or (country == 'CA'):
                        user_id = response_js[a]['Sessions'][i]['UserId']
                        if 'Events' in response_js[a]['Sessions'][i]:
                            event = response_js[a]['Sessions'][i]['Events']
                            # number of events need to review
                            len_event = len(event)
                            # enter every event
                            for j in range(len_event):
                                # check if the skin selection event
                                if event[j]['Name'] == 'select_skin_click':
                                    if 'Properties' in event[j]:
                                        # if the skin name is not yet in the dictionary, add it
                                        if event[j]['Properties']['skin_name'] not in data.keys():
                                            data[event[j]['Properties']['skin_name']] = []
                                        # add the user who clicked the skin to the list of skin type users
                                        data[event[j]['Properties']['skin_name']].append(user_id)
    return data


# calc number of clicks per skin type and number of unique users
def calc_clicks_users(clicks_dict):
    skin_type_data = {}
    for key, value in clicks_dict.items():
        if key not in skin_type_data.keys():
            skin_type_data[key] = []
        skin_type_data[key].append(len(clicks_dict[key]))
        skin_type_data[key].append(len(set(clicks_dict[key])))
    return skin_type_data


# write results to file
def write_results(skin_type_data):
    with open('skins_analysis.txt', 'a') as datafile:
        #print date and time
        base_func.print_time(datafile, StartDate, EndDate, Version)
        # print data
        base_func.print_dict(datafile, skin_type_data)


write_results(calc_clicks_users(extract_data(StartDate,EndDate, UserId, EventName, Version)))
