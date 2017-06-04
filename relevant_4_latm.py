# general report, relevant for version 0.9.0.1
# just US data, TM section only for collage created, starting version 0.9.0.1

import json
import statistics
import datetime as dt
from datetime import datetime, timedelta
import base_func

StartDate = datetime.strptime('2017-04-28', "%Y-%m-%d").date()
EndDate = datetime.strptime('2017-04-28', "%Y-%m-%d").date()
UserId = ''
EventName = ''
Version = '0.9.1.3'

with open('relevant_4_bycountry_report_latm.txt', 'a') as resultsFile:
    pages_num = (base_func.calc_pages(StartDate, EndDate, UserId, EventName, Version)) + 1

    # variables US
    sessions_1 = {}
    sessions = []
    dates = []
    # duration in timedelta
    sessions_duration = []
    # duration in ms (int) for calculations
    sessions_duration_ms = []
    # users that installed the app in current version
    newers = []
    users_with_gallery_size = []
    gallery_size = []
    first_collageers = []
    TM_clicks = []
    TM_clicks_true = []
    TM_creation_durationers =[]
    TM_creation_durationers_drive = []
    TM_creation_durationers_storage = []
    # duration in timedelta
    TM_collage_creation_duration = []
    # duration in ms (int) for calculations
    TM_collage_creation_duration_ms = []
    # edit mode
    edit_mode = []
    skin_selected = []
    photo_chosen_edit = []
    photo_chosen_changed = []
    edit_approved_is_share = []
    collage_approved = []
    weekly_notif_click = []
    tbt_notif_click = []
    comeback_notif_click = []
    share_collage_open = []
    share_save = []
    share_fb = []
    share_inst = []
    share_twt = []
    share_msg = []
    share_more = []
    skip_share = []
    # users that clicked 'connect' button
    connect_button = []
    # users that clicked 'skip' button
    skip = []
    # users that clicked 'connect' button in the suggested page
    connection_suggest = []
    # connect to drive screen shown
    drive_screen = []
    # connected to drive
    drive_true = []
    # disconnected to drive
    drive_false = []
    # connect to drive via suggestions
    suggest_drive_active = []
    # disconnect from drive via suggestions
    suggest_drive_disabled = []
    # connect to drive via settings
    settings_connect = []
    # days for counting 1st week
    days_range = dt.timedelta(days=6)
    days_range_str = 6
    # 1st week new users
    first_week_newers = []
    #countries to create the report for
    countries = []

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
                    #if country in ['AR', 'BO', 'BR', 'CL', 'CO', 'EC', 'JM', 'MX', 'PA', 'PE', 'PR', 'ES', 'UY']:
                    countries = base_func.countries_set('Latm')
                    if country in countries:
                        #'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Jamaica', 'Mexico', 'Panama', 'Peru', 'Puerto Rico', 'Spain', 'Uruguay'
                        user_id = response_js[a]['Sessions'][i]['UserId']
                        # all legal sessions
                        sessions.append(user_id)
                        date = response_js[a]['Sessions'][i]['StartTime']
                        dates.append(date)
                        # durations of legal sessions
                        duration_ms = response_js[a]['Sessions'][i]['Duration']
                        duration = timedelta(milliseconds=duration_ms)
                        duration_float = duration.total_seconds()
                        sessions_duration_ms.append(duration_ms)
                        sessions_duration.append(duration)
                        if user_id not in sessions_1.keys():
                            sessions_1[user_id] = {}
                        sessions_1[user_id][date] = duration_float
                        if 'Events' in response_js[a]['Sessions'][i]:
                            # enter the Events. The name of the list I want to access: response_js[l]['Sessions'], [i] indicates the index in the list and ['Events']
                            # the key of the dictionary in index i. the variable event is a list of dictionaries
                            event = response_js[a]['Sessions'][i]['Events']
                            # number of events need to review
                            len_event = len(event)
                            # enter every event
                            for j in range(len_event):
                                # new users
                                if event[j]['Name'] == 'launch':
                                    if 'Properties' in event[j]:
                                        if 'app_installed' in event[j]['Properties']:
                                            newers.append(user_id)
                                            if (date.split("T")[0]) <= str(StartDate + days_range):
                                                first_week_newers.append(user_id)
                                # find users with gallery size and the gallery size
                                if event[j]['Name'] == 'gallery_size':
                                    if 'Properties' in event[j]:
                                        if 'gallery_size' in event[j]['Properties']:
                                            users_with_gallery_size.append(user_id)
                                            gallery_size_value = event[j]['Properties']['gallery_size']
                                            gallery_size.append(gallery_size_value)
                                # first collage users
                                if event[j]['Name'] == 'first_collage_created':
                                    if 'Properties' in event[j]:
                                        if 'creation_duration' in event[j]['Properties']:
                                            first_collageers.append(user_id)
                                # TM number of clicks and collage creation duration
                                if event[j]['Name'] == 'time_machine_clicked':
                                    TM_clicks.append(user_id)
                                    if 'Properties' in event[j]:
                                        if 'generating_new_collage' in event[j]['Properties']:
                                            if event[j]['Properties']['generating_new_collage'] == 'true':
                                                TM_clicks_true.append(user_id)
                                if event[j]['Name'] == 'collage_created':
                                    if 'Properties' in event[j]:
                                        if event[j]['Properties']['time_machine'] == 'true':
                                            if 'creation_duration' in event[j]['Properties']:
                                                TM_creation_durationers.append(user_id)
                                                if event[j]['Properties']['source'] == 'Storage':
                                                    TM_creation_durationers_storage.append(user_id)
                                                elif event[j]['Properties']['source'] == 'Google Drive':
                                                    TM_creation_durationers_drive.append(user_id)
                                                creation_duration_ms = int(event[j]['Properties']['creation_duration'])
                                                creation_duration_value = timedelta(milliseconds=creation_duration_ms)
                                                TM_collage_creation_duration_ms.append(creation_duration_ms)
                                                TM_collage_creation_duration.append(creation_duration_value)
                                # edit data
                                if event[j]['Name'] == 'edit_click':
                                    edit_mode.append(user_id)
                                if event[j]['Name'] == 'select_skin_click':
                                    skin_selected.append(user_id)
                                if event[j]['Name'] == 'switch_photo_from_click':
                                    photo_chosen_edit.append(user_id)
                                if event[j]['Name'] == 'switch_photo_to_click':
                                    photo_chosen_changed.append(user_id)
                                if event[j]['Name'] == 'approve_collage':
                                    collage_approved.append(user_id)
                                # notification clicks
                                if event[j]['Name'] == 'notification_clicked':
                                    if 'Properties' in event[j]:
                                        if 'type' in event[j]['Properties']:
                                            if event[j]['Properties']['type'] == '0':
                                                weekly_notif_click.append(user_id)
                                            elif event[j]['Properties']['type'] == '1':
                                                tbt_notif_click.append(user_id)
                                if event[j]['Name'] == 'silent_notification_clicked':
                                    if 'Properties' in event[j]:
                                        if 'type' in event[j]['Properties']:
                                            if event[j]['Properties']['type'] == '0':
                                                weekly_notif_click.append(user_id)
                                            elif event[j]['Properties']['type'] == '1':
                                                tbt_notif_click.append(user_id)
                                if event[j]['Name'] == 'comeback_notification_clicked':
                                    comeback_notif_click.append(user_id)
                                # share types
                                if event[j]['Name'] == 'share_button_click':
                                    share_collage_open.append(user_id)
                                if event[j]['Name'] == 'share_collage_open':
                                    if 'Properties' in event[j]:
                                        if 'Share Target' in event[j]['Properties']:
                                            if event[j]['Properties']['Share Target'] == 'Save':
                                                share_save.append(user_id)
                                            elif event[j]['Properties']['Share Target'] == 'Facebook':
                                                share_fb.append(user_id)
                                            elif event[j]['Properties']['Share Target'] == 'Instagram':
                                                share_inst.append(user_id)
                                            elif event[j]['Properties']['Share Target'] == 'Twitter':
                                                share_twt.append(user_id)
                                            elif event[j]['Properties']['Share Target'] == 'Messages':
                                                share_msg.append(user_id)
                                            elif event[j]['Properties']['Share Target'] == 'More':
                                                share_more.append(user_id)
                                if event[j]['Name'] == 'event_share_skip':
                                    skip_share.append(user_id)
                                # connect to drive suggestion screen is shown
                                if event[j]['Name'] == 'cloud_connect_suggestion':
                                    drive_screen.append(user_id)
                                if event[j]['Name'] == 'Google Drive State':
                                    if 'Properties' in event[j]:
                                        if 'Connected' in event[j]['Properties']:
                                            if event[j]['Properties']['Connected'] == 'true':
                                                drive_true.append(user_id)
                                            elif event[j]['Properties']['Connected'] == 'false':
                                                drive_false.append(user_id)
                                # connect to drive via settings
                                if event[j]['Name'] == 'drive_active':
                                    settings_connect.append(user_id)
                        if 'Screens' in response_js[a]['Sessions'][i]:
                            screen = response_js[a]['Sessions'][i]['Screens']
                            len_screen = len(screen)
                            for j in range(len_screen):
                                if len(screen[j]['Actions']) > 0:
                                    for k in range(len(screen[j]['Actions'])):
                                        if 'Description' in screen[j]['Actions'][k]:
                                            # click on 'Share Collage' button
                                            if screen[j]['Actions'][k]['Description'] == 'SHARE':
                                                share_collage_open.append(user_id)
                                            # during onboarding drive connection preference
                                            if screen[j]['Actions'][k]['Description'] == 'Connect':
                                                connect_button.append(user_id)
                                            if screen[j]['Actions'][k]['Description'] == 'Skip':
                                                skip.append(user_id)
                                            # connect to drive via suggestion page
                                            if screen[j]['Actions'][k]['Description'] == 'Connect to google drive':
                                                connection_suggest.append(user_id)
                                            if screen[j]['Actions'][k]['Description'] == 'CONNECT GOOGLE PHOTOS':
                                                connection_suggest.append(user_id)
                                            if screen[j]['Actions'][k]['Description'] == 'CONNECT GOOGLE':
                                                connection_suggest.append(user_id)

            else:
                continue

    # US data
    # general data
    # unique users
    uniqueers = list(set(sessions))
    unique_newers = list(set(newers))
    unique_first_week_newers = list(set(first_week_newers))
    # avg and median session duration
    if sessions_duration_ms:
        avg_sessions_duration = statistics.mean(sessions_duration_ms)
        avg_sessions_duration_value = timedelta(milliseconds=avg_sessions_duration)
        #avg_sessions_duration_value_print = str(avg_sessions_duration_value).split(".")[0]
        median_sessions_duration = statistics.median(sessions_duration_ms)
        median_sessions_duration_value = timedelta(milliseconds=median_sessions_duration)
        #median_sessions_duration_value_print = str(median_sessions_duration_value).split(".")[0]
    #test
    if sessions_1:
        # number of sessions per user and total time spent in app
        total_time = 0
        for user_id in sessions_1.keys():
            if user_id in unique_newers:
                for date in sessions_1[user_id]:
                    if (date.split("T")[0]) <= str(StartDate + days_range):
                        total_time += (sessions_1[user_id][date])
        time_in_app_decimal_sec = float(total_time)/ len(unique_first_week_newers)
        m, s = divmod(time_in_app_decimal_sec, 60)
        h, m = divmod(m, 60)

    # avg and median gallery size
    if gallery_size:
        avg_gallery_size = "{:.2f}".format(statistics.mean(gallery_size))
        median_gallery_size = "{:.2f}".format(statistics.median(gallery_size))
    # drive data
    # users that clicked 'connect'
    connecters = connect_button + connection_suggest
    connecters_unique = list(set(connecters))
    # unique users that connected via suggestions
    settings_connect_unique = list(set(settings_connect))
    connect_settings_not_suggest = set(settings_connect_unique) - set(connecters_unique)
    # unique users that connected
    drive_true_unique = list(set(drive_true))
    # unique users that disconnected
    drive_false_unique = list(set(drive_false))
    # unique users that skipped
    skip_unique = list(set(skip))
    # users that clicked 'connect' and 'skip'
    skip_and_connect = list(set(connecters_unique).intersection(skip_unique))
    # first collage users
    unique_first_collage = list(set(first_collageers))
    # TM data
    # users that clicked the TM button
    TM_clicksers = list(set(TM_clicks))
    if TM_collage_creation_duration_ms:
        # avg and median TM collage creation duration
        avg_TM_collage_creation_duration = statistics.mean(TM_collage_creation_duration_ms)
        avg_TM_collage_creation_duration_value = timedelta(milliseconds=avg_TM_collage_creation_duration)
        #avg_TM_collage_creation_duration_value_print = str(avg_TM_collage_creation_duration_value).split(".")[0]
        median_TM_collage_creation_duration = statistics.median(TM_collage_creation_duration_ms)
        median_TM_collage_creation_duration_value = timedelta(milliseconds=median_TM_collage_creation_duration)
        #median_TM_collage_creation_duration_value_print = str(median_TM_collage_creation_duration_value).split(".")[0]
    if TM_clicks:
        TM_success_rate = len(TM_creation_durationers) / len(TM_clicks)
    # notifications data
    weekly_notif_click_unique = list(set(weekly_notif_click))
    tbt_notif_click_unique = list(set(tbt_notif_click))
    comeback_notif_click_unique = list(set(comeback_notif_click))
    # edit data
    unique_edit_mode = list(set(edit_mode))
    unique_skin_selected = list(set(skin_selected))
    unique_photo_chosen_edit = list(set(photo_chosen_edit))
    unique_photo_chosen_changed = list(set(photo_chosen_changed))
    unique_collage_approved = list(set(collage_approved))
    # Share data
    share_collage_open_unique = list(set(share_collage_open))
    share_button_collage_approved_unique = list(set(collage_approved + share_collage_open))
    share_platform_unique = list(set(share_fb + share_inst + share_twt + share_msg + share_more))
    share_save_unique = list(set(share_save))
    share_fb_unique = list(set(share_fb))
    share_inst_unique = list(set(share_inst))
    share_twt_unique = list(set(share_twt))
    share_msg_unique = list(set(share_msg))
    share_more_unique = list(set(share_more))
    skip_share_unique = list(set(skip_share))
    # edited and shared
    all_shares = list(set(share_fb_unique + share_inst_unique + share_twt_unique + share_msg_unique + share_more_unique))
    edit_approved_is_share = list(set(unique_collage_approved) & set(all_shares))

    # open a file to write the data
    base_func.print_time(resultsFile, StartDate, EndDate, Version)
    # print data US
    # print general data
    base_func.print_numeric_data(resultsFile,"uniqueers", uniqueers)
    base_func.print_numeric_data(resultsFile,"unique_newers", unique_newers)
    if sessions_duration_ms:
        base_func.print_values(resultsFile,"avg_sessions_duration", avg_sessions_duration_value)
        base_func.print_values(resultsFile,"median_sessions_duration", median_sessions_duration_value)
    resultsFile.write("total time in app during 1st week %d:%02d:%02d" % (h, m, s))
    resultsFile.write("\n")
    base_func.print_values(resultsFile,"avg_gallery_size", avg_gallery_size)
    base_func.print_values(resultsFile,"median_gallery_size", median_gallery_size)
    # print drive data
    base_func.print_numeric_data(resultsFile,"connecters_unique", connecters_unique)
    base_func.print_numeric_data(resultsFile,"connect_settings_not_suggest", connect_settings_not_suggest)
    base_func.print_numeric_data(resultsFile,"drive_true_unique", drive_true_unique)
    ##don't print: print_numeric_data("skip_unique", skip_unique)
    base_func.print_numeric_data(resultsFile,"drive_false_unique", drive_false_unique)
    ##don't print: print_numeric_data("skip_and_connect", skip_and_connect)
    # print 1st collage
    base_func.print_numeric_data(resultsFile,"unique_first_collage", unique_first_collage)
    # print TM data
    base_func.print_numeric_data(resultsFile,"TM_clicks", TM_clicks)
    base_func.print_numeric_data(resultsFile,"TM_clicksers", TM_clicksers)
    base_func.print_values(resultsFile,"TM_success_rate", TM_success_rate)
    base_func.print_numeric_data(resultsFile,"TM_creation_durationers_storage", TM_creation_durationers_storage)
    base_func.print_numeric_data(resultsFile,"TM_creation_durationers_drive", TM_creation_durationers_drive)
    if TM_collage_creation_duration_ms:
        base_func.print_values(resultsFile,"avg_TM_collage_creation_duration", avg_TM_collage_creation_duration_value)
        base_func.print_values(resultsFile,"median_TM_collage_creation_duration", median_TM_collage_creation_duration_value)
    # print notifications
    base_func.print_numeric_data(resultsFile,"weekly_notif_click_unique", weekly_notif_click_unique)
    base_func.print_numeric_data(resultsFile,"tbt_notif_click_unique", tbt_notif_click_unique)
    base_func.print_numeric_data(resultsFile,"comeback_notif_click_unique", comeback_notif_click_unique)
    # print edit data
    base_func.print_numeric_data(resultsFile,"unique_edit_mode", unique_edit_mode)
    base_func.print_numeric_data(resultsFile,"unique_skin_selected", unique_skin_selected)
    base_func.print_numeric_data(resultsFile,"unique_photo_chosen_edit", unique_photo_chosen_edit)
    base_func.print_numeric_data(resultsFile,"unique_photo_chosen_changed", unique_photo_chosen_changed)
    base_func.print_numeric_data(resultsFile,"unique_collage_approved", unique_collage_approved)
    base_func.print_numeric_data(resultsFile,"edit_approved_is_share", edit_approved_is_share)
    base_func.print_numeric_data(resultsFile,"skip_share_unique", skip_share_unique)
    # print share
    base_func.print_numeric_data(resultsFile,"share_collage_open_unique", share_collage_open_unique)
    base_func.print_numeric_data(resultsFile,"share_button_collage_approved_unique", share_button_collage_approved_unique)
    base_func.print_numeric_data(resultsFile,"share_platform_unique", share_platform_unique)
    base_func.print_numeric_data(resultsFile,"share_fb_unique", share_fb_unique)
    base_func.print_numeric_data(resultsFile,"share_inst_unique", share_inst_unique)
    base_func.print_numeric_data(resultsFile,"share_twt_unique", share_twt_unique)
    base_func.print_numeric_data(resultsFile,"share_msg_unique", share_msg_unique)
    base_func.print_numeric_data(resultsFile,"share_save_unique", share_save_unique)
    base_func.print_numeric_data(resultsFile,"share_more_unique", share_more_unique)
    resultsFile.write("\n")
    resultsFile.write("\n")