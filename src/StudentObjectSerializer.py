from datetime import datetime, date
import json
import numpy as np


def get_max_rank(number_of_lessons):
    ranks = ["recruit", "guardian", "watchmen", "defender", "ranger", "vigilante", "challenger", "superhero"]
    return ranks[int(np.ceil(number_of_lessons / 5)) - 1]


def calculate_rates(datetime_list):
    completion_rates_out = []
    for i in range(0, len(datetime_list)):
        if i != 0:
            date_a = date(datetime_list[i].year, datetime_list[i].month, datetime_list[i].day)
            date_b = date(datetime_list[i - 1].year, datetime_list[i - 1].month, datetime_list[i - 1].day)
            delta = date_a - date_b
            completion_rates_out.append(delta.days)
    return completion_rates_out


def convert_to_datetime(date_data):
    return [datetime.strptime(dates, "%m/%d/%y") for dates in date_data]


def create_student_object_dict(student_dates_dict):
    student_obj_dict = {}
    for key in student_dates_dict:
        if student_dates_dict[key] is not None:
            if len(student_dates_dict[key]) != 0:
                student_obj_dict[key] = Student(student_dates_dict[key], key)
    return student_obj_dict


# reads or writes from/to JSON file depending on if the optional pram student_data is present
def IO_JSON(file_name, *student_data):
    if student_data:
        print("writing to json")
        with open(file_name + ".json", "w") as write_file:
            json.dump(student_data, write_file, indent=4)  # indent = 4 to format json to match to python syntax
    else:
        print("reading from json")
        with open(file_name) as read_file:
            return json.load(read_file)


# Converts object to dict format, since we cant serialize custom objects :(
def object_to_dict_map(student_object):
    key = student_object.name
    members_dict = {
        "name": student_object.name,
        "dates": [str(s_date.date().strftime("%m/%d/%y")) for s_date in student_object.completion_dates],
        "lessons": student_object.lesson_completion_rates,
        "rank": student_object.max_rank
    }
    return key, members_dict


# Converts dict entry back to Student object format
def dict_entry_to_object_map(student_dict, key):
    print(key)
    print(student_dict[key]["dates"])
    student_out = Student(student_dict[key]["dates"], key)
    return student_out


def to_student_object_dict(json_dict):
    students_obj_dict = {}
    for key_json in json_dict:
        students_obj_dict[key_json] = dict_entry_to_object_map(json_dict, key_json)
    return students_obj_dict


def to_json_dates_dict(students_dict):
    students_json = {}
    for s_key in students_dict:
        json_key = object_to_dict_map(students_dict[s_key])[0]
        students_json[json_key] = object_to_dict_map(students_dict[s_key])[1]
    return students_json


class Student:
    name = ""
    completion_dates = []
    lesson_completion_rates = []
    max_rank = ""

    def __init__(self, dates, student_name):
        self.name = student_name
        self.completion_dates = convert_to_datetime(dates)
        self.lesson_completion_rates = calculate_rates(self.completion_dates)
        self.max_rank = get_max_rank(len(self.completion_dates))


# Some test code for the functions
"""
# read in master list of all data
student_dates = IO_JSON("studentsMCDataMaster.json")  # some error causing dict to become list :(
student_dates = student_dates[0]
# convert to objects and store in a dict
students = create_student_object_dict(student_dates)
# write to json w/ object format
students_json = {}
for s_key in students:
    json_key = object_to_dict_map(students[s_key])[0]
    students_json[json_key] = object_to_dict_map(students[s_key])[1]
print(students_json)
IO_JSON("students", students_json)
convert_to_obj_dict_test = IO_JSON("students.json")
convert_to_obj_dict_test = convert_to_obj_dict_test[0]
test = {}
for key_json in convert_to_obj_dict_test:
    test[key_json] = dict_entry_to_object_map(convert_to_obj_dict_test, key_json)

"""
