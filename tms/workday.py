import logging
import datetime
from time import strftime
import re
import math

class WorkDay(object):
    def __init__(self, settings):
        self.curr_time = datetime.datetime.now().time()

        self.settings = settings

        self.clockings = []
        self.no_clk_out = False
        self.total_time_min = 0
        self.total_time = ""
        self.break_time = 0
        self.auth_absence = "--:--"

    def add_clocking(self, clock_str):
        self.clockings.append(clock_str)
        logging.info("Adding Clock {}".format(clock_str))

    def _conv_to_min(self, value, time_div):
        if time_div.lower() == 'h':
            return value * 60

    def _conv_time_str_to_int(self, time_str):
        hour, minute = re.match("([0-9]+):([0-9]+)", time_str).groups()
        return int(hour), int(minute)

    def _conv_time_int_to_str(self, time_int):
        hour = int(time_int/60)
        minute = time_int%60
        return "{}:{:02d}".format(hour, minute)

    def _calc_clk_val(self, clk):
        hour, minute = self._conv_time_str_to_int(clk)
        return self._conv_to_min(hour, 'h') + minute

    def _calc_pair_time_contrib(self, pair_num):
        time_clk_in = self._calc_clk_val(self.clockings[pair_num * 2])
        time_clk_out = self._calc_clk_val(self.clockings[(pair_num * 2) + 1])
        pair_total_time = time_clk_out - time_clk_in

        logging.debug("Pair {} IN: {} ({}) OUT: {} ({}) Total: {}".format(pair_num, self.clockings[(pair_num * 2)], time_clk_in, self.clockings[(pair_num * 2) + 1], time_clk_out, pair_total_time))
        return pair_total_time

    def _check_after_two(self):
        time_clk_out = self._calc_clk_val(self.clockings[-1])
        if time_clk_out >= self._calc_clk_val("14:00"):
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
        if self.auth_absence == "--:--":
            auth_absence_min = 0
        else:
            auth_absence_min = self._calc_clk_val(self.auth_absence)

        logging.debug("Authorised Absence: {} ({})".format(self.auth_absence, auth_absence_min))
        return auth_absence_min

    def _modify_total_time(self, mod, time):
        if mod == "+":
            self.total_time_min = self.total_time_min + time

        elif mod == "-":
            self.total_time_min = self.total_time_min - time
        else:
            raise ValueError("modification string \'{}\' not supported".format(mod))

        self.total_time = self._conv_time_int_to_str(self.total_time_min)

        logging.debug("Modifying the total time by {} minutes to {} ({})".format(time, self.total_time, self.total_time_min))

    def _check_still_working(self):
        if len(self.clockings)%2 != 0:
            self.no_clk_out = True
            self.add_clocking("{}:{:02d}".format(self.curr_time.hour, self.curr_time.minute))
            logging.debug("No final clk out detected. Adding current time {}:{:02d} as a clk".format(self.curr_time.hour, self.curr_time.minute))

    def calc_day_total_time(self):
        if len(self.clockings) == 0:
            raise ValueError("No Clockings added for the workday")

        self._check_still_working()

        clk_pairs = math.ceil(len(self.clockings)/2)
        for pair_num in range(0, clk_pairs):
            self._modify_total_time("+", self._calc_pair_time_contrib(pair_num))

        self._modify_total_time("-", self._calc_break_time())

        self._modify_total_time("+", self._calc_auth_absence())