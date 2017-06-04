# users by countries analysis

import base_func

StartDate = '2017-05-18'
EndDate = '2017-05-20'
UserId = ''
EventName = ''
Version = ''
countries = []
countries_code = 'Latm'
Platform = 'Android'

# function to extract all sessions
def extract_data():
    data = {}

    response_js = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\\15_200517.json')

    # enter each session. each session is a list of dictionaries
    for i in range(len(response_js['Sessions'])):
        # remove internal users: Israel/ Ukraine
        if 'Location' in response_js['Sessions'][i]:
            loc = response_js['Sessions'][i]['Location']
            country = loc['Country']
            if (country == 'UA') or (country == 'IL'):
                continue
            if response_js['Sessions'][i]['Platform'] != Platform:
                continue
            else:
                countries = base_func.countries_set(countries_code)
                if country in countries:
                    user_id = response_js['Sessions'][i]['UserId']
                    if country not in data.keys():
                        data[country] = {}
                    if user_id not in data[country].keys():
                        data[country][user_id] = {}
                        data[country][user_id]['request_count'] = 0
                        data[country][user_id]['response_count'] = 0
                    if 'Events' in response_js['Sessions'][i]:
                        event = response_js['Sessions'][i]['Events']
                        # number of events need to review
                        len_event = len(event)
                        # enter every event
                        for j in range(len_event):
                            if event[j]['Name'] == 'i2t_counter':
                                data[country][user_id]['request_count'] += int(event[j]['Properties']['request_count'])
                                data[country][user_id]['response_count'] += int(event[j]['Properties']['response_count'])
                            if (event[j]['Name'] == 'i2t_response_received') and ('message' in event[j]['Properties']):
                                if event[j]['Properties']['message'] not in data[country][user_id].keys():
                                    data[country][user_id][event[j]['Properties']['message']] = 0
                                data[country][user_id][event[j]['Properties']['message']] += 1
    print(data)
    return data


# calc number of clicks per skin type and number of unique users
def calc_events_users(data):
    share_data = {}
    for key, value in data.items():
        if key not in share_data.keys():
            share_data[key] = {}
            share_data[key]['users_num'] = len(data[key])
            for key1, value1 in data[key].items():
                for key2, value2 in data[key][key1].items():
                    if key2 not in share_data[key].keys():
                        share_data[key][key2] = 0
                    share_data[key][key2] = share_data[key][key2] + value2
    print(share_data)
    return share_data


# write results to file
def write_results(share_data):
    with open('users_countries.txt', 'a') as datafile:
        # print date and time
        base_func.print_time(datafile, StartDate, EndDate, Version)
        # print countries
        base_func.print_countries(datafile, countries_code)
        # print data
        base_func.print_dict(datafile, share_data)





# function to check number of sessions that contained requests and/or error and type of connectivity
def extract_i2t_sessions():
    data_i2t = {}

    response_js = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\\20_0517.json')

    # enter each session. each session is a list of dictionaries
    for i in range(len(response_js['Sessions'])):
        # remove internal users: Israel/ Ukraine
        if 'Location' in response_js['Sessions'][i]:
            country = response_js['Sessions'][i]['Location']['Country']
            connectivity = response_js['Sessions'][i]['Connectivity']
            if (country == 'UA') or (country == 'IL'):
                continue
            '''if response_js['Sessions'][i]['UserId'] != '161cdf511ef41ca2_1495293097712':
                continue
            if country != 'PE':
                continue'''
            if response_js['Sessions'][i]['Platform'] != Platform:
                continue
            else:
                countries = base_func.countries_set(countries_code)
                if country in countries:
                    if country not in data_i2t.keys():
                        data_i2t[country] = {}
                        data_i2t[country]['requests'] = {}
                        data_i2t[country]['errors'] = {}
                    user_id = response_js['Sessions'][i]['UserId']
                    if 'Events' in response_js['Sessions'][i]:
                        event = response_js['Sessions'][i]['Events']
                        # number of events need to review
                        len_event = len(event)
                        # enter every event
                        for j in range(len_event):
                            if (event[j]['Name'] == 'i2t_counter') and (event[j]['Properties']['request_count']):
                                if connectivity not in data_i2t[country]['requests'].keys():
                                    data_i2t[country]['requests'][connectivity] = 0
                                data_i2t[country]['requests'][connectivity] += int(event[j]['Properties']['request_count'])
                            if (event[j]['Name'] == 'i2t_response_received') and ('Properties' in event[j]) and ('message' in event[j]['Properties']):
                                if connectivity not in data_i2t[country]['errors'].keys():
                                    data_i2t[country]['errors'][connectivity] = 0
                                data_i2t[country]['errors'][connectivity] += 1
                                '''if country == 'PE':
                                    print(user_id)'''
    print(data_i2t)
    return data_i2t

#write_results(extract_i2t_sessions())
#write_results(calc_events_users(extract_data(StartDate,EndDate, UserId, EventName, Version, Platform)))

extract_data()