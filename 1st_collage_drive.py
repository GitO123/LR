# all users - 1st collage - drive analysis

import base_func

StartDate = '2017-05-01'
EndDate = '2017-05-09'
UserId = ''
EventName = ''
Version = '0.9.2.2'
countries = []
countries_code = 'Latm'
Platform = 'android'

# extract all user ids
def extract_users(StartDate,EndDate, UserId, EventName, Version, Platform):
    pages_num = (base_func.calc_pages(StartDate, EndDate, UserId, EventName, Version, Platform)) + 1
    data = {}


    data_from_func = base_func.extract_api(pages_num, StartDate, EndDate, UserId, EventName, Version, Platform)
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
                    countries = base_func.countries_set(countries_code)
                    if country in countries:
                        user_id = response_js[a]['Sessions'][i]['UserId']
                        if 'Events' in response_js[a]['Sessions'][i]:
                            event = response_js[a]['Sessions'][i]['Events']
                            # number of events need to review
                            len_event = len(event)
                            # enter every event
                            for j in range(len_event):
                                if (event[j]['Name'] == 'launch') and ('Properties' in event[j]) and (event[j]['Properties']['app_installed'] == 'true'):
                                    if user_id not in data.keys():
                                        data[user_id] = {}
                                        data[user_id]['1st_collage'] = 0
                                        data[user_id]['drive_click_connect'] = 0
                                        data[user_id]['drive_connection'] = 0
    return data

#extract data
def extract_data(StartDate,EndDate, UserId, EventName, Version, data):
    pages_num = (base_func.calc_pages(StartDate, EndDate, UserId, EventName, Version, Platform)) + 1

    data_from_func = base_func.extract_api(pages_num, StartDate, EndDate, UserId, EventName, Version, Platform)
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
                    countries = base_func.countries_set(countries_code)
                    if country in countries:
                        user_id = response_js[a]['Sessions'][i]['UserId']
                        if user_id in data.keys():
                            if 'Events' in response_js[a]['Sessions'][i]:
                                event = response_js[a]['Sessions'][i]['Events']
                                for j in range(len(event)):
                                    if (event[j]['Name'] == 'first_collage_created') and (data[user_id]['1st_collage'] < 1):
                                        data[user_id]['1st_collage'] += 1
                                    if event[j]['Name'] == 'Google Drive State':
                                        if ('Properties' in event[j]) and (event[j]['Properties']['Connected'] == 'true') and (data[user_id]['drive_connection'] < 1):
                                                data[user_id]['drive_connection'] += 1
                            if 'Screens' in response_js[a]['Sessions'][i]:
                                screen = response_js[a]['Sessions'][i]['Screens']
                                for j in range(len(screen)):
                                    if len(screen[j]['Actions']) > 0:
                                        for k in range(len(screen[j]['Actions'])):
                                            if 'Description' in screen[j]['Actions'][k]:
                                                # during onboarding drive connection preference
                                                if (screen[j]['Actions'][k]['Description'] == 'Connect' or screen[j]['Actions'][k]['Description'] == 'Conectar' or screen[j]['Actions'][k]['Description'] == 'Conectar-se') and (data[user_id]['drive_click_connect'] < 1):
                                                    data[user_id]['drive_click_connect'] += 1
                                                if (screen[j]['Actions'][k]['Description'] == 'CONNECT GOOGLE PHOTOS' or screen[j]['Actions'][k]['Description'] == 'CONECTAR GOOGLE FOTOS' or screen[j]['Actions'][k]['Description'] == 'CONECTAR-SE AO GOOGLE PHOTOS') and (data[user_id]['drive_click_connect'] < 1):
                                                    data[user_id]['drive_click_connect'] += 1
    return data


# write results to file
def write_results(share_data):
    with open('users_1stcollage_drive.txt', 'a') as datafile:
        #print date and time
        base_func.print_time(datafile, StartDate, EndDate, Version)
        # print countries
        base_func.print_countries(datafile, countries_code)
        # print data
        base_func.print_dict(datafile, share_data)


write_results(extract_data(StartDate, EndDate, UserId, EventName, Version, extract_users(StartDate, EndDate, UserId, EventName, Version, Platform)))

