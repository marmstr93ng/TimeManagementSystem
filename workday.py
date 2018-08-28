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
        self.break_rule = "rule_1"
        self.no_clk_out = False

    def add_clocking(self, clock_str):
        self.clockings.append(clock_str)

    def get_break_rule_def(self, break_rule=None):
        if not break_rule: break_rule = self.break_rule
        rule_def = {"rule_1":"If after 14:00, 45 minutes deducted", "rule_2":"15 minutes deducted on arrival with the remaining 30 minutes subtracted after 14:00"}
        print("{}: {}".format(break_rule, rule_def.get(break_rule,"Rule doesn't exist")))

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
        print("Pair {} IN: {} ({}) OUT: {} ({})".format(pair_num, self.clockings[(pair_num * 2)], time_clk_in, self.clockings[(pair_num * 2) + 1], time_clk_out))

        return time_clk_out - time_clk_in

    def _check_after_two(self):
        time_clk_out = self._calc_clk_val(self.clockings[-1])
        if time_clk_out >= self._calc_clk_val("14:00"):
            return True
        else:
            return False

    def _calc_break_time(self):
        if self.break_rule == "rule_1":
            self.break_time = 15
            if self._check_after_two():
                self.break_time += 30
        elif self.break_time == "rule_2":
            if self._check_after_two():
                self.break_time = 45

        print("Break Time in minutes: {}".format(self.break_time))
        return self.break_time

    def _modify_total_time(self, mod, time):
        if mod == "+":
            self.total_time_min = self.total_time_min + time

        elif mod == "-":
            self.total_time_min = self.total_time_min - time
        else:
            raise ValueError("modification string \'{}\' not supported".format(mod))

        self.total_time = self._conv_time_int_to_str(self.total_time_min)

    def calc_day_total_time(self):
        if len(self.clockings) == 0:
            raise ValueError("No Clockings added for the workday")

        if len(self.clockings)%2 != 0:
            self.no_clk_out = True
            self.add_clocking("{}:{:02d}".format(self.curr_time.hour, self.curr_time.minute))
            print("No final clk out detected. Adding current time: {}:{:02d}".format(self.curr_time.hour, self.curr_time.minute))

        clk_pairs = math.ceil(len(self.clockings)/2)
        for pair_num in range(0, clk_pairs):

            pair_time = self._calc_pair_time_contrib(pair_num)
            print("Pair {} time in minutes: {}".format(pair_num, pair_time))

            self._modify_total_time("+", pair_time)
            print("Current Total Time (min): {} ({})".format(self.total_time, self.total_time_min))

        self._modify_total_time("-", self._calc_break_time())

today = WorkDay()
#today.get_break_rule_def("rule_2")
today.add_clocking("9:28")
#today.add_clocking("12:09")
#today.add_clocking("13:01")
#today.add_clocking("13:59")
#today.add_clocking("16:13")
today.calc_day_total_time()
print(today.total_time)