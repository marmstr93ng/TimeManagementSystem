# TimeManagementSystem
Tool for recording and calculating work hours

## workday.py
- clockings will appear in chronological order
- clockings will always come in pairs, the first being a clock in and the second being a clock out
- clock ins will always be even indexed (0 indexing), clock outs will always be odd indexing
- minute granularity
- all time calculations performed at lowest granularity
- "convert to minute" method added to have only one place a modification will need to occur if a change is made
- if odd number of clock ins (still at work), calculation of total time taken from current time

## scraper.py
A working chrome driver has been included in the repo but the latest can be downloaded at the following URL:
http://chromedriver.chromium.org/

Selenium browser automation can be followed at the next link
https://automatetheboringstuff.com/chapter11/ - Starting a Selenium-Controlled Browser


## ToDo
1. Python project layout - modules? utilities (e.g. chromedriver)
2. Logging
3. Lunch Rules
4. Multiple days - Total work week
5. Develop web scraper
6. Verification check against TMS daily totals
7. Gui

