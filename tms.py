import os
import sys
import logging
import logging.config

def main():
    """Function that defines the workflow of the tool"""

    logging.config.fileConfig('logging/log_settings.conf')
    logging.info("Beginning Script")

if __name__ == '__main__':

    # Included to allow realtime output to the console
    # Re-opens stdout file descriptor with write mode and 0 as the buffer size
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

    main()
