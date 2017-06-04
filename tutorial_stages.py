# tag_counter analysis

import base_func

StartDate = '2017-05-01'
EndDate = '2017-05-01'
UserId = ''
EventName = ''
Version = '0.9.2.2'
countries_code = 'Latm'

# function to find the users that got 'launch' event
def find_launch_users():
    data = {}

    data_from_func = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\\01_070517.json')
    response_js = data_from_func

    # empty counters and all counters
    for i in range(len(response_js['Sessions'])):
        # remove internal users: Israel/ Ukraine
        if 'Location' in response_js['Sessions'][i]:
            country = response_js['Sessions'][i]['Location']['Country']
            if (country == 'UA') or (country == 'IL'):
                continue
            else:
                countries = base_func.countries_set(countries_code)
                if country in countries:
                    if response_js['Sessions'][i]['AppVersion'] == '0.9.2.2':
                        user_id = response_js['Sessions'][i]['UserId']
                        if 'Events' in response_js['Sessions'][i]:
                            event = response_js['Sessions'][i]['Events']
                            len_event = len(response_js['Sessions'][i]['Events'])
                            for j in range(len_event):
                                if (event[j]['Name'] == 'launch') and ('Properties' in event[j]) and ('app_installed' in event[j]['Properties']):
                                    if user_id not in data.keys():
                                        data[user_id] = {'tutorial_p_1' :0, 'tutorial_p_2' :0, 'tutorial_p_3' :0, 'tutorial_p_4' :0, 'first_tm_connect' :0}
    return data


# function to find the users that got 'launch' event and tutorial pages
def find_launch_tutorial_users(data_launch):
    data = data_launch

    data_from_func = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\\01_070517.json')
    response_js = data_from_func

    # empty counters and all counters
    for i in range(len(response_js['Sessions'])):
        # remove internal users: Israel/ Ukraine
        if 'Location' in response_js['Sessions'][i]:
            country = response_js['Sessions'][i]['Location']['Country']
            if (country == 'UA') or (country == 'IL'):
                continue
            else:
                countries = base_func.countries_set(countries_code)
                if country in countries:
                    if response_js['Sessions'][i]['AppVersion'] == '0.9.2.2':
                        user_id = response_js['Sessions'][i]['UserId']
                        if 'Events' in response_js['Sessions'][i]:
                            event = response_js['Sessions'][i]['Events']
                            len_event = len(response_js['Sessions'][i]['Events'])
                            for j in range(len_event):
                                if (event[j]['Name'] == 'tutorial_page') and ('Properties' in event[j]):
                                    if 'page_number' in event[j]['Properties']:
                                        if event[j]['Properties']['page_number'] == 1:
                                            if (user_id in data.keys()) and (data[user_id]['tutorial_p_1'] < 1):
                                                data[user_id]['tutorial_p_1'] =1
                                        elif event[j]['Properties']['page_number'] == 2:
                                            if (user_id in data.keys()) and (data[user_id]['tutorial_p_2'] < 1):
                                                data[user_id]['tutorial_p_2'] =1
                                        elif event[j]['Properties']['page_number'] == 3:
                                            if (user_id in data.keys()) and (data[user_id]['tutorial_p_3'] < 1):
                                                data[user_id]['tutorial_p_3'] =1
                                        elif event[j]['Properties']['page_number'] == 4:
                                            if (user_id in data.keys()) and (data[user_id]['tutorial_p_4'] < 1):
                                                data[user_id]['tutorial_p_4'] =1
                                '''if ((event[j]['Name'] == 'first_collage_created') and ('Properties' in event[j]) and('creation_duration' in event[j]['Properties']))\
                                    or (event[j]['Name'] == 'time_machine_clicked')\
                                    or (event[j]['Name'] == 'cloud_connect_suggestion')\
                                    or (event[j]['Name'] == 'Google Drive State'):'''
                                if (event[j]['Name'] == 'time_machine_clicked') \
                                   or (event[j]['Name'] == 'cloud_connect_suggestion') \
                                   or (event[j]['Name'] == 'Google Drive State'):
                                        if (user_id in data.keys()) and (data[user_id]['first_tm_connect'] < 1):
                                            data[user_id]['first_tm_connect'] = 1
                            if 'Screens' in response_js['Sessions'][i]:
                                screen = response_js['Sessions'][i]['Screens']
                                len_screen = len(screen)
                                for j in range(len_screen):
                                    if screen[j]['Name'] == 'Feed':
                                        if (user_id in data.keys()) and (data[user_id]['first_tm_connect'] < 1):
                                            data[user_id]['first_tm_connect'] = 1
    print(data)
    return data

def calc_tutorial_users(tutorial_users):
    summary = {'launch' :0, 'tutorial_p_1' :0, 'tutorial_p_2' :0, 'tutorial_p_3' :0, 'tutorial_p_4' :0, 'first_tm_connect' :0}
    summary['launch'] = len(tutorial_users)
    for key, value in tutorial_users.items():
        if tutorial_users[key]['tutorial_p_1'] > 0:
            summary['tutorial_p_1'] += 1
        if tutorial_users[key]['tutorial_p_2'] > 0:
            summary['tutorial_p_2'] += 1
        if tutorial_users[key]['tutorial_p_3'] > 0:
            summary['tutorial_p_3'] += 1
        if tutorial_users[key]['tutorial_p_4'] > 0:
            summary['tutorial_p_4'] += 1
        if tutorial_users[key]['first_tm_connect'] > 0:
            summary['first_tm_connect'] += 1
    print(summary)
    return summary


# write results to file
def write_results(data):
    with open('tutorial_stages.txt', 'a') as datafile:
        # print date and time
        base_func.print_time(datafile, StartDate, EndDate, Version)
        # print countries
        base_func.print_countries(datafile, countries_code)
        # print data
        base_func.print_dict(datafile, data)


write_results(calc_tutorial_users(find_launch_tutorial_users(find_launch_users())))
