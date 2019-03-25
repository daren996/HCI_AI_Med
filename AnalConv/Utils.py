

import datetime


# time_str format: 2018-10-14 05:17:40
def cmp_date(time_str1, time_str2):
    date_parts1 = time_str1.split(' ')[0].split('-')
    date_parts2 = time_str2.split(' ')[0].split('-')
    date1 = datetime.datetime(int(date_parts1[0]), int(date_parts1[1]), int(date_parts1[2]))
    date2 = datetime.datetime(int(date_parts2[0]), int(date_parts2[1]), int(date_parts2[2]))
    return (date1-date2).days


