import logging

from tms import Day
from tms import ClockMinutes

def ctrl_week(settings):
    week = Week(settings)

    action_options = {"add": ActionAddClock(), "dis": ActionDisplayWeek()}
    week_menu = Menu("Work Week Menu", action_options)

    while True:
        week_menu.display_options()
        if not week_menu.sel_action(): break
        week_menu.execute_action(week)


class Week(object):
    def __init__(self, settings):
        self.settings = settings

        self.week_days = {
            "sunday":Day(self.settings),
            "monday":Day(self.settings),
            "tuesday":Day(self.settings),
            "wednesday":Day(self.settings),
            "thursday":Day(self.settings),
            "friday":Day(self.settings),
            "saturday":Day(self.settings)}
        self.total_time = ClockMinutes(0)
    
    def calc_total_time(self):
        self.total_time = ClockMinutes(0)
        for name, day in self.week_days.items():
            self.total_time = ClockMinutes(self.total_time.minutes + day.total_time.minutes)
            logging.debug("Week Total Time in minutes after {}: {}".format(name, self.total_time.minutes))


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
            action_key = input("Select an Option? ").replace(" ", "")
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


class ActionAddClock(object):
    def __init__(self):
        self.description = "Add a clock to a desire day of the week"
        
    def execute(self, week):
        while True:
            day_key = input("Input a day of the week: ").replace(" ", "")
            try:
                day = week.week_days[day_key.lower()]
            except KeyError:
                    logging.warning("WARNING: Please select a day of the week.")
                    continue
            break

        while True:
            time = input("Input a clock time (hh:mm): ").replace(" ", "")
            if day.change_attribute("add_clock", time):
                break

        week.calc_total_time()
        

class ActionDisplayWeek(object):
    def __init__(self):
        self.description = "Display the TMS information for the current week"

    def execute(self, week):
        logging.info("")
        for name, day in week.week_days.items():
            logging.info("{:9}:: Clockings: {!s:60} Basic Hours: {} Auth Absense: {} Total Time: {}".format(name, [clock.string for clock in day.clockings], day.basic_hours.string, day.auth_absence.string, day.total_time.string))
        logging.info("Total Week: {}".format(week.total_time.string))
