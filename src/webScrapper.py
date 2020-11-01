import json
import os
import sys

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath("C:\projects\MCDataVis\StudentObjectSerializer.py")),
                                'lib'))
import StudentObjectSerializer as sos

del sys.path[0], sys, os


# presses the next page button at the button of the LMS when in the current students section
def next_page():
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "styles_list__1DkSt")))
    buttons = driver.find_element_by_class_name("styles_list__1DkSt")
    buttons = buttons.find_elements_by_tag_name("li")
    next_button = buttons[len(buttons) - 1]
    next_button.click()


# gets all the lesson start dats for a given studnet and returns them as a list of strings
def get_dates():
    try:
        print("getting dates")
        # wait for div elements containing dates to load into the webpage
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "styles_enrollmentDate__3daTq")))
        date_elements = driver.find_elements_by_class_name("styles_enrollmentDate__3daTq")
        string_dates = []
        # iterate through all elements that contain dates and return that collection as a list
        for t in range(0, len(date_elements) - 1):
            string_dates.append(date_elements[t].text)

        return string_dates
    # it is possible for a student's account to have no dates, such as an inactive account
    # in this case just return Null
    # useful to still track these elements as it gives an idea of how many in active accounts there could be
    except:
        print("no dates")
        return None


# pulls the name of the student from the top of the page when looking at a student profile in the LMS
def get_name():
    # Locate the names H2 in the lms this something like "Enrollments of STUDENT_NAME"
    name = driver.find_element_by_tag_name("h1").text
    # shorten to remove all elements of the string that aren't part of the actual name
    name = name[15:]
    print(name)
    return name


# grabs all hyperlinks found in current students and stores them in a list
# this list can be used to navigate to specific student profiles
def get_links():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "td")))
    view_links = driver.find_elements_by_link_text("View")
    return view_links


# returns to the current page of students
def get_to_current_page(page):
    for number_of_clicks in range(15 - page, 15):
        next_page()


# Lambda to merge dicts
dict_merge = lambda dict_a, dict_b: dict_a.update(dict_b) or dict_a

# Web scrapper run
# Pattern:
# - Load mc.live
# - Enter login info
# - Navigate to current students
# - From current students iterate through all pages
# - For each student on a page get all date stamps from their profile
# - Add student and their date collection to a dict
# - Serialize to JSON file

# Set up webdriver for chrome
driver = selenium.webdriver.Chrome("/Users/Miles/Downloads/chromedriver")
driver.get("https://mighty.codenow.live")
# wait for input boxes to load
wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input")))
# Login into mc.live
# Bothell account:
# - User: milessmith1809@gmail.com
# - PW: 3XRakrXy2V5278y
# Kirkland account
# - User: miles+milessmith1809@gmail.com
# - PW: mightymiles
id_box = driver.find_element_by_name("login")
pass_box = driver.find_element_by_name("password")
id_box.send_keys("miles+milessmith1809@gmail.com")  # this is currently for kirkland
pass_box.send_keys("mightymiles")
login_element = driver.find_element_by_class_name("styles_variantText__2Csd6")
login_element.click()

# wait for side bar to load, and then click on it to see the page of current students
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "styles_navItem__1WtMM")))
current_students = driver.find_elements_by_class_name("styles_navItem__1WtMM")
current_students = driver.find_elements_by_class_name("styles_navItem__1WtMM")
current_students = current_students.find_elements_by_tag_name("li")
current_students[1].click()
# iterate through all pages and through students to build a dict of students and start dates
# dict set up {key:"student_name",value:[collection of all start dates for courses]}
students = {}
# range corresponds to number of pages defined at the bottom when when in the current students section of the site
# so in this case 0 - 3 is for kirkland, since there are only 3 pages worth of students for that LMS
for i in range(0, 3):

    number_students = len(get_links())  # the number of students on the current page
    print("no of students " + str(number_students))

    for x in range(0, number_students):
        links = get_links()
        current_link = links[x]
        current_link.click()
        dates = get_dates()
        current_name = get_name()
        students[current_name] = dates
        # every time you click on current students in the sidebar it returns to the first page
        # so the function get_to_current_page will re nav back to the current page
        current_students[1].click()
        get_to_current_page(i)
        # after getting all data for a page we move to the next one and repeat
    current_students[1].click()
    print("moving to next page")
    get_to_current_page(i)

# Write to json
# IO_JSON("studentsMCDataKirkland", students)
# Open both kirk and both json data to combine into a master list
kirk_data = sos.IO_JSON("studentsMCDataKirkland.json")  # for some reason this is a list now ?????
both_data = sos.IO_JSON("studentsMCData.json")
# Add kirk to bothell data
students_data_master = dict_merge(both_data, kirk_data[0])
print(len(students_data_master))
# Write to a master data file
sos.IO_JSON("studentsMCDataMaster", students_data_master)
# From master file create dict of objects and write to JSON file
students = sos.IO_JSON("studentsMCDataMaster.json")[0]
students = sos.create_student_object_dict(students)
sos.IO_JSON("students", students)
