from selenium import webdriver
import os
import re

tms_url = "http://intranet.andor.com/tms/"
with webdriver.Chrome(executable_path='{}\chromedriver.exe'.format(os.getcwd())) as browser:
    browser.get(tms_url)

    user_id, user_name = re.match("TMS Clockings for ([0-9]+): (.*)", browser.find_element_by_tag_name("h1").text).groups()
    print("Welcome {} ({})".format(user_name, user_id))

    elem = browser.find_elements_by_class_name("Clocking")
    for i in range(0, len(elem)):
        print(elem[i].text)