import base_func

StartDate = '2017-05-01'
EndDate = '2017-05-01'
UserId = ''
EventName = ''
Version = ''
countries_code = ''
Platform = 'Android'

# function to find the users that got 'launch' event
def find_launch_users():
    data = {}

    data_from_func = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\\15_200517.json')
    response_js = data_from_func

    # empty counters and all counters
    for i in range(len(response_js['Sessions'])):
        # remove internal users: Israel/ Ukraine
        if 'Location' in response_js['Sessions'][i]:
            country = response_js['Sessions'][i]['Location']['Country']
            if (country == 'UA') or (country == 'IL') or response_js['Sessions'][i]['Platform'] != Platform:
                continue
            else:
                user_id = response_js['Sessions'][i]['UserId']
                if 'Events' in response_js['Sessions'][i]:
                    event = response_js['Sessions'][i]['Events']
                    len_event = len(response_js['Sessions'][i]['Events'])
                    for j in range(len_event):
                        if (event[j]['Name'] == 'launch') and ('Properties' in event[j]) and ('app_installed' in event[j]['Properties']):
                            if user_id not in data.keys():
                                data[user_id] = {'tutorial_p_1' :0, 'tutorial_p_2' :0, 'tutorial_p_3' :0, 'tutorial_p_4' :0, 'first_tm_connect' :0}
    print(data)
    return data

find_launch_users()