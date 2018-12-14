import logging
import logging.config
import configparser
import os

from tms import ctrl_week
from tms import BreakRule

def main():
    """Function that defines the workflow of the tool"""

    logging.config.fileConfig('logging/log_settings.conf')
    logging.info("Running Time Management System Emulator")

    settings = configparser.ConfigParser()
    settings.read("{}/tms/settings.ini".format(os.getcwd()))

    ctrl_week(settings)

    #breakrule = BreakRule(self.settings)
    #breakrule.print_rules()
    #breakrule.get_break_rule()
    #breakrule.get_break_rule("2")
    #breakrule.cmd_update_break_rule()

if __name__ == '__main__':

    main()
