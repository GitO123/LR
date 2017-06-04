# general report, relevant for version 0.9.0.1
# just US data, TM section only for collage created, starting version 0.9.0.1

import json
import statistics
import datetime as dt
from datetime import datetime, timedelta
import base_func

StartDate = datetime.strptime('2017-05-22', "%Y-%m-%d").date()
EndDate = datetime.strptime('2017-05-29', "%Y-%m-%d").date()
UserId = ''
EventName = ''
Version = '0.9.3.3'
Platform = 'Android'

with open('relevant_4_bycountry_report.txt', 'a') as resultsFile:

    # variables US
    sessions_us_1 = {}
    sessions_us = []
    dates = []
    # duration in timedelta
    sessions_duration_us = []
    # duration in ms (int) for calculations
    sessions_duration_ms_us = []
    # users that installed the app in current version
    new_users_us = []
    users_with_gallery_size_us = []
    gallery_size_us = []
    first_collage_users_us = []
    TM_clicks_us = []
    TM_clicks_true_us = []
    TM_creation_duration_users_us = []
    TM_creation_duration_users_us_drive = []
    TM_creation_duration_users_us_storage = []
    # duration in timedelta
    TM_collage_creation_duration_us = []
    # duration in ms (int) for calculations
    TM_collage_creation_duration_ms_us = []
    # duration in ms (int) for calculations, high values are filtered
    TM_collage_creation_duration_us_filt = []
    TM_collage_creation_duration_ms_us_filt = []
    # edit mode
    edit_mode_us = []
    skin_selected_us = []
    photo_chosen_edit_us = []
    photo_chosen_changed_us = []
    edit_approved_is_share = []
    collage_approved_us = []
    weekly_notif_click_us = []
    tbt_notif_click_us = []
    comeback_notif_click_us = []
    share_collage_open_us = []
    share_save_us = []
    share_fb_us = []
    share_inst_us = []
    share_twt_us = []
    share_msg_us = []
    share_more_us = []
    skip_share_us = []
    # users that clicked 'connect' button
    connect_button_us = []
    # users that clicked 'skip' button
    skip_us = []
    # users that clicked 'connect' button in the suggested page
    connection_suggest_us = []
    # connect to drive screen shown
    drive_screen_us = []
    # connected to drive
    drive_true_us = []
    # disconnected to drive
    drive_false_us = []
    # connect to drive via suggestions
    suggest_drive_active = []
    # disconnect from drive via suggestions
    suggest_drive_disabled = []
    # connect to drive via settings
    settings_connect_us = []
    # days for counting 1st week
    days_range = dt.timedelta(days=6)
    days_range_str = 6
    # 1st week new users
    first_week_new_users_us = []
    # countries to create the report for
    countries = []
    countries_code = 'Latm'

    response_js = base_func.extract_file('C:\\Users\\user\Documents\Projects\LifeReel\Data\\June_17\\1805_030617.json')

    # enter each session. each session is a list of dictionaries
    for i in range(len(response_js['Sessions'])):
        # remove internal users: Israel/ Ukraine
        if 'Location' in response_js['Sessions'][i]:
            country = response_js['Sessions'][i]['Location']['Country']
            if (country == 'UA') or (country == 'IL'):
                continue
            if response_js['Sessions'][i]['AppVersion'] != Version:
                continue
            if response_js['Sessions'][i]['Platform'] != Platform:
                continue
            else:
                countries = base_func.countries_set(countries_code)
                if country in countries:
                    user_id = response_js['Sessions'][i]['UserId']
                    # all legal sessions
                    sessions_us.append(user_id)
                    date = response_js['Sessions'][i]['StartTime']
                    dates.append(date)
                    # durations of legal sessions
                    duration_ms = response_js['Sessions'][i]['Duration']
                    duration = timedelta(milliseconds=duration_ms)
                    duration_float = duration.total_seconds()
                    sessions_duration_ms_us.append(duration_ms)
                    sessions_duration_us.append(duration)
                    if user_id not in sessions_us_1.keys():
                        sessions_us_1[user_id] = {}
                    sessions_us_1[user_id][date] = duration_float
                    if 'Events' in response_js['Sessions'][i]:
                        # enter the Events. The name of the list I want to access: response_js[l]['Sessions'], [i] indicates the index in the list and ['Events']
                        # the key of the dictionary in index i. the variable event is a list of dictionaries
                        event = response_js['Sessions'][i]['Events']
                        # number of events need to review
                        len_event = len(event)
                        # enter every event
                        for j in range(len_event):
                            # new users
                            if event[j]['Name'] == 'launch':
                                if 'Properties' in event[j]:
                                    if 'app_installed' in event[j]['Properties']:
                                        new_users_us.append(user_id)
                                        if (date.split("T")[0]) <= str(StartDate + days_range):
                                            first_week_new_users_us.append(user_id)
                            # find users with gallery size and the gallery size
                            if event[j]['Name'] == 'gallery_size':
                                if 'Properties' in event[j]:
                                    if 'gallery_size' in event[j]['Properties']:
                                        users_with_gallery_size_us.append(user_id)
                                        gallery_size_value = event[j]['Properties']['gallery_size']
                                        gallery_size_us.append(gallery_size_value)
                            # first collage users
                            if (event[j]['Name'] == 'first_collage_created') or (event[j]['Name'] == 'first_drive_collage_created'):
                                if 'Properties' in event[j]:
                                    if 'creation_duration' in event[j]['Properties']:
                                        first_collage_users_us.append(user_id)
                            # TM number of clicks and collage creation duration
                            if event[j]['Name'] == 'time_machine_clicked':
                                TM_clicks_us.append(user_id)
                                if 'Properties' in event[j]:
                                    if 'generating_new_collage' in event[j]['Properties']:
                                        if event[j]['Properties']['generating_new_collage'] == 'true':
                                            TM_clicks_true_us.append(user_id)
                            if event[j]['Name'] == 'collage_created':
                                if 'Properties' in event[j]:
                                    if event[j]['Properties']['time_machine'] == 'true':
                                        if 'creation_duration' in event[j]['Properties']:
                                            TM_creation_duration_users_us.append(user_id)
                                            if event[j]['Properties']['source'] == 'Storage':
                                                TM_creation_duration_users_us_storage.append(user_id)
                                            elif event[j]['Properties']['source'] == 'Google Drive':
                                                TM_creation_duration_users_us_drive.append(user_id)
                                            creation_duration_ms = int(event[j]['Properties']['creation_duration'])
                                            creation_duration_value = timedelta(milliseconds=creation_duration_ms)
                                            TM_collage_creation_duration_ms_us.append(creation_duration_ms)
                                            TM_collage_creation_duration_us.append(creation_duration_value)
                                            if creation_duration_ms < 1000000:
                                                TM_collage_creation_duration_ms_us_filt.append(creation_duration_ms)
                                                TM_collage_creation_duration_us_filt.append(creation_duration_value)
                            # edit data
                            if event[j]['Name'] == 'edit_click':
                                edit_mode_us.append(user_id)
                            if event[j]['Name'] == 'select_skin_click':
                                skin_selected_us.append(user_id)
                            if event[j]['Name'] == 'switch_photo_from_click':
                                photo_chosen_edit_us.append(user_id)
                            if event[j]['Name'] == 'switch_photo_to_click':
                                photo_chosen_changed_us.append(user_id)
                            if event[j]['Name'] == 'approve_collage':
                                collage_approved_us.append(user_id)
                            # notification clicks
                            if event[j]['Name'] == 'notification_clicked':
                                if 'Properties' in event[j]:
                                    if 'type' in event[j]['Properties']:
                                        if event[j]['Properties']['type'] == '0':
                                            weekly_notif_click_us.append(user_id)
                                        elif event[j]['Properties']['type'] == '1':
                                            tbt_notif_click_us.append(user_id)
                            if event[j]['Name'] == 'silent_notification_clicked':
                                if 'Properties' in event[j]:
                                    if 'type' in event[j]['Properties']:
                                        if event[j]['Properties']['type'] == '0':
                                            weekly_notif_click_us.append(user_id)
                                        elif event[j]['Properties']['type'] == '1':
                                            tbt_notif_click_us.append(user_id)
                            if event[j]['Name'] == 'comeback_notification_clicked':
                                comeback_notif_click_us.append(user_id)
                            # share types
                            if event[j]['Name'] == 'share_button_click':
                                share_collage_open_us.append(user_id)
                            if event[j]['Name'] == 'share_collage_open':
                                if 'Properties' in event[j]:
                                    if 'Share Target' in event[j]['Properties']:
                                        if event[j]['Properties']['Share Target'] == 'Save' or event[j]['Properties']['Share Target'] == 'Guardar' or event[j]['Properties']['Share Target'] == 'Salvar':
                                            share_save_us.append(user_id)
                                        elif event[j]['Properties']['Share Target'] == 'Facebook':
                                            share_fb_us.append(user_id)
                                        elif event[j]['Properties']['Share Target'] == 'Instagram':
                                            share_inst_us.append(user_id)
                                        elif event[j]['Properties']['Share Target'] == 'Twitter':
                                            share_twt_us.append(user_id)
                                        elif event[j]['Properties']['Share Target'] == 'Messages':
                                            share_msg_us.append(user_id)
                                        elif event[j]['Properties']['Share Target'] == 'More' or event[j]['Properties']['Share Target'] == 'Más' or event[j]['Properties']['Share Target'] == 'Mais':
                                            share_more_us.append(user_id)
                            if event[j]['Name'] == 'event_share_skip':
                                skip_share_us.append(user_id)
                            # connect to drive suggestion screen is shown
                            if event[j]['Name'] == 'cloud_connect_suggestion':
                                drive_screen_us.append(user_id)
                            if event[j]['Name'] == 'Google Drive State':
                                if 'Properties' in event[j]:
                                    if 'Connected' in event[j]['Properties']:
                                        if event[j]['Properties']['Connected'] == 'true':
                                            drive_true_us.append(user_id)
                                        elif event[j]['Properties']['Connected'] == 'false':
                                            drive_false_us.append(user_id)
                            # connect to drive via settings
                            if event[j]['Name'] == 'drive_active':
                                settings_connect_us.append(user_id)
                    if 'Screens' in response_js['Sessions'][i]:
                        screen = response_js['Sessions'][i]['Screens']
                        len_screen = len(screen)
                        for j in range(len_screen):
                            if len(screen[j]['Actions']) > 0:
                                for k in range(len(screen[j]['Actions'])):
                                    if 'Description' in screen[j]['Actions'][k]:
                                        # click on 'Share Collage' button
                                        if screen[j]['Actions'][k]['Description'] == 'SHARE' or screen[j]['Actions'][k]['Description'] == 'COMPARTIR' or screen[j]['Actions'][k]['Description'] == 'COMPARTILHAR':
                                            share_collage_open_us.append(user_id)
                                        # during onboarding drive connection preference
                                        if screen[j]['Actions'][k]['Description'] == 'Connect' or screen[j]['Actions'][k]['Description'] == 'Conectar' or screen[j]['Actions'][k]['Description'] == 'Conectar-se':
                                            connect_button_us.append(user_id)
                                        if screen[j]['Actions'][k]['Description'] == 'Skip':
                                            skip_us.append(user_id)
                                        # connect to drive via suggestion page
                                        if screen[j]['Actions'][k]['Description'] == 'Connect to google drive':
                                            connection_suggest_us.append(user_id)
                                        if screen[j]['Actions'][k]['Description'] == 'CONNECT GOOGLE PHOTOS' or screen[j]['Actions'][k]['Description'] == 'CONECTAR GOOGLE FOTOS' or screen[j]['Actions'][k]['Description'] == 'CONECTAR-SE AO GOOGLE PHOTOS':
                                            connection_suggest_us.append(user_id)
                                        if screen[j]['Actions'][k]['Description'] == 'CONNECT GOOGLE':
                                            connection_suggest_us.append(user_id)
        else:
            continue


    # general data
    # unique users
    unique_users_us = list(set(sessions_us))
    unique_new_users_us = list(set(new_users_us))
    unique_first_week_new_users_us = list(set(first_week_new_users_us))
    # avg and median session duration
    if sessions_duration_ms_us:
        avg_sessions_duration_us = statistics.mean(sessions_duration_ms_us)
        avg_sessions_duration_value_us = timedelta(milliseconds=avg_sessions_duration_us)
        #avg_sessions_duration_value_print = str(avg_sessions_duration_value).split(".")[0]
        median_sessions_duration_us = statistics.median(sessions_duration_ms_us)
        median_sessions_duration_value_us = timedelta(milliseconds=median_sessions_duration_us)
        #median_sessions_duration_value_print = str(median_sessions_duration_value).split(".")[0]
    #test
    if sessions_us_1:
        # number of sessions per user and total time spent in app
        total_time = 0
        for user_id in sessions_us_1.keys():
            if user_id in unique_new_users_us:
                for date in sessions_us_1[user_id]:
                    if (date.split("T")[0]) <= str(StartDate + days_range):
                        total_time += (sessions_us_1[user_id][date])
        time_in_app_decimal_sec = float(total_time)/ len(unique_first_week_new_users_us)
        m, s = divmod(time_in_app_decimal_sec, 60)
        h, m = divmod(m, 60)

    # avg and median gallery size
    if gallery_size_us:
        avg_gallery_size_us = "{:.2f}".format(statistics.mean(gallery_size_us))
        median_gallery_size_us = "{:.2f}".format(statistics.median(gallery_size_us))
    # drive data
    # users that clicked 'connect'
    connect_users_us = connect_button_us + connection_suggest_us
    connect_users_us_unique = list(set(connect_users_us))
    # unique users that connected via suggestions
    settings_connect_us_unique = list(set(settings_connect_us))
    connect_settings_not_suggest = set(settings_connect_us_unique) - set(connect_users_us_unique)
    # unique users that connected
    drive_true_unique_us = list(set(drive_true_us))
    # unique users that disconnected
    drive_false_unique_us = list(set(drive_false_us))
    # unique users that skipped
    skip_us_unique = list(set(skip_us))
    # users that clicked 'connect' and 'skip'
    skip_and_connect_us = list(set(connect_users_us_unique).intersection(skip_us_unique))
    # first collage users
    unique_first_collage_us = list(set(first_collage_users_us))
    # TM data
    # users that clicked the TM button
    TM_clicks_users_us = list(set(TM_clicks_us))
    if TM_collage_creation_duration_ms_us:
        # avg and median TM collage creation duration
        avg_TM_collage_creation_duration_us = statistics.mean(TM_collage_creation_duration_ms_us)
        avg_TM_collage_creation_duration_value_us = timedelta(milliseconds=avg_TM_collage_creation_duration_us)
        #avg_TM_collage_creation_duration_value_print = str(avg_TM_collage_creation_duration_value).split(".")[0]
        median_TM_collage_creation_duration_us = statistics.median(TM_collage_creation_duration_ms_us)
        median_TM_collage_creation_duration_value_us = timedelta(milliseconds=median_TM_collage_creation_duration_us)
        #print(TM_collage_creation_duration_ms_us)
        # creation duration filtered values:
        # avg and median TM collage creation duration
        avg_TM_collage_creation_duration_us_filt = statistics.mean(TM_collage_creation_duration_ms_us_filt)
        avg_TM_collage_creation_duration_value_us_filt = timedelta(milliseconds=avg_TM_collage_creation_duration_us_filt)
        # avg_TM_collage_creation_duration_value_print = str(avg_TM_collage_creation_duration_value).split(".")[0]
        median_TM_collage_creation_duration_us_filt = statistics.median(TM_collage_creation_duration_ms_us_filt)
        median_TM_collage_creation_duration_value_us_filt = timedelta(milliseconds=median_TM_collage_creation_duration_us_filt)
        #print(TM_collage_creation_duration_ms_us_filt)
        #median_TM_collage_creation_duration_value_print = str(median_TM_collage_creation_duration_value).split(".")[0]
    if TM_clicks_us:
        TM_success_rate_us = len(TM_creation_duration_users_us) / len(TM_clicks_us)
    # notifications data
    weekly_notif_click_us_unique = list(set(weekly_notif_click_us))
    tbt_notif_click_us_unique = list(set(tbt_notif_click_us))
    comeback_notif_click_us_unique = list(set(comeback_notif_click_us))
    # edit data
    unique_edit_mode_us = list(set(edit_mode_us))
    unique_skin_selected_us = list(set(skin_selected_us))
    unique_photo_chosen_edit_us = list(set(photo_chosen_edit_us))
    unique_photo_chosen_changed_us = list(set(photo_chosen_changed_us))
    unique_collage_approved_us = list(set(collage_approved_us))
    # Share data
    share_collage_open_us_unique = list(set(share_collage_open_us))
    share_button_collage_approved_unique = list(set(collage_approved_us + share_collage_open_us))
    share_platform_unique = list(set(share_fb_us + share_inst_us + share_twt_us + share_msg_us + share_more_us))
    share_save_us_unique = list(set(share_save_us))
    share_fb_us_unique = list(set(share_fb_us))
    share_inst_us_unique = list(set(share_inst_us))
    share_twt_us_unique = list(set(share_twt_us))
    share_msg_us_unique = list(set(share_msg_us))
    share_more_us_unique = list(set(share_more_us))
    skip_share_us_unique = list(set(skip_share_us))
    # edited and shared
    all_shares = list(set(share_fb_us_unique + share_inst_us_unique + share_twt_us_unique + share_msg_us_unique + share_more_us_unique))
    edit_approved_is_share = list(set(unique_collage_approved_us) & set(all_shares))

    # open a file to write the data
    resultsFile.write("countries: ")
    resultsFile.write(base_func.return_countries(countries_code))
    resultsFile.write("\n")
    base_func.print_time(resultsFile, StartDate, EndDate, Version)
    # print data US
    # print general data
    base_func.print_numeric_data(resultsFile,"unique_users_us", unique_users_us)
    base_func.print_numeric_data(resultsFile,"unique_new_users_us", unique_new_users_us)
    if sessions_duration_ms_us:
        base_func.print_values(resultsFile,"avg_sessions_duration_us", avg_sessions_duration_value_us)
        base_func.print_values(resultsFile,"median_sessions_duration_us", median_sessions_duration_value_us)
    resultsFile.write("total time in app during 1st week %d:%02d:%02d" % (h, m, s))
    resultsFile.write("\n")
    base_func.print_values(resultsFile,"avg_gallery_size_us", avg_gallery_size_us)
    base_func.print_values(resultsFile,"median_gallery_size_us", median_gallery_size_us)
    # print drive data
    base_func.print_numeric_data(resultsFile,"connect_users_us_unique", connect_users_us_unique)
    base_func.print_numeric_data(resultsFile,"connect_settings_not_suggest", connect_settings_not_suggest)
    base_func.print_numeric_data(resultsFile,"drive_true_unique_us", drive_true_unique_us)
    ##don't print: print_numeric_data("skip_us_unique", skip_us_unique)
    base_func.print_numeric_data(resultsFile,"drive_false_unique_us", drive_false_unique_us)
    ##don't print: print_numeric_data("skip_and_connect_us", skip_and_connect_us)
    # print 1st collage
    base_func.print_numeric_data(resultsFile,"unique_first_collage_us", unique_first_collage_us)
    # print TM data
    base_func.print_numeric_data(resultsFile,"TM_clicks_us", TM_clicks_us)
    base_func.print_numeric_data(resultsFile,"TM_clicks_users_us", TM_clicks_users_us)
    base_func.print_values(resultsFile,"TM_success_rate_us", TM_success_rate_us)
    base_func.print_numeric_data(resultsFile,"TM_creation_duration_users_us_storage", TM_creation_duration_users_us_storage)
    base_func.print_numeric_data(resultsFile,"TM_creation_duration_users_us_drive", TM_creation_duration_users_us_drive)
    if TM_collage_creation_duration_ms_us:
        base_func.print_values(resultsFile,"avg_TM_collage_creation_duration_us", avg_TM_collage_creation_duration_value_us)
        base_func.print_values(resultsFile,"median_TM_collage_creation_duration_us", median_TM_collage_creation_duration_value_us)
        base_func.print_values(resultsFile, "avg_TM_collage_creation_duration_us_filt", avg_TM_collage_creation_duration_value_us_filt)
        base_func.print_values(resultsFile, "median_TM_collage_creation_duration_us_filt", median_TM_collage_creation_duration_value_us_filt)
    # print notifications
    base_func.print_numeric_data(resultsFile,"weekly_notif_click_us_unique", weekly_notif_click_us_unique)
    base_func.print_numeric_data(resultsFile,"tbt_notif_click_us_unique", tbt_notif_click_us_unique)
    base_func.print_numeric_data(resultsFile,"comeback_notif_click_us_unique", comeback_notif_click_us_unique)
    # print edit data
    base_func.print_numeric_data(resultsFile,"unique_edit_mode_us", unique_edit_mode_us)
    base_func.print_numeric_data(resultsFile,"unique_skin_selected_us", unique_skin_selected_us)
    base_func.print_numeric_data(resultsFile,"unique_photo_chosen_edit_us", unique_photo_chosen_edit_us)
    base_func.print_numeric_data(resultsFile,"unique_photo_chosen_changed_us", unique_photo_chosen_changed_us)
    base_func.print_numeric_data(resultsFile,"unique_collage_approved_us", unique_collage_approved_us)
    base_func.print_numeric_data(resultsFile,"edit_approved_is_share", edit_approved_is_share)
    base_func.print_numeric_data(resultsFile,"skip_share_us_unique", skip_share_us_unique)
    # print share
    base_func.print_numeric_data(resultsFile,"share_collage_open_us_unique", share_collage_open_us_unique)
    base_func.print_numeric_data(resultsFile,"share_button_collage_approved_unique", share_button_collage_approved_unique)
    base_func.print_numeric_data(resultsFile,"share_platform_unique", share_platform_unique)
    base_func.print_numeric_data(resultsFile,"share_fb_us_unique", share_fb_us_unique)
    base_func.print_numeric_data(resultsFile,"share_inst_us_unique", share_inst_us_unique)
    base_func.print_numeric_data(resultsFile,"share_twt_us_unique", share_twt_us_unique)
    base_func.print_numeric_data(resultsFile,"share_msg_us_unique", share_msg_us_unique)
    base_func.print_numeric_data(resultsFile,"share_save_us_unique", share_save_us_unique)
    base_func.print_numeric_data(resultsFile,"share_more_us_unique", share_more_us_unique)
    resultsFile.write("\n")
    resultsFile.write("\n")