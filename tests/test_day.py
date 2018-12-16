import pytest
import configparser
import os

from tms import BreakRule
from tms import Day

class TestDayClass():
    def setup(self):
        settings = configparser.ConfigParser()
        settings.read("{}/tms/settings.ini".format(os.getcwd()))

        self.breakrule = BreakRule(settings)
        self.og_breakrule = settings.get("Settings", "BreakRule")

        self.day = Day(settings)

    def test_add_clock(self):
        self.day._add_clock("6:00")
        assert self.day.clockings[0].string == "6:00"
        assert self.day.clockings[0].is_current_time == False

        self.day._add_clock("10:00", True)
        assert self.day.clockings[1].string == "10:00"
        assert self.day.clockings[1].is_current_time == True
        
        self.day._add_clock("6:30")
        assert self.day.clockings[1].string == "6:30"
        assert self.day.clockings[1].is_current_time == False
        assert self.day.clockings[2].string == "10:00"
        assert self.day.clockings[2].is_current_time == True
    
    def test_remove_clock(self):
        self.day._add_clock("2:00")
        self.day._add_clock("5:00")
        assert len(self.day.clockings) == 2
        self.day._remove_clock("2:00")
        assert len(self.day.clockings) == 1

    def test_update_auth_absence(self):
        assert self.day.auth_absence.minutes == 0
        self.day._update_auth_absence("2:00")
        assert self.day.auth_absence.minutes == 120

    def test_calc_pair_time_contrib(self):
        self.day._add_clock("1:00")
        self.day._add_clock("1:20")
        assert self.day._calc_pair_time_contrib(0) == 20

        self.day._add_clock("5:00")
        self.day._add_clock("9:45")
        assert self.day._calc_pair_time_contrib(1) == 285
    
    def test_modify_for_incomplete_pair(self):
        self.day._add_clock("11:00")
        assert len(self.day.clockings) == 1
        self.day._modify_for_incomplete_pair()
        assert len(self.day.clockings) == 2
        self.day._add_clock("9:00")
        self.day._modify_for_incomplete_pair()
        assert len(self.day.clockings) == 2
        self.day._add_clock("15:36")
        self.day._modify_for_incomplete_pair()
        assert len(self.day.clockings) == 4
    
    def test_check_after_two(self):
        self.day._add_clock("11:00")
        assert self.day._check_after_two() == False
        self.day._add_clock("16:00")
        assert self.day._check_after_two() == True
    
    def test_calc_break_time(self):
        self.breakrule._update_break_rule("1")
        self.day._add_clock("9:00")
        assert self.day._calc_break_time() == 15

        self.day._add_clock("17:00")
        assert self.day._calc_break_time() == 45

        self.breakrule._update_break_rule("2")
        self.day._remove_clock("17:00")
        assert self.day._calc_break_time() == 0
        self.day._add_clock("18:00")
        assert self.day._calc_break_time() == 45

    def test_calc_total_time(self):
        self.day._add_clock("9:00")
        self.day._calc_total_time()
        self.day._add_clock("12:45")
        self.day._calc_total_time()
        assert self.day.total_time.minutes == (225 - 15 + 0)
        assert self.day.basic_hours.minutes == (225 - 15)
        self.day._add_clock("15:00")
        self.day._calc_total_time()
        self.day._add_clock("16:00")
        self.day._update_auth_absence("0:30")
        self.day._calc_total_time()
        assert self.day.total_time.minutes == (285 - 45 + 30)
        assert self.day.basic_hours.minutes == (285 - 45)
    
    def test_change_attribute(self):
        assert self.day.change_attribute("add_clock", "4:00") == True
        assert self.day.change_attribute("add_clock", "89:00") == False
        assert self.day.change_attribute("add_clock", "4:76") == False
        print([clock.string for clock in self.day.clockings])
        assert len(self.day.clockings) == 2

        assert self.day.change_attribute("remove_clock", "4:00") == True
        assert len(self.day.clockings) == 0

        assert self.day.change_attribute("update_auth_absence", "0:33") == True
        assert self.day.auth_absence.string == "0:33"
    
    def teardown(self):
        self.breakrule._update_break_rule(self.og_breakrule)