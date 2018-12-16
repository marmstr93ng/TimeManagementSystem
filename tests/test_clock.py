import pytest
import re

from tms import conv_clock_str_to_min
from tms import conv_clock_int_to_str
from tms import retrieve_current_time
from tms import ClockString

def test_conv_clock_str_to_min():
    assert conv_clock_str_to_min("2:00") == 120
    assert conv_clock_str_to_min("5:22") == 322

def test_conv_clock_int_to_str():
    assert conv_clock_int_to_str(120) == "2:00"
    assert conv_clock_int_to_str(322) == "5:22"

def test_retrieve_current_time():
    hour, minute = re.match("([0-9]+):([0-9]+)", retrieve_current_time()).groups()
    assert ((int(hour) >= 0) and (int(hour) < 24)) == True
    assert ((int(minute) >= 0) and (int(minute) < 60)) == True

def test_clock_class():
    clock = ClockString("1:00")
    assert clock.string == "1:00"
    assert clock.minutes == 60
    assert clock.is_current_time == False

    clock = ClockString("4:56", True)
    assert clock.string == "4:56"
    assert clock.minutes == 296
    assert clock.is_current_time == True