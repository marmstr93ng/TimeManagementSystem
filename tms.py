import logging
import logging.config

from tms import WorkDay

def main():
    """Function that defines the workflow of the tool"""

    logging.config.fileConfig('logging/log_settings.conf')
    logging.info("Beginning Script")

    today = WorkDay()
    #today.get_break_rule_def("rule_2")
    today.add_clocking("9:28")
    today.add_clocking("12:09")
    today.add_clocking("13:01")
    #today.add_clocking("13:59")
    #today.add_clocking("16:13")
    today.calc_day_total_time()
    print(today.total_time)

if __name__ == '__main__':

    main()
