# Time Management System Emulator
Tool for recording and calculating work hours

Rationale: Not having your clock in card is annoying. A manager is required to input the lost data and even then the information can't be input until the next working day. This can lead to problems especially if the day the card is left is the end of the week. TMS is aimed to alleviate these problems by created a system emulator. Missed data can be input and an accurate view of the work week timings can be obtained. Speculative data can be added to see how clocking times would affect total hours.

Steps:
1. Day Calculator - A way of calculating the would-be times of the day missed.
2. Week Integration - Integrate the missing day into a complete work week
3. Automate - Method of pulling existing information off the system
4. User Friendly - System should be easier to use, probably going to mean creating a Gui

## workday.py
- clockings will appear in chronological order
- clockings will always come in pairs, the first being a clock in and the second being a clock out
- clock ins will always be even indexed (0 indexing), clock outs will always be odd indexing
- minute granularity
- all time calculations performed at lowest granularity
- "convert to minute" method added to have only one place a modification will need to occur if a change is made
- if odd number of clock ins (still at work), calculation of total time taken from current time

## scraper.py
- use of selenium to overcome user permissions issues of the script accessing the intranet page

A working chrome driver has been included in the repo but the latest can be downloaded at the following URL:
http://chromedriver.chromium.org/

Selenium browser automation can be followed at the next link
https://automatetheboringstuff.com/chapter11/ - Starting a Selenium-Controlled Browser


## ToDo (No order)
1. Multiple days - Total work week
2. User Class - pass user settings to different modules
3. Create User profile - asks name, work ID, break rule -> added to custom user settings file
4. Develop web scraper - move to main.(must be kept as an optional step to fit into other TMSs)
5. Verification check against TMS daily totals
6. Gui (QT)
7. Scrape historic clock
8. Trend (normal check in time for each day, number of work hours)
9. Error Handling (e.g. should there be a valueerror if calculate total hours off no clocks)
