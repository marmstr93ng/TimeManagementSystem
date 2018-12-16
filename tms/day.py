import logging
import re

from tms import ClockString, ClockMinutes
from tms import retrieve_current_time

def inspect_min(elem):
    return elem.minutes

class Day(object):
    def __init__(self, settings):
        self.settings = settings

        self.clockings = []
        self.break_time = ClockMinutes(0)
        self.basic_hours = ClockMinutes(0)
        self.auth_absence = ClockString("00:00")
        self.total_time = ClockMinutes(0)
    
    def change_attribute(self, change, time):
        try:
            re.match("^([0-1]?[0-9]{1}|[2]{1}[0-3]{1}):([0-5]{1}[0-9]{1})$", time).groups()
        except AttributeError:
            logging.warning("WARNING: Please select a properly format time")
            return False
        getattr(self, "_{}".format(change))(time)
        self._calc_total_time()
        return True
    
    def _add_clock(self, time, is_current_time=False):
        self.clockings.append(ClockString(time, is_current_time))
        logging.debug("Adding clock {} ({}) to clockings list".format(self.clockings[-1].minutes, self.clockings[-1].string))
        self.clockings.sort(key=inspect_min)
        logging.debug("Sorting the clocking list: {}".format([clock.string for clock in self.clockings]))

    def _remove_clock(self, time):
        for clock in self.clockings:
            if clock.string == time:
                self.clockings.remove(clock)
                logging.debug("Removing clock {} ({}) from clockings list".format(clock.minutes, clock.string))
    
    def _update_auth_absence(self, string):
        self.auth_absence = ClockString(string)
        logging.debug("Updating authorised absence: {} ({})".format(self.auth_absence.minutes, self.auth_absence.string))

    def _calc_total_time(self):
        self._modify_for_incomplete_pair()

        if len(self.clockings) != 0:
            self.total_time = ClockMinutes(0)
        
            for pair_num in range(0, int(len(self.clockings)/2)):
                self.total_time = ClockMinutes(self.total_time.minutes + self._calc_pair_time_contrib(pair_num))
                logging.debug("New total time: {}".format(self.total_time))
        
            self.total_time = ClockMinutes(self.total_time.minutes - self._calc_break_time())
            self.basic_hours = self.total_time

            self.total_time = ClockMinutes(self.total_time.minutes + self.auth_absence.minutes)
    
    def _modify_for_incomplete_pair(self):
        for clock in self.clockings:
            if clock.is_current_time:
                self._remove_clock(clock.string)
                logging.debug("Removing current time clock: {}".format(clock.string))
        if len(self.clockings)%2 != 0:
            current_time_string = retrieve_current_time()
            self._add_clock(current_time_string, True)
            logging.debug("Adding current time clock: {}".format(current_time_string))

    def _calc_pair_time_contrib(self, pair_num):
        time_clk_in = self.clockings[pair_num * 2].minutes
        time_clk_out = self.clockings[(pair_num * 2) + 1].minutes
        pair_total_time = time_clk_out - time_clk_in

        logging.debug("Pair {} IN: {} OUT: {} Total: {}".format(pair_num, time_clk_in, time_clk_out, pair_total_time))
        return pair_total_time

    def _check_after_two(self):
        if self.clockings[-1].minutes >= 840:
            logging.debug("After two ({})".format(self.clockings[-1].minutes))
            return True
        else:
            logging.debug("Not after two ({})".format(self.clockings[-1].minutes))
            return False
        
    def _calc_break_time(self):
        self.break_time = ClockMinutes(0)
        if self.settings.get("Settings", "BreakRule") == "1":
            if self._check_after_two():
                self.break_time = ClockMinutes(45)
        elif self.settings.get("Settings", "BreakRule") == "2":
            self.break_time = ClockMinutes(15)
            if self._check_after_two():
                self.break_time = ClockMinutes(self.break_time.minutes + 30)

        logging.debug("Break Time in minutes: {}".format(self.break_time))
        return self.break_time.minutes