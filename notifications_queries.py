import mysql.connector
# tutorial http://www.mysqltutorial.org/getting-started-mysql-python-connector/

def connect(host, database, user, password):
    conn = mysql.connector.connect(host=host, database=database, user=user, password=password)
    return conn

'''def event_notif_token():
    event_notif_token_query = ('SELECT COUNT(token)'
                               ' FROM devices'
                               ' WHERE device_id NOT IN (SELECT device_id FROM devices WHERE timezone = 3)'
                               ' AND push_server_enable = 1'
                               ' AND created_at <= %s')
    return event_notif_token_query'''

def event_notif():
    event_notif_query = ('SELECT COUNT(DISTINCT user_id)'
                         ' FROM `analytics`'
                         ' WHERE event_type = %s'
                         ' AND TYPE = %s'
                         ' AND DATE BETWEEN %s AND %s'
                         ' AND device_id NOT IN (SELECT device_id FROM devices WHERE timezone = 3)')
    return event_notif_query

def comeback_notif():
    comeback_notif_query = ('SELECT COUNT(DISTINCT user_id)'
                            ' FROM `analytics`'
                            ' WHERE event_type = %s'
                            ' AND DATE BETWEEN %s AND %s'
                            ' AND device_id NOT IN (SELECT device_id FROM devices WHERE timezone = 3)')
    return comeback_notif_query

def excute_daily_query(connection, event_notif, comeback_notif):
    cursor = connection.cursor()
    data = {'legit_tokens', 'event_received', 'event_displayed', 'event_clicked', 'comeback_received', 'comeback_displayed', 'comeback_clicked'}
    data = dict.fromkeys(data, 0)
    cursor.execute(event_notif, ('silent_notification_received', 'event', '2017-05-31 04:00:00', '2017-06-01 05:00:00'))
    data['event_received'] = cursor.fetchone()[0]
    cursor.execute(event_notif, ('silent_notification_displayed', 'event', '2017-05-31 04:00:00', '2017-06-01 05:00:00'))
    data['event_displayed'] = cursor.fetchone()[0]
    cursor.execute(event_notif, ('silent_notification_clicked', 'event', '2017-05-31 04:00:00', '2017-06-01 05:00:00'))
    data['event_clicked'] = cursor.fetchone()[0]
    cursor.execute(comeback_notif, ('comeback_notification_received', '2017-05-31 00:00:00', '2017-05-31 23:59:59'))
    data['comeback_received'] = cursor.fetchone()[0]
    cursor.execute(comeback_notif, ('comeback_notification_displayed', '2017-05-31 00:00:00', '2017-05-31 23:59:59'))
    data['comeback_displayed'] = cursor.fetchone()[0]
    cursor.execute(comeback_notif, ('comeback_notification_clicked', '2017-05-31 00:00:00', '2017-05-31 23:59:59'))
    data['comeback_clicked'] = cursor.fetchone()[0]
    print(data)


def excute_monday(connection, event_notif):
    cursor = connection.cursor()
    data = {'legit_tokens', 'event_received', 'event_displayed', 'event_clicked'}
    data = dict.fromkeys(data, 0)
    cursor.execute(event_notif, ('silent_notification_received', 'weekly', '2017-05-28 00:00:00', '2017-05-29 23:59:59'))
    data['event_received'] = cursor.fetchone()[0]
    cursor.execute(event_notif, ('silent_notification_displayed', 'weekly', '2017-05-28 00:00:00', '2017-05-29 23:59:59'))
    data['event_displayed'] = cursor.fetchone()[0]
    cursor.execute(event_notif, ('silent_notification_clicked', 'weekly', '2017-05-28 00:00:00', '2017-05-29 23:59:59'))
    data['event_clicked'] = cursor.fetchone()[0]
    print(data)


def excute_tursday(connection, event_notif):
    cursor = connection.cursor()
    data = {'legit_tokens', 'event_received', 'event_displayed', 'event_clicked'}
    data = dict.fromkeys(data, 0)
    cursor.execute(event_notif, ('silent_notification_received', 'historic', '2017-05-24 00:00:00', '2017-05-25 23:59:59'))
    data['event_received'] = cursor.fetchone()[0]
    cursor.execute(event_notif, ('silent_notification_displayed', 'historic', '2017-05-24 00:00:00', '2017-05-25 23:59:59'))
    data['event_displayed'] = cursor.fetchone()[0]
    cursor.execute(event_notif, ('silent_notification_clicked', 'historic', '2017-05-24 00:00:00', '2017-05-25 23:59:59'))
    data['event_clicked'] = cursor.fetchone()[0]
    print(data)



#excute_monday(connect('weekly-sum.ctehpvgbi3sb.us-east-1.rds.amazonaws.com', 'lifereel_production', 'cortica', 'oRAQpmiHS6RC'), event_notif())
excute_tursday(connect('weekly-sum.ctehpvgbi3sb.us-east-1.rds.amazonaws.com', 'lifereel_production', 'cortica', 'oRAQpmiHS6RC'), event_notif())
#excute_daily_query(connect('weekly-sum.ctehpvgbi3sb.us-east-1.rds.amazonaws.com', 'lifereel_production', 'cortica', 'oRAQpmiHS6RC'), event_notif(), comeback_notif())