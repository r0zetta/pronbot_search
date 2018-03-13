from datetime import datetime, date, time, timedelta
import time
import re

def twitter_time_to_readable(time_string):
    twitter_format = "%a %b %d %H:%M:%S %Y"
    match_expression = "^(.+)\s(\+[0-9][0-9][0-9][0-9])\s([0-9][0-9][0-9][0-9])$"
    match = re.search(match_expression, time_string)
    if match is not None:
        first_bit = match.group(1)
        second_bit = match.group(2)
        last_bit = match.group(3)
        new_string = first_bit + " " + last_bit
        date_object = datetime.strptime(new_string, twitter_format)
        return date_object.strftime("%Y-%m-%d %H:%M:%S")

def twitter_time_to_object(time_string):
    twitter_format = "%a %b %d %H:%M:%S %Y"
    match_expression = "^(.+)\s(\+[0-9][0-9][0-9][0-9])\s([0-9][0-9][0-9][0-9])$"
    match = re.search(match_expression, time_string)
    if match is not None:
        first_bit = match.group(1)
        second_bit = match.group(2)
        last_bit = match.group(3)
        new_string = first_bit + " " + last_bit
        date_object = datetime.strptime(new_string, twitter_format)
        return date_object

def twitter_time_to_unix(time_string):
    return time_object_to_unix(twitter_time_to_object(time_string))

def seconds_to_days(seconds):
    return float(float(seconds)/86400.00)

def seconds_since_twitter_time(time_string):
    input_time_unix = int(twitter_time_to_unix(time_string))
    current_time_unix = int(get_utc_unix_time())
    return current_time_unix - input_time_unix

def time_object_to_readable(time_object):
    return time_object.strftime("%Y-%m-%d %H:%M:%S")

def time_string_to_object(time_string):
    return datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')

def time_object_to_string(time_object):
    return datetime.strftime(time_object, '%Y-%m-%d %H:%M:%S')

def time_object_to_month(time_object):
    return datetime.strftime(time_object, '%Y-%m')

def time_object_to_week(time_object):
    return datetime.strftime(time_object, '%Y-%U')

def time_object_to_day(time_object):
    return datetime.strftime(time_object, '%Y-%m-%d')

def time_object_to_hour(time_object):
    return datetime.strftime(time_object, '%Y-%m-%d-%H')

def time_object_to_unix(time_object):
    return int(time_object.strftime("%s"))

def get_utc_unix_time():
    dts = datetime.utcnow()
    epochtime = time.mktime(dts.timetuple())
    return epochtime

def unix_time_to_readable(time_string):
    return datetime.fromtimestamp(int(time_string)).strftime('%Y-%m-%d %H:%M:%S')

def get_datestring(data_type=None, offset=0):
    if data_type is "hour":
        time_here = datetime.utcnow() - timedelta(hours = offset)
        ymd = time_here.strftime("%Y%m%d")
        hour = int(time_here.strftime("%H"))
        hour_string = "%02d" % hour
        return ymd + hour_string
    else:
        time_here = datetime.utcnow() - timedelta(days = offset)
        ymd = time_here.strftime("%Y%m%d")
        return ymd

def create_heatmap(timestamps):
    heatmap = [[0 for j in range(24)] for i in range(7)]
    for t in timestamps:
        weekday = t.weekday()
        hour = t.hour
        heatmap[weekday][hour] = heatmap[weekday][hour] + 1
    return heatmap

