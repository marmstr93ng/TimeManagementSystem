import pytest

from tms import DayNew

class TestDayClass():
    def setup(self):
        self.day = DayNew()

    def test_day_class(self):
        assert self.day.add_clocking() is True