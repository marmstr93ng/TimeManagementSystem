import logging
import datetime
from time import strftime
import re
import math

def _conv_to_min(value, time_div):
    if time_div.lower() == 'h':
        return value * 60

def conv_time_str_to_int(time_str):
    hour, minute = re.match("([0-9]+):([0-9]+)", time_str).groups()
    return int(hour), int(minute)

def conv_time_int_to_str(time_int):
    hour = int(time_int/60)
    minute = time_int%60
    return "{}:{:02d}".format(hour, minute)

def calc_clk_val(clk):
    if clk == "--:--":
        return 0
    hour, minute = conv_time_str_to_int(clk)
    return _conv_to_min(hour, 'h') + minute


class Day(object):
    def __init__(self, settings):
        self.curr_time = datetime.datetime.now().time()

        self.settings = settings

        self.clockings = []
        self.no_clk_out = False
        self.break_time = 0
        self.basic_hours = "--:--"
        self.auth_absence = "--:--"
        self.total_time = "--:--"

    def add_clocking(self, clock_str):
        try:
            re.match("^([0-1]?[0-9]{1}|[2]{1}[0-3]{1}):([0-5]{1}[0-9]{1})$", clock_str).groups()
        except AttributeError:
            logging.warning("WARNING: Please select a properly format time")
            return False
        if self.no_clk_out:
            del self.clockings[-1]
            self.no_clk_out = False
        self.clockings.append(clock_str)
        logging.info("Adding Clock {}".format(clock_str))
        return True
    
    def calc_day_total_time(self):
        if len(self.clockings) == 0:
            raise ValueError("No Clockings added for the workday")
        
        self.total_time = "--:--"

        self._check_still_working()

        clk_pairs = math.ceil(len(self.clockings)/2)
        for pair_num in range(0, clk_pairs):
            self._modify_total_time("+", self._calc_pair_time_contrib(pair_num))

        self._modify_total_time("-", self._calc_break_time())
        self.basic_hours = self.total_time

        self._modify_total_time("+", self._calc_auth_absence())

    def _calc_pair_time_contrib(self, pair_num):
        time_clk_in = calc_clk_val(self.clockings[pair_num * 2])
        time_clk_out = calc_clk_val(self.clockings[(pair_num * 2) + 1])
        pair_total_time = time_clk_out - time_clk_in

        logging.debug("Pair {} IN: {} ({}) OUT: {} ({}) Total: {}".format(pair_num, self.clockings[(pair_num * 2)], time_clk_in, self.clockings[(pair_num * 2) + 1], time_clk_out, pair_total_time))
        return pair_total_time

    def _check_after_two(self):
        time_clk_out = calc_clk_val(self.clockings[-1])
        if time_clk_out >= calc_clk_val("14:00"):
            logging.debug("After two ({})".format(time_clk_out))
            return True
        else:
            logging.debug("Not after two ({})".format(time_clk_out))
            return False

    def _calc_break_time(self):
        if self.settings.get("Settings", "BreakRule") == "1":
            self.break_time = 15
            if self._check_after_two():
                self.break_time += 30
        elif self.settings.get("Settings", "BreakRule") == "2":
            if self._check_after_two():
                self.break_time = 45

        logging.debug("Break Time in minutes: {}".format(self.break_time))
        return self.break_time

    def _calc_auth_absence(self):
        auth_absence_min = calc_clk_val(self.auth_absence)

        logging.debug("Authorised Absence: {} ({})".format(self.auth_absence, auth_absence_min))
        return auth_absence_min

    def _modify_total_time(self, mod, time):
        total_time_min = calc_clk_val(self.total_time)
        if mod == "+":
            total_time_min += time

        elif mod == "-":
            total_time_min -= time
        else:
            raise ValueError("modification string \'{}\' not supported".format(mod))

        self.total_time = conv_time_int_to_str(total_time_min)

        logging.debug("Modifying the total time by {} minutes to {} ({})".format(time, self.total_time, total_time_min))

    def _check_still_working(self):
        if len(self.clockings)%2 != 0:
            self.add_clocking("{}:{:02d}".format(self.curr_time.hour, self.curr_time.minute))
            self.no_clk_out = True
            logging.debug("No final clk out detected. Adding current time {}:{:02d} as a clk".format(self.curr_time.hour, self.curr_time.minute))
