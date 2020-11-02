from datetime import datetime, date
import json
import numpy as np


def get_max_rank(number_of_lessons):
    """

    :param number_of_lessons:
    :return:
    """
    ranks = ["recruit", "guardian", "watchmen", "defender", "ranger", "vigilante", "challenger", "superhero"]
    return ranks[int(np.ceil(number_of_lessons / 5)) - 1]


def calculate_rates(datetime_list):
    """

    :param datetime_list:
    :return:
    """
    completion_rates_out = []
    for i in range(0, len(datetime_list)):
        if i != 0:
            date_a = date(datetime_list[i].year, datetime_list[i].month, datetime_list[i].day)
            date_b = date(datetime_list[i - 1].year, datetime_list[i - 1].month, datetime_list[i - 1].day)
            delta = date_a - date_b
            completion_rates_out.append(delta.days)
    return completion_rates_out


def convert_to_datetime(date_data):
    """

    :param date_data:
    :return:
    """
    return [datetime.strptime(dates, "%m/%d/%y") for dates in date_data]


def calculate_times_and_dates_per_rank(lessons, lesson_dates):
    """

    :param lessons:
    :param lesson_dates:
    :return:
    """
    time_per_rank = []
    date_per_rank = []
    current_rank_rates = []
    total_completed_lessons = len(lessons)
    for i in range(0, total_completed_lessons):
        if i % 5 == 0 and i != 0 or i + 1 == total_completed_lessons:
            time_per_rank.append(sum(current_rank_rates))
            date_per_rank.append(lesson_dates[i])
            current_rank_rates = [lessons[i]]
        else:
            current_rank_rates.append(lessons[i])
    return time_per_rank, date_per_rank


def calculate_average_rate_per_rank(lessons):
    """

    :param lessons:
    :return:
    """
    avg_rates = []
    total_completed_lessons = len(lessons)
    current_rank_rates = []
    for i in range(0, total_completed_lessons):
        # 1 rank = 5 lesson so the avg lesson per rank comp  time = sum(lessonRates)/5
        # check if at 5th lesson or at the end of the list (aka current rank in time)
        if i % 5 == 0 and i != 0 or i + 1 == total_completed_lessons:
            # create an avg for that rank and add it to a list
            # since of list equal to total number of ranks students has completed + plus current
            if len(current_rank_rates) == 0:
                avg_rates.append(0)
            else:
                avg_rates.append(sum(current_rank_rates) / len(current_rank_rates))
            # print(len(current_rank_rates))
            # Since lesson completion time = NextLessonTime - currentLessonTime
            # to get the time spent on every fifth lesson we need to count 6-5
            # rest the list to contain the next lesson
            current_rank_rates = [lessons[i]]
        else:
            current_rank_rates.append(lessons[i])
    return avg_rates


def create_student_object_dict(student_dates_dict):
    """

    :param student_dates_dict:
    :return:
    """
    student_obj_dict = {}
    for key in student_dates_dict:
        if student_dates_dict[key] is not None:
            if len(student_dates_dict[key]) != 0:
                student_obj_dict[key] = Student(student_dates_dict[key], key)
    return student_obj_dict


# reads or writes from/to JSON file depending on if the optional pram student_data is present
def IO_JSON(file_name, *student_data):
    """

    :param file_name:
    :param student_data:
    :return:
    """
    if student_data:
        print("writing to json")
        with open(file_name + ".json", "w") as write_file:
            json.dump(student_data, write_file, indent=4)  # indent = 4 to format json to match to python syntax
    else:
        print("reading from json")
        with open(file_name) as read_file:
            return json.load(read_file)


# Converts object to dict format, since we cant serialize custom objects in Python
def object_to_dict_map(student_object):
    """

    :param student_object:
    :return:
    """
    key = student_object.name
    members_dict = {
        "name": student_object.name,
        "dates": [str(lesson_date.date().strftime("%m/%d/%y")) for lesson_date in student_object.completion_dates],
        "lessons": student_object.lesson_completion_rates,
        "rank": student_object.max_rank,
        "average completion rate": student_object.average_completion_rate_per_rank,
        "time spent per rank": student_object.time_spent_per_rank,
        "rank completion dates": [str(rank_date.date().strftime("%m/%d/%y"))
                                  for rank_date in student_object.rank_completion_dates]
    }
    return key, members_dict


# Converts dict entry back to Student object format
def dict_entry_to_object_map(student_dict, key):
    """

    :param student_dict:
    :param key:
    :return:
    """
    student_out = Student(student_dict[key]["dates"], key)
    return student_out


def to_student_object_dict(json_dict):
    """

    :param json_dict:
    :return:
    """
    students_obj_dict = {}
    for key_json in json_dict:
        students_obj_dict[key_json] = dict_entry_to_object_map(json_dict, key_json)
    return students_obj_dict


def to_json_dates_dict(students_dict):
    """

    :param students_dict:
    :return:
    """
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
    average_completion_rate_per_rank = []
    rank_completion_dates = []
    time_spent_per_rank = []

    def __init__(self, dates, student_name):
        """

        :param dates:
        :param student_name:
        """
        self.name = student_name
        self.completion_dates = convert_to_datetime(dates)
        self.lesson_completion_rates = calculate_rates(self.completion_dates)
        self.max_rank = get_max_rank(len(self.completion_dates))
        self.average_completion_rate_per_rank = calculate_average_rate_per_rank(self.lesson_completion_rates)
        time_per_rank, rank_dates = calculate_times_and_dates_per_rank(self.lesson_completion_rates,
                                                                       self.completion_dates)
        self.time_spent_per_rank = time_per_rank
        self.rank_completion_dates = rank_dates

# Move to example file
"""
# Some test code for the functions
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
IO_JSON("students", students_json)
convert_to_obj_dict_test = IO_JSON("students.json")
convert_to_obj_dict_test = convert_to_obj_dict_test[0]
test = {}
for key_json in convert_to_obj_dict_test:
    test[key_json] = dict_entry_to_object_map(convert_to_obj_dict_test, key_json)
"""

