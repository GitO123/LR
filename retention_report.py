# retention report for api reachable pages

import json
from datetime import datetime, timedelta


# function to extract all sessions
# data structure: dictionary of all sessions. keys are user ids and values are list of dictionaries where each dictionary contains: country, date + time, duration, version, tm_collage
def extract_data():
    path = 'C:\\Users\\user\Documents\Projects\LifeReel\Data\\all\\0202_310517.json'
    with open(path, 'r') as data_file:
        response_js = json.loads(data_file.read())

        # all users and all sessions
        results = {}

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
                if (country == 'UA') or (country == 'IL'):
                    continue
                if 'UserId' not in response_js['Sessions'][i]:
                    continue
                if ('Platform' in response_js['Sessions'][i]) and (response_js['Sessions'][i]['Platform'] != 'Android'):
                    continue
                else:
                    user_id = response_js['Sessions'][i]['UserId']
                    # if the user_id does not exist in the results, create new entry to the dictionary
                    if user_id not in results.keys():
                        results[user_id] = []
                    # populating sessions per user
                    # object containing data for current session to add to user's data
                    current_session = {}
                    current_session['country'] = country
                    current_session['date_time'] = response_js['Sessions'][i]['StartTime']
                    current_session['duration'] = response_js['Sessions'][i]['Duration']
                    current_session['version'] = response_js['Sessions'][i]['AppVersion']
                    current_session['tm_collage'] = False
                    # check is it's a tm_collage user, if so, the False will turn to True
                    if 'Events' in response_js['Sessions'][i]:
                        event = response_js['Sessions'][i]['Events']
                        # number of events need to review
                        len_event = len(event)
                        # enter every event
                        for j in range(len_event):
                            # need to count only the 1st TM click
                            if (event[j]['Name'] == 'collage_created') and ('Properties' in event[j]) and (event[j]['Properties']['time_machine'] == 'true'):
                                current_session['tm_collage'] = True
                                break
                    # write the results to the dictionary
                    results[user_id].append(current_session)
            else:
                continue
    return results

# take only tm_collage users and their sessions
def filter_users_by_tm_collage(users):
    results = {}
    # for of the user id
    for user_id, user_sessions_list in users.items():
        # for of sessions
        for session in user_sessions_list:
            # if value is True
            if session['tm_collage']:
                results[user_id] = users[user_id]
                break
    return results

# take first sessions and sessions with delta of 15 min from previous and duration >= 4 sec of tm_collage users
def filter_users_by_delta_duration(users):
    results = {}
    filtered_results = {}
    # for of the user id
    for user_id, user_sessions_list in users.items():
        # order sessions per user by date_time asc
        # sorted_user-> list of dictionaries
        sorted_user = sorted(user_sessions_list, key = lambda k: k['date_time'])
        # results-> dictionary of lists of dictionaries
        #sorted sessions per user
        results[user_id] = sorted_user
        # first_sessions-> dictionary of lists of dictionaries
        sorted_user_len = len(sorted_user)
        # not taking 1st session to avoid duplicates in the calc section
        #filtered_results[user_id] = sorted_user[0]
        # find sessions with delta from previous 15 min
        if user_id not in filtered_results:
            filtered_results[user_id] = []
            filtered_results[user_id].append(sorted_user[0])
        for i in range(0, sorted_user_len-1, 1):
            date_time_object_i = datetime.strptime(sorted_user[i]['date_time'], '%Y-%m-%dT%H:%M:%S')
            date_time_object_i1 = datetime.strptime(sorted_user[i+1]['date_time'], '%Y-%m-%dT%H:%M:%S')
            delta = date_time_object_i1 - date_time_object_i
            if (delta >= timedelta(minutes=15)) and (sorted_user[i+1]['duration'] >= 4000):
                filtered_results[user_id].append(sorted_user[i+1])
    #print(filtered_results)
    return filtered_results


# find week num
def calc_week_num(date):
    date = date.split('T')[0]
    if date >= '2017-02-02' and date <= '2017-02-08':
        return 1
    elif date >= '2017-02-09' and date <= '2017-02-15':
        return 2
    elif date >= '2017-02-16' and date <= '2017-02-22':
        return 3
    elif date >= '2017-02-23' and date <= '2017-03-01':
        return 4
    elif date >= '2017-03-02' and date <= '2017-03-08':
        return 5
    elif date >= '2017-03-09' and date <= '2017-03-15':
        return 6
    elif date >= '2017-03-16' and date <= '2017-03-22':
        return 7
    elif date >= '2017-03-23' and date <= '2017-03-29':
        return 8
    elif date >= '2017-03-30' and date <= '2017-04-05':
        return 9
    elif date >= '2017-04-06' and date <= '2017-04-12':
        return 10
    elif date >= '2017-04-13' and date <= '2017-04-19':
        return 11
    elif date >= '2017-04-20' and date <= '2017-04-26':
        return 12
    elif date >= '2017-04-27' and date <= '2017-05-03':
        return 13
    elif date >= '2017-05-04' and date <= '2017-05-10':
        return 14
    elif date >= '2017-05-11' and date <= '2017-05-17':
        return 15
    elif date >= '2017-05-18' and date <= '2017-05-24':
        return 16
    elif date >= '2017-05-25' and date <= '2017-05-31':
        return 17

# calc registered and returning users in each week
def calc_registered_returning(users):
    # dictionary will contain week number as keys, each value will be another dictionary the will contain number of users started in the specific week and number of users returned each week
    weeks_data = {}
    #tests dictionary
    weeks_data_users = {}
    weeks_data_fin = {}
    # go over each user and populate weeks_data
    for user_id, user_sessions_list in users.items():
        # go over each session
        for i in range(len(users[user_id])):
            # find the date of the session
            date = (users[user_id][i]['date_time']).split('T')[0]
            # if it's the first session, populate the 'registered' field in the value dictionary per week
            if i == 0:
                # find the week of the start
                first_appear_week = calc_week_num(date)
                # if this week is not yet exists in the main dictionary (weeks_data) create the nested dictionary and populate it with 0
                if first_appear_week not in weeks_data:
                    weeks_data[first_appear_week] = {}
                    weeks_data_fin[first_appear_week] = {}
                    weeks_data[first_appear_week]['registered'] = 0
                    weeks_data_users[first_appear_week] = {}
                    weeks_data_users[first_appear_week]['registered'] = []
                # increase the value of the counter
                weeks_data[first_appear_week]['registered'] += 1
                weeks_data_fin[first_appear_week]['registered'] = weeks_data[first_appear_week]['registered']
                weeks_data_users[first_appear_week]['registered'].append(user_id)
            # if it's not the first session
            else:
                first_appear_date = (users[user_id][0]['date_time']).split('T')[0]
                first_appear_date_week = calc_week_num(first_appear_date)
                week = calc_week_num(date)
                # if the week of the session is not yet exist in the nested dictionary, create it (it's a dictionary)
                if week not in weeks_data[first_appear_date_week]:
                    weeks_data[first_appear_date_week][week] = {}
                    weeks_data_fin[first_appear_date_week][week] = {}
                    weeks_data[first_appear_date_week][week]['returning_users'] = 0
                    weeks_data_users[first_appear_date_week][week] = {}
                    weeks_data_users[first_appear_date_week][week]['returning_users'] = []
                # if the user id of the session is not yet exist in the nested dictionary, create it and populate with 0
                if user_id not in weeks_data[first_appear_date_week][week]:
                    weeks_data[first_appear_date_week][week][user_id] = 0
                    weeks_data[first_appear_date_week][week]['returning_users'] += 1
                    weeks_data_fin[first_appear_date_week][week]['returning_users'] = weeks_data[first_appear_date_week][week]['returning_users']
                    weeks_data_users[first_appear_date_week][week]['returning_users'].append(user_id)
                weeks_data[first_appear_date_week][week][user_id] += 1
    print(weeks_data_fin)
    print(weeks_data_users)
    return weeks_data_fin
    #return weeks_data_users

# calc retention per week
def calc_retention(weeks_data_fin):
    retention_per_week = {}
    for main_week in weeks_data_fin.keys():
        if main_week not in retention_per_week.keys():
            retention_per_week[main_week] = {}
            for inner_week in weeks_data_fin[main_week].keys():
                if inner_week != 'registered':
                    if inner_week not in retention_per_week[main_week].keys():
                        '''x= weeks_data_fin[main_week][inner_week]['returning_users']
                        y= weeks_data_fin[main_week]['registered']'''
                        retention_per_week[main_week][inner_week] = float(weeks_data_fin[main_week][inner_week]['returning_users'])/ float(weeks_data_fin[main_week]['registered'])
    return retention_per_week





#print(calc_registered_returning(filter_users_by_delta_duration(filter_users_by_tm_collage(extract_data()))))

print(calc_retention(calc_registered_returning(filter_users_by_delta_duration(filter_users_by_tm_collage(extract_data())))))

#print(calc_retention(calc_registered_returning(filter_users_by_delta_duration(extract_data()))))
