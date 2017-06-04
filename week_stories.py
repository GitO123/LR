# skins analysis

import base_func

StartDate = '2017-04-20'
EndDate = '2017-05-04'
UserId = ''
EventName = ''
Version = ''
countries = []
countries_code = ''

# function to extract all sessions
# data structure: dictionary of skin types, values: user ids
def extract_data(StartDate,EndDate, UserId, EventName, Version):
    pages_num = (base_func.calc_pages(StartDate, EndDate, UserId, EventName, Version)) + 1
    data = {}
    data['collage_weekly'] = []
    data['collage_event'] = []
    data['share_weekly'] = []
    data['share_event'] = []
    print(pages_num)


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
                    #countries = base_func.countries_set(countries_code)
                    #if country in countries:
                        user_id = response_js[a]['Sessions'][i]['UserId']
                        if 'Events' in response_js[a]['Sessions'][i]:
                            event = response_js[a]['Sessions'][i]['Events']
                            # number of events need to review
                            len_event = len(event)
                            # enter every event
                            for j in range(len_event):
                                # check if the skin selection event
                                if event[j]['Name'] == 'collage_created':
                                    if 'Properties' in event[j]:
                                        if 'type' in event[j]['Properties']:
                                            # add the user who share the type to the list of share types users
                                            if event[j]['Properties']['type'] == 'weekly':
                                                data['collage_weekly'].append(user_id)
                                            if event[j]['Properties']['type'] == 'event':
                                                data['collage_event'].append(user_id)
                                if event[j]['Name'] == 'share_collage_open':
                                    if 'Properties' in event[j]:
                                        if 'type' in event[j]['Properties']:
                                            # add the user who share the type to the list of share types users
                                            if event[j]['Properties']['type'] == 'weekly':
                                                data['share_weekly'].append(user_id)
                                            if event[j]['Properties']['type'] == 'event':
                                                data['share_event'].append(user_id)
    print(data)
    return data


# calc number of clicks per skin type and number of unique users
def calc_clicks_users(type_shares):
    share_data = {}
    for key, value in type_shares.items():
        if key not in share_data.keys():
            share_data[key] = []
            share_data[key].append(len(type_shares[key]))
            share_data[key].append(len(set(type_shares[key])))
    return share_data


# write results to file
def write_results(share_data):
    with open('share_data.txt', 'a') as datafile:
        #print date and time
        base_func.print_time(datafile, StartDate, EndDate, Version)
        # print countries
        base_func.print_countries(datafile, countries_code)
        # print data
        base_func.print_dict(datafile, share_data)

#calc_clicks_users(extract_data(StartDate,EndDate, UserId, EventName, Version))
write_results(calc_clicks_users(extract_data(StartDate,EndDate, UserId, EventName, Version)))
