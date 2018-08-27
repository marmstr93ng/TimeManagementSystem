import datetime
from time import strftime
import re
import math

class WorkDay(object):
    def __init__(self):
        self.curr_time = datetime.datetime.now().time()
        self.clockings = []
        self.total_time_min = 0
        self.total_time = ""
        self.break_time = 0
        self.no_clk_out = False

    def add_clocking(self, clock_str):
        self.clockings.append(clock_str)

    def conv_to_min(self, value, time_div):
        if time_div.lower() == 'h':
            return value * 60

    def conv_time_str_to_int(self, time_str):
        hour, minute = re.match("([0-9]+):([0-9]+)", time_str).groups()
        return int(hour), int(minute)

    def conv_time_int_to_str(self, time_int):
        hour = int(time_int/60)
        minute = time_int%60
        return "{}:{:02d}".format(hour, minute)

    def calc_clk_val(self, clk):
        hour, minute = self.conv_time_str_to_int(clk)
        return self.conv_to_min(hour, 'h') + minute

    def calc_pair_time_contrib(self, pair_num):
        time_clk_in = self.calc_clk_val(self.clockings[pair_num * 2])

        if self.clockings[pair_num * 2] == self.clockings[-1]: # Checks pair only has one element (will only be possibly true for last pair)
            print("No clk out detected for pair {}. Using current time: {}:{:02d}".format(pair_num, self.curr_time.hour, self.curr_time.minute))
            time_clk_out = self.conv_to_min(self.curr_time.hour, 'h') + self.curr_time.minute

            print("Pair {} (min) IN: {} ({}) OUT: {}:{:02d} ({})".format(pair_num, self.clockings[(pair_num * 2)], time_clk_in, self.curr_time.hour, self.curr_time.minute, time_clk_out))
        else:
            time_clk_out = self.calc_clk_val(self.clockings[(pair_num * 2) + 1])

            print("Pair {} IN: {} ({}) OUT: {} ({})".format(pair_num, self.clockings[(pair_num * 2)], time_clk_in, self.clockings[(pair_num * 2) + 1], time_clk_out))

        return time_clk_out - time_clk_in

    def calc_break_time(self):
        # Rule 1: if after 14:00 45 min
        # Rule 2: 15 min at start of day and if after 14:00 30min
        # returns total break time to be deducted fromt the total
        # Rule needs to be identfied

        # Use this structure in a function that can be used to calculate clock out time in pair_time_contrib (if final pair? or some more clever calc around passing in clockings with index)
        if len(self.clockings)%2 == 0:
            self.no_clk_out = True
            time_clk_out = self.calc_clk_val(self.clockings[-1])
        else:
            print("No final clk out detected. Using current time: {}:{:02d}".format(self.curr_time.hour, self.curr_time.minute))
            time_clk_out = self.conv_to_min(self.curr_time.hour, 'h') + self.curr_time.minute

        if time_clk_out >= self.calc_clk_val("14:00"):
            self.break_time = 45

        print("Break Time in minutes: {}".format(self.break_time))
        return self.break_time

    def modify_total_time(self, mod, time):
        if mod == "+":
            self.total_time_min = self.total_time_min + time

        elif mod == "-":
            self.total_time_min = self.total_time_min - time
        else:
            raise ValueError("modification string \'{}\' not supported".format(mod))

        self.total_time = self.conv_time_int_to_str(self.total_time_min)

    def calc_day_total_time(self):
        if len(self.clockings) == 0:
            raise ValueError("No Clockings added for the workday")

        if len(self.clockings)%2 == 0:
            self.no_clk_out = True
            self.add_clocking()

        clk_pairs = math.ceil(len(self.clockings)/2)
        for pair_num in range(0, clk_pairs):

            pair_time = self.calc_pair_time_contrib(pair_num)
            print("Pair {} time in minutes: {}".format(pair_num, pair_time))

            self.modify_total_time("+", pair_time)
            print("Current Total Time (min): {} ({})".format(self.total_time, self.total_time_min))

        self.modify_total_time("-", self.calc_break_time())

today = WorkDay()
today.add_clocking("9:28")
#today.add_clocking("12:09")
#today.add_clocking("13:01")
#today.add_clocking("13:59")
#today.add_clocking("16:13")
today.calc_day_total_time()
print(today.total_time)