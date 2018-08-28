from selenium import webdriver
import os
import re

# tms_url = "http://intranet.andor.com/tms/"
tms_url = '{}\TMS Clockings Record Two Days.html'.format(os.getcwd())

with webdriver.Chrome(executable_path='{}\chromedriver.exe'.format(os.getcwd())) as browser:
    browser.get(tms_url)

    user_id, user_name = re.match("TMS Clockings for ([0-9]+): (.*)", browser.find_element_by_tag_name("h1").text).groups()
    print("Welcome {} ({})".format(user_name, user_id))

    elem = browser.find_elements_by_class_name("past")
    #for i in range(0, len(elem)):
    #    print("{}: {}".format(i, elem[i].text))

    for i in range(0, int(len(elem)/5)):
        day_str, date_str = re.match("([A-Za-z]+)\n([0-9]{2}/[0-9]{2}/[0-9]{2})", elem[0].text).groups()
        print("{}: {}".format(day_str, date_str))
        print("{}".format(re.findall("([0-9]+:[0-9]+)", elem[1].text)))
        basic_hrs = elem[2].text
        print("Basic Hours: {}".format(basic_hrs))
        auth_absence = elem[3].text
        print("Authorised Absence: {}".format(auth_absence))
        total_hrs = elem[4].text
        print("Total hours: {}".format(total_hrs))

    elem = browser.find_elements_by_class_name("present")
    for i in range(0, int(len(elem)/5)):
        day_str, date_str = re.match("([A-Za-z]+)\n([0-9]{2}/[0-9]{2}/[0-9]{2})", elem[0].text).groups()
        print("{}: {}".format(day_str, date_str))
        print("{}".format(re.findall("([0-9]+:[0-9]+)", elem[1].text)))
        basic_hrs = elem[2].text
        print("Basic Hours: {}".format(basic_hrs))
        auth_absence = elem[3].text
        print("Authorised Absence: {}".format(auth_absence))
        total_hrs = elem[4].text
        print("Total hours: {}".format(total_hrs))
