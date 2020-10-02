from datetime import datetime, date
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath("C:\projects\MCDataVis\StudentObjectSerializer.py")),
                                'lib'))
import StudentObjectSerializer as sos

del sys.path[0], sys, os

# Collection of ranks (ordered)
ranks = ["recruit", "guardian", "watchmen", "defender", "ranger", "vigilante", "challenger", "superhero"]

student_obj_dict = {}
student_obj_dict = sos.to_student_object_dict(sos.IO_JSON("students.json")[0])

# Time for plots
# Test Student name = "Aaron Prem"

student_name = 'Aaron Prem'

students_comp_rates = student_obj_dict['Aaron Prem'].lesson_completion_rates


def avg_comp_rate_rank(rates, total):
    return sum(rates) / total


avg_rates = []

number_of_completed_courses = len(student_obj_dict[student_name].lesson_completion_rates)
current_rank_rates = []

for i in range(0, number_of_completed_courses):
    if i % 5 == 0 and i != 0 or i + 1 == number_of_completed_courses:
        avg_rates.append(avg_comp_rate_rank(current_rank_rates, len(current_rank_rates)))
        # print(len(current_rank_rates))
        current_rank_rates = [students_comp_rates[i]]
    else:
        current_rank_rates.append(students_comp_rates[i])

plt.style.use('seaborn')
mc_purple = '#8032ed'
mc_blue = '#05cacc'
# Y: avg completion rate per rank, X: rank, Type: scatter
names = ranks[:len(avg_rates)]
plt.scatter(names, avg_rates, color=mc_blue)
plt.plot(names, avg_rates, color=mc_purple)
plt.show()
# Y: completion time per course, X: months
plt.plot(student_obj_dict['Aaron Prem'].completion_dates[:len(students_comp_rates)], students_comp_rates,
         color=mc_purple)
plt.scatter(student_obj_dict['Aaron Prem'].completion_dates[:len(students_comp_rates)], students_comp_rates,
            color=mc_blue)

COVID_point = [datetime.strptime("3/1/20", '%m/%d/%y')] * 55
time_range = range(0, 55)
plt.plot(COVID_point, time_range, '-.', color=mc_blue)
plt.ylim(-2, 50)
plt.show()

# For all students

# Need:
# max ranks for all students dict {"rank", number of students at rank}
# plot type Bar Y: no of students, X: ranks
# Histogram of lesson completion time
# avg of above plot but for all students completion of ranks

max_ranks_dict = {"recruit": 0, "guardian": 0, "watchmen": 0, "defender": 0, "ranger": 0, "vigilante": 0,
                  "challenger": 0, "superhero": 0}

for key in student_obj_dict.keys():
    max_ranks_dict[student_obj_dict[key].max_rank] += 1
print(max_ranks_dict)
plt.bar(max_ranks_dict.keys(), max_ranks_dict.values(), color=mc_purple)
plt.show()
