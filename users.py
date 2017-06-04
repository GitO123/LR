# extract users phone folders


import base_func

StartDate = '2017-05-01'
EndDate = '2017-05-01'
UserId = ''
EventName = ''
Version = ''
countries_code = ''

# function to extract users
def extract_users():
    data_users = {}

    response_js = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\All\\25_310517.json')

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
            if (country == 'UA') or (country == 'IL') or response_js['Sessions'][i]['Platform'] != 'Android':
                continue
            else:
                # find user id
                user_id = response_js['Sessions'][i]['UserId']
                if user_id not in data_users.keys():
                    data_users[user_id] = []
                if response_js['Sessions'][i]['AppVersion'] not in data_users[user_id]:
                    data_users[user_id].append(response_js['Sessions'][i]['AppVersion'])
    print(data_users)
    return data_users

def extract_gallery():
    data_gallery = {}

    response_js = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\May_17\\18_240517.json')

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
            if (country == 'UA') or (country == 'IL') or response_js['Sessions'][i]['Platform'] != 'Android':
                continue
            else:
                # find user id
                user_id = response_js['Sessions'][i]['UserId']
                if user_id not in data_gallery.keys():
                    data_gallery[user_id] = []
                if 'Events' in response_js['Sessions'][i]:
                    # enter the Events. The name of the list I want to access: response_js[l]['Sessions'], [i] indicates the index in the list and ['Events']
                    # the key of the dictionary in index i. the variable event is a list of dictionaries
                    event = response_js['Sessions'][i]['Events']
                    # number of events need to review
                    len_event = len(event)
                    # enter every event
                    for j in range(len_event):
                        if event[j]['Name'] == 'gallery_size' and 'Properties' in event[j] and 'gallery_size' in event[j]['Properties']:
                            gallery_size_value = event[j]['Properties']['gallery_size']
                            data_gallery[user_id].append(gallery_size_value)
    print(data_gallery)
    return data_gallery

extract_users()
#extract_gallery()
