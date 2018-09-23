import logging
import os
import re

from tms import WorkDay
from tms import scraper
from tms import calc_clk_val, conv_time_int_to_str

class WorkWeek(object):
    def __init__(self, settings):
        self.settings = settings
        self.week = {
            "Monday":WorkDay(self.settings),
            "Tuesday":WorkDay(self.settings),
            "Wednesday":WorkDay(self.settings),
            "Thursday":WorkDay(self.settings),
            "Friday":WorkDay(self.settings),
            "Saturday":WorkDay(self.settings),
            "Sunday":WorkDay(self.settings)}
        self.week_total_time = "--:--"


        self.week["Monday"].add_clocking("8:30")
        self.week["Monday"].add_clocking("16:50")
        self.week["Monday"].calc_day_total_time()

        self.week["Tuesday"].add_clocking("9:25")
        self.week["Tuesday"].add_clocking("18:50")
        self.week["Tuesday"].calc_day_total_time()

        #scraper()
        self.calc_week_total_time()
        self.display_week()
    
    def calc_week_total_time(self):
        week_total_time_min = calc_clk_val(self.week_total_time)
        for name, day in self.week.items():
            week_total_time_min = week_total_time_min + calc_clk_val(day.total_time)
            logging.debug("Week Total Time in minutes after {}: {}".format(name, week_total_time_min))
        
        self.week_total_time = conv_time_int_to_str(week_total_time_min)
        logging.debug("Week Total: {} ({})".format(self.week_total_time, week_total_time_min))
    
    def display_week(self):
        for name, day in self.week.items():
            logging.info("{}:: Clockings: {} Basic Hours: {} Auth Absense: {} Total Time: {}".format(name, [clock for clock in day.clockings], day.basic_hours, day.auth_absence, day.total_time))
        logging.info("Total Week: {}".format(self.week_total_time))