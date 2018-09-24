import logging
import os
import re

from tms import WorkDay
from tms import scraper
from tms import calc_clk_val, conv_time_int_to_str

def cmd_week(settings):
    workweek = WorkWeek(settings)

    action_options = {"add": ActionAddClock(), "dis": ActionDisplayWeek()}
    week_menu = Menu("Work Week Menu", action_options)

    while True:
        week_menu.display_options()
        if not week_menu.sel_action(): break
        week_menu.execute_action(workweek)


class Menu(object):
    def __init__(self, title, action_options):
        self.menu_title = title
        self.action_options = action_options
        self.current_option = None
    
    def display_options(self):
        logging.info("\n{}:".format(self.menu_title)) 
        for key, value in self.action_options.items():
            logging.info("  {:10} = {}".format(key, value.description))
        logging.info("  {:10} = Quit".format("q"))
    
    def sel_action(self):
        while True:
            action_key = input("Select an Option? ")
            if action_key.lower() == 'q':
                return False
            else:
                try:
                    self.current_option = self.action_options[action_key]
                except KeyError:
                    logging.warning("WARNING: Please enter an option for the above choices.")
                    continue
                return True
    
    def execute_action(self, *args):
        self.current_option.execute(*args)


class WorkWeek(object):
    def __init__(self, settings):
        self.settings = settings

        self.week = {
            "monday":WorkDay(self.settings),
            "tuesday":WorkDay(self.settings),
            "wednesday":WorkDay(self.settings),
            "thursday":WorkDay(self.settings),
            "friday":WorkDay(self.settings),
            "saturday":WorkDay(self.settings),
            "sunday":WorkDay(self.settings)}
        self.week_total_time = "--:--"
    
    def calc_week_total_time(self):
        week_total_time_min = 0
        for name, day in self.week.items():
            week_total_time_min = week_total_time_min + calc_clk_val(day.total_time)
            logging.debug("Week Total Time in minutes after {}: {}".format(name, week_total_time_min))
        
        self.week_total_time = conv_time_int_to_str(week_total_time_min)
        logging.debug("Week Total: {} ({})".format(self.week_total_time, week_total_time_min))


class ActionAddClock(object):
    def __init__(self):
        self.description = "Add a clock to a desire day of the week"
        
    def execute(self, workweek):
        while True:
            day_key = input("Input a day of the week: ")
            try:
                day = workweek.week[day_key.lower()]
            except KeyError:
                    logging.warning("WARNING: Please select a day of the week.")
                    continue
            break

        while True:
            time = input("Input a clock time (hh:mm): ")
            try:
                re.match("([0-9]+):([0-9]+)", time).groups()
            except AttributeError:
                logging.warning("WARNING: Please select a properly format time")
                continue
            break

        day.add_clocking(time)
        day.calc_day_total_time()
        workweek.calc_week_total_time()
        

class ActionDisplayWeek(object):
    def __init__(self):
        self.description = "Display the TMS information for the current week"

    def execute(self, workweek):
        for name, day in workweek.week.items():
            logging.info("{:9}:: Clockings: {!s:60} {status} Basic Hours: {} Auth Absense: {} Total Time: {}".format(name, [clock for clock in day.clockings], day.basic_hours, day.auth_absence, day.total_time, status="True" if day.no_clk_out else "    "))
        logging.info("Total Week: {}".format(workweek.week_total_time))
