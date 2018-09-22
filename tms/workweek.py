import logging
import os

from tms import WorkDay
from tms import scraper

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
        
        #scraper()

        #today = WorkDay(self.settings)
        #today.add_clocking("9:30")
        #today.add_clocking("10:49")
        #today.add_clocking("15:22")
        #today.add_clocking("13:59")
        #today.add_clocking("16:13")
        #today.calc_day_total_time()
        #logging.info(today.total_time)
