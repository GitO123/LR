# skins analysis

import json
from datetime import datetime
import base_func

StartDate = '2017-02-21'
EndDate = '2017-03-02'
UserId = ''
EventName = ''
Version = ''

# function to extract all sessions
# data structure: dictionary of user ids, values: tokens if exist
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
                    user_id = response_js[a]['Sessions'][i]['UserId']
                    if user_id not in data.keys():
                        data[user_id] = []
                    if 'Events' in response_js[a]['Sessions'][i]:
                        event = response_js[a]['Sessions'][i]['Events']
                        # number of events need to review
                        len_event = len(event)
                        # enter every event
                        for j in range(len_event):
                            if event[j]['Name'] == 'token_sent':
                                if 'Properties' in event[j]:
                                    if 'token' in event[j]['Properties']:
                                        data[user_id].append(event[j]['Properties']['token'])
    return data


# calc number of users for each category
def calc_tokens_users(users_tokens):
    results = [0]*3
    # number of users (results[0]), number of users with legit tokens (results[1]), number of users with no token/ BL (results[2])
    results[0] = len(users_tokens)
    for key, value in users_tokens.items():
        if (len(users_tokens[key])) > 0:
            for i in range(len(users_tokens[key])):
                if users_tokens[key][i] == 'BLACKLISTED':
                    results[2] += 1
                    break
        else:
            results[2] += 1
        results[1] = results[0] - results[2]
    return results


# write results to file
def write_results(results):
    with open('notification_report.txt', 'a') as datafile:
        base_func.print_time(datafile, StartDate, EndDate, Version)
        # print data
        datafile.write("results: " + str(results))
        datafile.write('\n')
        datafile.write('\n')

#calc_tokens_users(extract_data(StartDate,EndDate, UserId, EventName, Version))
write_results(calc_tokens_users(extract_data(StartDate,EndDate, UserId, EventName, Version)))
