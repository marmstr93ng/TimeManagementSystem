import pytest
import configparser
import os

from tms import Week

class TestWeekClass():
    def setup(self):
        settings = configparser.ConfigParser()
        settings.read("{}/tms/settings.ini".format(os.getcwd()))
        self.breakrule = settings.get("Settings", "BreakRule")

        self.week = Week(settings)

    def test_calc_total_time(self):
        self.week.week_days["monday"].change_attribute("add_clock", "9:30")
        self.week.week_days["monday"].change_attribute("add_clock", "15:00")
        self.week.calc_total_time()  
        assert self.week.total_time.string == "4:45" # Account for lunch

        self.week.week_days["tuesday"].change_attribute("add_clock", "8:30")
        self.week.week_days["tuesday"].change_attribute("add_clock", "9:00")
        self.week.calc_total_time()
        if self.breakrule == "1":
            result = "5:00"
        elif self.breakrule == "2":
            result = "5:15"
        else: # Breakrule not defined in test
            result = "0:00"
        assert self.week.total_time.string == result