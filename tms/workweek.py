import logging
import configparser
import os

from tms import WorkDay
from tms.breakrule import BreakRule

class WorkWeek(object):
    def __init__(self):
        self.settings = configparser.ConfigParser()
        self.settings.read("{}/tms/settings.ini".format(os.getcwd()))

        self.week = {
            "Monday":WorkDay(),
            "Tuesday":WorkDay(),
            "Wednesday":WorkDay(),
            "Thursday":WorkDay(),
            "Friday":WorkDay(),
            "Saturday":WorkDay(),
            "Sunday":WorkDay()}

        breakrule = BreakRule()
        #breakrule.update_break_rule()
        breakrule.get_break_rule()
        breakrule.get_break_rule("2")

        #today = WorkDay()
        #today.add_clocking("9:30")
        #today.add_clocking("10:49")
        #today.add_clocking("15:22")
        #today.add_clocking("13:59")
        #today.add_clocking("16:13")
        #today.calc_day_total_time()
        #logging.info(today.total_time)
