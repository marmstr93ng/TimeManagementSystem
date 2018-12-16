import logging
import datetime
import re

def conv_clock_str_to_min(clock_str):
    hour, minute = re.match("([0-9]+):([0-9]+)", clock_str).groups()
    return (int(hour) * 60) + int(minute)

def conv_clock_int_to_str(clock_int):
    hour = int(clock_int/60)
    minute = clock_int%60
    return "{}:{:02d}".format(hour, minute)

def retrieve_current_time():
    unformat_curr_time = datetime.datetime.now().time()
    return "{}:{:02d}".format(unformat_curr_time.hour, unformat_curr_time.minute)


class ClockString(object):
    def __init__(self, string, is_current_time=False):
        self.string = string
        self.is_current_time = is_current_time
        self.minutes = conv_clock_str_to_min(string)


class ClockMinutes(object):
    def __init__(self, minutes):
        self.minutes = minutes
        self.string = conv_clock_int_to_str(minutes)
