from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import os
import sys

# PATH for SOS, so we can read in the JSON obj data
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


def gauss(u, sigma, x):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.power(np.e, np.power((-1 * (1 / 2) * ((x - u) / sigma)), 2))

def generate_report_card(key,dict):

    student = dict[key]
    comp_rates = student.lesson_completion_rates
    comp_dates = student.completion_dates
    rank = student.max_rank
    name = student.name

# settings for all plots
plt.style.use('seaborn')
mc_purple = '#8032ed'
mc_blue = '#05cacc'

# Collection of ranks (ordered)
ranks = ["recruit", "guardian", "watchmen", "defender", "ranger", "vigilante", "challenger", "superhero"]
# load in student objects to visualize
student_obj_dict = {}
student_obj_dict = sos.to_student_object_dict(sos.IO_JSON("students.json")[0])


student_name = 'Rukshik Nelluri'
students_comp_rates = student_obj_dict[student_name].lesson_completion_rates
students_comp_dates = student_obj_dict[student_name].completion_dates

number_of_completed_courses = len(students_comp_rates)
time_per_rank = student_obj_dict[student_name].time_spent_per_rank
avg_rates = student_obj_dict[student_name].average_completion_rate_per_rank

avg_lesson_time = calc_avg(students_comp_rates, number_of_completed_courses)
avg_rank_time = calc_avg(time_per_rank, len(time_per_rank))
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
date_labels = [date.strftime('%m/%d/%y') for date in
               student_obj_dict[student_name].completion_dates[:len(students_comp_rates)]]
axs_student[1, 1].set_xticklabels(date_labels, rotation=60)

# stats pages, aka two butchered plots :(
axs_student[0, 0].set_title("Average Completion rates for Ranks and Lessons", size=20, color=mc_purple)
axs_student[0, 0].axis('off')
axs_student[0, 0].text(.5, .9, "Avg Time Per Lesson: " + str(int(avg_lesson_time)) + " Days",
                       horizontalalignment="center",
                       verticalalignment="center", size=20, color=mc_purple)
axs_student[0, 0].text(.5, .7, "Avg Time Per rank: " + str(int(calc_avg(time_per_rank, len(time_per_rank)))) + " Days",
                       horizontalalignment="center",
                       verticalalignment="center", size=20, color=mc_purple)
axs_student[0, 1].axis('off')
axs_student[0, 2].set_title("Longest Completion times for Ranks and Lessons", size=20, color=mc_blue)
axs_student[0, 2].axis('off')
axs_student[0, 2].text(.5, .9, "Current Rank: " + student_obj_dict[student_name].max_rank, horizontalalignment="center",
                       verticalalignment="center", size=20, color=mc_blue)
axs_student[0, 2].text(.5, .7,
                       "Most time spent at rank: " + most_time_rank_name + " for " + str(most_time_rank) + " days",
                       horizontalalignment="center",
                       verticalalignment="center", size=20, color=mc_blue)
axs_student[0, 2].text(.5, .5,
                       "Most time spent at lesson: " + str(most_time_lesson) + " days",
                       horizontalalignment="center",
                       verticalalignment="center", size=20, color=mc_blue)
axs_student[0, 2].axis('off')
# Set labels and titles
# Student subgraph of Rank completion per rank labels
axs_student[1, 0].set_title("Average Lesson Completion rate per Rank")
axs_student[1, 0].set(xlabel="Ranks", ylabel="Rate (days)")
# Student subgraph of lesson over time labels
# Generate line to mark the time when lockdown started
# COVID_point = [datetime.strptime("3/1/20", '%m/%d/%y')] * 55
# time_range = range(0, 55)
# axs_student[1, 1].plot(COVID_point, time_range, '-.', color=mc_blue)
axs_student[1, 1].set_title("Lesson Completion Rate per Date")
axs_student[1, 1].set(xlabel="Dates", ylabel="Rate (days)")
# axs_student[1, 1].annotate('Lockdown Date', xy=(datetime.strptime("3/1/20", '%m/%d/%y'), 45))
# Rank comp rate timeline
axs_student[1, 2].set_title("Time spent at each rank")
axs_student[1, 2].scatter(names, time_per_rank, color=mc_blue)
axs_student[1, 2].plot(names, time_per_rank, color=mc_purple)
axs_student[1, 2].set(xlabel="Ranks", ylabel="Days spent on rank")

fig_student.suptitle(student_name + " Report Card", size=20, color='grey')
fig_student.set_size_inches(16, 16)
#plt.savefig(student_name + "ReportCard.png", dpi=100)
plt.show()

# For all students
# Need:
# max ranks for all students dict {"rank", number of students at rank}
# plot type Bar Y: no of students, X: ranks
# Histogram of lesson completion time
# avg of above plot but for all students completion of ranks

max_ranks_dict = {"recruit": 0, "guardian": 0, "watchmen": 0, "defender": 0, "ranger": 0, "vigilante": 0,
                  "challenger": 0, "superhero": 0}
lesson_dist_ranks_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [],
                          6: [], 7: []}
lesson_dates_dict = {}  # key is date, value is int with number of lessons in that date
# we only care about months && years so if lesson is in same comp date mm/yy then plus 1 to val
lesson_dates = []
all_comp_rates = []
# loops through students
for key in student_obj_dict.keys():
    all_comp_rates = all_comp_rates + student_obj_dict[key].lesson_completion_rates  # for histogram all lessons
    max_ranks_dict[student_obj_dict[key].max_rank] += 1  # for bar all ranks
    print(student_obj_dict[key].name)
    for curr_date_index in range(0, len(student_obj_dict[key].completion_dates)):

        lesson_date = student_obj_dict[key].completion_dates[curr_date_index]
        # print("stripped date: " + lesson_date.strftime("%m/%y") + " og date: " + str(lesson_date))
        stripped_date = datetime.strptime(lesson_date.strftime("%m/%y"), "%m/%y")
        # print(type(stripped_date))
        # print(str(stripped_date))
        # replace with lesson date for daily instead of monthly
        if lesson_date not in lesson_dates:
            lesson_dates.append(lesson_date)
            lesson_dates_dict[lesson_date] = 1
        else:
            lesson_dates_dict[lesson_date] += 1
    for curr_lesson_index in range(0, len(student_obj_dict[key].lesson_completion_rates)):
        if curr_lesson_index > 0:
            lesson_dist_ranks_dict[int(np.ceil(curr_lesson_index / 5)) - 1].append(
                student_obj_dict[key].lesson_completion_rates[curr_lesson_index])
        else:
            lesson_dist_ranks_dict[0].append(student_obj_dict[key].lesson_completion_rates[curr_lesson_index])
plt.bar(max_ranks_dict.keys(), max_ranks_dict.values(), color=mc_purple)
plt.show()
lesson_dates.sort()
print(lesson_dates)
print("check list and dict: " + str(len(lesson_dates_dict)) + " and " + str(len(lesson_dates)))
lesson_totals = []
for i in range(0,len(lesson_dates)):
    lesson_totals.append(lesson_dates_dict[lesson_dates[i]])
print(len(lesson_totals))
plt.scatter(lesson_dates,lesson_totals)
# stripping outliers low and high
# turn this into a function as well pramms outlier lims and list to strip
all_comp_rates = [i for i in all_comp_rates if i != 0]
all_comp_rates = [i for i in all_comp_rates if i <= 100]

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
data = [gauss(all_comp_rates_u, all_comp_rates_sigma, i) for i in all_comp_rates]
tick_range = np.arange(0, max(all_comp_rates), 5)
axs[0].set_xticks(tick_range)
data.sort()
all_comp_rates.sort()
axs[1].plot(data, all_comp_rates)
plt.show()
print(lesson_dist_ranks_dict[7])
for rank in lesson_dist_ranks_dict:
    print(ranks[rank])
    print("stats")
    print("min: " + str(min(lesson_dist_ranks_dict[rank])))
    print("max: " + str(max(lesson_dist_ranks_dict[rank])))
    print("mean: " + str(calc_avg(lesson_dist_ranks_dict[rank], len(lesson_dist_ranks_dict[rank]))))
    print("std: " + str(standard_deviation(lesson_dist_ranks_dict[rank])))
    print("variance: " + str(variance(lesson_dist_ranks_dict[rank])))
    print("median: " + str(np.median(lesson_dist_ranks_dict[rank])))
    print("total comp lessons: " + str(len(lesson_dist_ranks_dict[rank])))

# N, bins, patches = plt.hist(lesson_dist_ranks_dict[rank], bins="auto")
# plt.show()
