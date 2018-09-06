import logging
import logging.config

from tms import WorkWeek
#from tms import scraper

def main():
    """Function that defines the workflow of the tool"""

    logging.config.fileConfig('logging/log_settings.conf')
    logging.info("Running Time Management System Emulator")

    week = WorkWeek()
    #scraper()

if __name__ == '__main__':

    main()
