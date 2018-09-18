import logging
import logging.config
import configparser
import os

from tms import WorkWeek
#from tms import scraper

def main():
    """Function that defines the workflow of the tool"""

    logging.config.fileConfig('logging/log_settings.conf')
    logging.info("Running Time Management System Emulator")

    settings = configparser.ConfigParser()
    settings.read("{}/tms/settings.ini".format(os.getcwd()))

    WorkWeek(settings)
    #scraper()

if __name__ == '__main__':

    main()
