# extract legit users, session dates and duration
# TM data and tokens data

import requests
import json
from datetime import datetime
import base_func
from collections import defaultdict

StartDate = '2017-02-02'
EndDate = '2017-02-04'
UserId = ''
EventName = ''
Version = ''

# function to extract all sessions and put the data in lists
def extract_data(StartDate,EndDate, UserId, EventName, Version):
    pages_num = (base_func.calc_pages(StartDate, EndDate, UserId, EventName, Version)) + 1
    data_from_func = base_func.extract_api(pages_num, StartDate, EndDate, UserId, EventName, Version)
    response_js = data_from_func
    json_num = len(response_js)

    data = defaultdict(list)
    # sessions date
    dates = []
    # users
    users = []
    # session's country
    countries = []
    # session duration
    durations = []
    # session's version
    versions = []

    # extract data while page is not empty
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
                    date = response_js[a]['Sessions'][i]['StartTime']
                    dates.append(date)
                    user_id = response_js[a]['Sessions'][i]['UserId']
                    users.append(user_id)
                    countries.append(country)
                    duration = response_js[a]['Sessions'][i]['Duration']
                    durations.append(duration)
                    version = response_js[a]['Sessions'][i]['AppVersion']
                    versions.append(version)
    data[users].append(users)
    data[dates].append(dates)
    data[durations].append(durations)
    data[versions].append(versions)
    data[countries].append(countries)
    return data

# function to extract all sessions and put the data in lists for TM sessions
def extract_data_tm(StartDate, EndDate, UserId, EventName, Version):
    pages_num = (base_func.calc_pages(StartDate, EndDate, UserId, EventName, Version)) + 1
    data_from_func = base_func.extract_api(pages_num, StartDate, EndDate, UserId, EventName, Version)
    response_js = data_from_func
    json_num = len(response_js)

    data = defaultdict(list)
    # sessions date
    dates = []
    # users
    users = []
    # session's country
    countries = []
    # session duration
    durations = []
    # session's version
    versions = []

    # extract data while page is not empty
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
                    if 'Events' in response_js[a]['Sessions'][i]:
                        event = response_js[a]['Sessions'][i]['Events']
                        # number of events need to review
                        len_event = len(event)
                        # enter every event
                        for j in range(len_event):
                            if event[j]['Name'] == 'collage_created':
                                if 'Properties' in event[j]:
                                    if event[j]['Properties']['time_machine'] == 'true':
                                        date = response_js[a]['Sessions'][i]['StartTime']
                                        dates.append(date)
                                        user_id = response_js[a]['Sessions'][i]['UserId']
                                        users.append(user_id)
                                        countries.append(country)
                                        duration = response_js[a]['Sessions'][i]['Duration']
                                        durations.append(duration)
                                        version = response_js[a]['Sessions'][i]['AppVersion']
                                        versions.append(version)
    data[users].append(users)
    data[dates].append(dates)
    data[durations].append(durations)
    data[versions].append(versions)
    data[countries].append(countries)
    return data

# function to extract all sessions and put the data in lists for tokens event
def extract_data_tokens(StartDate, EndDate, UserId, EventName, Version):
    pages_num = (base_func.calc_pages(StartDate, EndDate, UserId, EventName, Version)) + 1
    data_from_func = base_func.extract_api(pages_num, StartDate, EndDate, UserId, EventName, Version)
    response_js = data_from_func
    json_num = len(response_js)

    data = defaultdict(list)
    # sessions date
    dates = []
    # users
    users = []
    # session's country
    countries = []
    # session duration
    durations = []
    # session's version
    versions = []
    # token
    tokens = []

    # extract data while page is not empty
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
                    if 'Events' in response_js[a]['Sessions'][i]:
                        event = response_js[a]['Sessions'][i]['Events']
                        # number of events need to review
                        len_event = len(event)
                        # enter every event
                        for j in range(len_event):
                            if event[j]['Name'] == 'token_sent':
                                if 'Properties' in event[j]:
                                    if 'token' in event[j]['Properties']:
                                        date = response_js[a]['Sessions'][i]['StartTime']
                                        dates.append(date)
                                        user_id = response_js[a]['Sessions'][i]['UserId']
                                        users.append(user_id)
                                        countries.append(country)
                                        duration = response_js[a]['Sessions'][i]['Duration']
                                        durations.append(duration)
                                        version = response_js[a]['Sessions'][i]['AppVersion']
                                        versions.append(version)
                                        token = response_js[a]['Sessions'][i]['AppVersion']
                                        tokens.append(token)
    data[users].append(users)
    data[dates].append(dates)
    data[durations].append(durations)
    data[versions].append(versions)
    data[countries].append(countries)
    data[tokens].append(tokens)
    return data

def write_results(results):
    with open('users_data.txt', 'a') as datafile:
        # print time
        base_func.print_time(datafile, StartDate, EndDate, Version)
        # print data
        base_func.resultsFile.write("all sessions")
        base_func.print_dict(datafile, extract_data(StartDate, EndDate, UserId, EventName, Version))
        base_func.resultsFile.write("TM sessions")
        base_func.print_dict(datafile, extract_data_tm(StartDate, EndDate, UserId, EventName, Version))
        base_func.resultsFile.write("token sessions")
        base_func.print_dict(datafile, extract_data_tokens(StartDate, EndDate, UserId, EventName, Version))