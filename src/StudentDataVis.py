from datetime import datetime, date
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sb
import os
import sys

# PATH
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath("C:\projects\MCDataVis\StudentObjectSerializer.py")),
                                'lib'))
import StudentObjectSerializer as sos

del sys.path[0], sys, os


def calc_avg(rates, total):
    return sum(rates) / total


def variance(student_data):
    n = len(student_data)
    x_bar = calc_avg(student_data, n)
    s_2 = sum([((x - x_bar) ** 2) / n for x in student_data])
    return s_2


def standard_deviation(student_data):
    return np.sqrt(variance(student_data))


def guass(u, sigma, x):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.power(np.e, np.power((-1 * (1 / 2) * ((x - u) / sigma)), 2))


# settings for all plots
plt.style.use('seaborn')
mc_purple = '#8032ed'
mc_blue = '#05cacc'

# Collection of ranks (ordered)
ranks = ["recruit", "guardian", "watchmen", "defender", "ranger", "vigilante", "challenger", "superhero"]
# load in student objects to visualize
student_obj_dict = {}
student_obj_dict = sos.to_student_object_dict(sos.IO_JSON("students.json")[0])

# Time for plots
# Test Student name = "Aaron Prem"

student_name = 'Logan Laney'
students_comp_rates = student_obj_dict['Logan Laney'].lesson_completion_rates

# Convert into function
avg_rates = []

number_of_completed_courses = len(student_obj_dict[student_name].lesson_completion_rates)
current_rank_rates = []

for i in range(0, number_of_completed_courses):
    # 1 rank = 5 lesson so the avg lesson per rank comp  time = sum(lessonRates)/5
    # check if at 5th lesson or at the end of the list (aka current rank in time)
    if i % 5 == 0 and i != 0 or i + 1 == number_of_completed_courses:
        # create an avg for that rank and add it to a list
        # since of list equal to total number of ranks students has completed + plus current
        avg_rates.append(calc_avg(current_rank_rates, len(current_rank_rates)))
        # print(len(current_rank_rates))
        # Since lesson completion time = NextLessonTime - currentLessonTime
        # to get the time spent on every fifth lesson we need to count 6-5
        # rest the list to contain the next lesson
        current_rank_rates = [students_comp_rates[i]]
    else:
        current_rank_rates.append(students_comp_rates[i])
# convert to function
# same as above but sums up all lesson rates in a rank and adds that time to a list
# gives you the total time spent per rank
time_per_rank = []
date_per_rank = []
current_rank_rates_2 = []
for x in range(0, number_of_completed_courses):
    if x % 5 == 0 and x != 0 or x + 1 == number_of_completed_courses:
        time_per_rank.append(sum(current_rank_rates_2))
        date_per_rank.append(student_obj_dict['Logan Laney'].completion_dates[x])
        # print(len(current_rank_rates_2))
        current_rank_rates_2 = [students_comp_rates[x]]
    else:
        current_rank_rates_2.append(students_comp_rates[x])
print(len(time_per_rank))
print(len(date_per_rank))
# Student stats
avg_lesson_time = calc_avg(students_comp_rates, number_of_completed_courses)
avg_rank_time = calc_avg(current_rank_rates, len(current_rank_rates))
most_time_lesson = max(students_comp_rates)
most_time_rank = max(time_per_rank)
most_time_rank_name = ranks[time_per_rank.index(max(time_per_rank))]

fig_student, axs_student = plt.subplots(2, 3, figsize=(10, 4))

# Y: avg completion rate per rank, X: rank, Type: scatter
names = ranks[:len(avg_rates)]
axs_student[1, 0].scatter(names, avg_rates, color=mc_blue)
axs_student[1, 0].plot(names, avg_rates, color=mc_purple)
# Y: completion time per course, X: months
axs_student[1, 1].plot(student_obj_dict[student_name].completion_dates[:len(students_comp_rates)], students_comp_rates,
                       color=mc_purple)
axs_student[1, 1].scatter(student_obj_dict[student_name].completion_dates[:len(students_comp_rates)],
                          students_comp_rates,
                          color=mc_blue)
# Generate line to mark the time when lockdown started
COVID_point = [datetime.strptime("3/1/20", '%m/%d/%y')] * 55
time_range = range(0, 55)
axs_student[1, 1].plot(COVID_point, time_range, '-.', color=mc_blue)
# stats pages, aka two butchered plots :(
axs_student[0, 0].set_title("Average Completion rates for Ranks and Lessons")
axs_student[0, 0].axis('off')
axs_student[0, 0].text(.5, .6, "Avg Time Per Lesson: " + str(int(avg_lesson_time)) + " Days",
                       horizontalalignment="center",
                       verticalalignment="center", size=20, color=mc_purple)
axs_student[0, 0].text(.5, .4, "Avg Time Per rank: " + str(int(calc_avg(time_per_rank, len(time_per_rank)))) + " Days",
                       horizontalalignment="center",
                       verticalalignment="center", size=20, color=mc_purple)
axs_student[0, 1].axis('off')
axs_student[0, 1].set_title("Longest Completion rate for Ranks and Lessons")
axs_student[0, 1].axis('off')
axs_student[0, 1].text(.5, .7, "Current Rank: " + student_obj_dict[student_name].max_rank, horizontalalignment="center",
                       verticalalignment="center", size=20, color=mc_blue)
axs_student[0, 1].text(.5, .5,
                       "Most time spent at rank : " + most_time_rank_name + " for " + str(most_time_rank) + " days",
                       horizontalalignment="center",
                       verticalalignment="center", size=20, color=mc_blue)
axs_student[0, 1].text(.5, .3,
                       "Most time spent at lesson : " + str(most_time_lesson) + " days",
                       horizontalalignment="center",
                       verticalalignment="center", size=20, color=mc_blue)
# Set labels and titles
fig_student.suptitle(student_name + " Stats")
# Student subgraph of Rank completion per rank labels
axs_student[1, 0].set_title("AVG Lesson Completion rate per Rank")
axs_student[1, 0].set(xlabel="Ranks", ylabel="Rate (days)")
# Student subgraph of lesson over time labels
axs_student[1, 1].set_title("Lesson Completion Rate per Date")
axs_student[1, 1].set(xlabel="Dates", ylabel="Rate (days)")
axs_student[1, 1].annotate('Lockdown Date', xy=(datetime.strptime("3/1/20", '%m/%d/%y'), 45))
# Rank comp rate timeline
axs_student[1, 2].scatter(date_per_rank, time_per_rank)
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
plt.bar(max_ranks_dict.keys(), max_ranks_dict.values(), color=mc_purple)
plt.show()

# number of students
all_comp_rates = []
for key in student_obj_dict:
    all_comp_rates = all_comp_rates + student_obj_dict[key].lesson_completion_rates
print(all_comp_rates)
print(max(all_comp_rates))
all_comp_rates = [i for i in all_comp_rates if i != 0]
all_comp_rates = [i for i in all_comp_rates if i <= 100]
print(all_comp_rates)
print(len(all_comp_rates))
val_test = len(all_comp_rates)
fig, axs = plt.subplots(1, 2)
N, bins, patches = axs[0].hist(all_comp_rates, bins=100)
fracs = N / N.max()
norm = colors.Normalize(fracs.min(), fracs.max())
for this_frac, this_patch in zip(fracs, patches):
    color = plt.cm.viridis(norm(this_frac))
    this_patch.set_facecolor(color)
all_comp_rates_u = np.mean(all_comp_rates)
all_comp_rates_sigma = np.std(all_comp_rates)
data = [guass(all_comp_rates_u, all_comp_rates_sigma, i) for i in all_comp_rates]
tick_range = np.arange(0, max(all_comp_rates), 5)
axs[0].set_xticks(tick_range)
data.sort()
all_comp_rates.sort()
axs[1].plot(data, all_comp_rates)
plt.show()
