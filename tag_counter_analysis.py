# tag_counter analysis

import base_func

StartDate = '2017-05-05'
EndDate = '2017-05-08'
UserId = ''
EventName = ''
Version = ''
countries = []
countries_code = 'US'

# function to count number of events and number of non empty events
def count_empty():
    data = {'event_count', 'unempty_event_count'}
    data = dict.fromkeys(data, 0)

    data_from_func = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\\01_140517.json')
    response_js = data_from_func

    # empty counters and all counters
    for i in range(len(response_js['Sessions'])):
        # remove internal users: Israel/ Ukraine
        if 'Location' in response_js['Sessions'][i]:
            loc = response_js['Sessions'][i]['Location']
            country = loc['Country']
            if (country == 'UA') or (country == 'IL'):
                continue
            else:
                countries = base_func.countries_set(countries_code)
                if country in countries:
                    if 'Events' in response_js['Sessions'][i]:
                        event = response_js['Sessions'][i]['Events']
                        # number of events need to review
                        len_event = len(response_js['Sessions'][i]['Events'])
                        # enter every event
                        for j in range(len_event):
                            if event[j]['Name'] == 'tag_counter':
                                data['event_count'] += 1
                                if 'Properties' in event[j]:
                                    data['unempty_event_count'] += 1
    print(data)
    return data

# function to find all tags
def count_tags():
    data = {}

    data_from_func = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\\01_140517.json')
    response_js = data_from_func

    # empty counters and all counters
    for i in range(len(response_js['Sessions'])):
        # remove internal users: Israel/ Ukraine
        if 'Location' in response_js['Sessions'][i]:
            loc = response_js['Sessions'][i]['Location']
            country = loc['Country']
            if (country == 'UA') or (country == 'IL'):
                continue
            else:
                countries = base_func.countries_set(countries_code)
                if country in countries:
                    if 'Events' in response_js['Sessions'][i]:
                        event = response_js['Sessions'][i]['Events']
                        # number of events need to review
                        len_event = len(response_js['Sessions'][i]['Events'])
                        # enter every event
                        for j in range(len_event):
                            if (event[j]['Name'] == 'tag_counter') and ('Properties' in event[j]):
                                for key in event[j]['Properties']:
                                    if key not in data.keys():
                                        data[key] = 0
                                    data[key] += 1
    print(data)
    return data


# write results to file
def write_results(share_data):
    with open('tag_counter.txt', 'a') as datafile:
        # print date and time
        base_func.print_time(datafile, StartDate, EndDate, Version)
        # print countries
        base_func.print_countries(datafile, countries_code)
        # print data
        base_func.print_dict(datafile, share_data)


write_results(count_empty())
write_results(count_tags())