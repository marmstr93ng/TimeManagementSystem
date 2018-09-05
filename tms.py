import logging
import logging.config

from tms import WorkDay
from tms import scraper

def main():
    """Function that defines the workflow of the tool"""

    logging.config.fileConfig('logging/log_settings.conf')
    logging.info("Running Time Management System Emulator")

    today = WorkDay()
    #today.get_break_rule_def("rule_2")
    today.add_clocking("9:30")
    #today.add_clocking("10:49")
    #today.add_clocking("15:22")
    #today.add_clocking("13:59")
    #today.add_clocking("16:13")
    today.calc_day_total_time()
    logging.info(today.total_time)

    #scraper()

if __name__ == '__main__':

    main()
