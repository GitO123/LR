# monetization analysis

import base_func

StartDate = '2017-05-01'
EndDate = '2017-05-20'
UserId = ''
EventName = ''
Version = '0.9.2.2'
countries = []
countries_code = ''

# function to extract all sessions
# data structure: dictionary of skin types, values: user ids
def extract_data():
    data = {}
    data['users'] = []
    data['print_shop_clicked'] = []
    data['print_item_clicked'] = {}
    data['edit_click'] = []
    data['premium_bg_click'] = {}
    data['premium_bg_click_buy'] = {}

    response_js = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\May_17\\01_200517.json')

    # enter each session. each session is a list of dictionaries
    for a in range(len(response_js)):
        for i in range(len(response_js['Sessions'])):
            # remove internal users: Israel/ Ukraine
            if 'Location' in response_js['Sessions'][i]:
                loc = response_js['Sessions'][i]['Location']
                country = loc['Country']
                if (country == 'UA') or (country == 'IL'):
                    continue
                if response_js['Sessions'][i]['AppVersion'] != Version:
                    continue
                if ('Platform' in response_js['Sessions'][i]) and (response_js['Sessions'][i]['Platform'] != 'Android'):
                    continue
                else:
                    #countries = base_func.countries_set(countries_code)
                    #if country in countries:
                        user_id = response_js['Sessions'][i]['UserId']
                        if user_id not in data['users']:
                            data['users'].append(user_id)
                        if 'Events' in response_js['Sessions'][i]:
                            event = response_js['Sessions'][i]['Events']
                            # number of events need to review
                            len_event = len(event)
                            # enter every event
                            for j in range(len_event):
                                # print flow (print->buy print)
                                if event[j]['Name'] == 'print_shop_clicked':
                                    data['print_shop_clicked'].append(user_id)
                                if event[j]['Name'] == 'print_item_clicked':
                                    if 'Properties' in event[j]:
                                        if user_id not in data['print_item_clicked'].keys():
                                            data['print_item_clicked'][user_id] = []
                                        data['print_item_clicked'][user_id].append(event[j]['Properties']['item_name'])
                                # BG flow (edit->BG->buy BG)
                                if event[j]['Name'] == 'edit_click':
                                    data['edit_click'].append(user_id)
                                if event[j]['Name'] == 'premium_bg_click':
                                    if 'Properties' in event[j]:
                                        if user_id not in data['premium_bg_click'].keys():
                                            data['premium_bg_click'][user_id] = []
                                        data['premium_bg_click'][user_id].append(event[j]['Properties']['bg'])
                                if event[j]['Name'] == 'premium_bg_click_buy':
                                    if 'Properties' in event[j]:
                                        if user_id not in data['premium_bg_click_buy'].keys():
                                            data['premium_bg_click_buy'][user_id] = []
                                        data['premium_bg_click_buy'][user_id].append(event[j]['Properties']['bg'])
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
    with open('monetization_analysis.txt', 'a') as datafile:
        #print date and time
        base_func.print_time(datafile, StartDate, EndDate, Version)
        # print countries
        base_func.print_countries(datafile, countries_code)
        # print data
        base_func.print_dict(datafile, share_data)


#extract_data(StartDate, EndDate, UserId, EventName, Version)
#calc_clicks_users(extract_data(StartDate,EndDate, UserId, EventName, Version))
write_results(calc_clicks_users(extract_data()))

