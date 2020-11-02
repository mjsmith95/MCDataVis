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

# settings for all plots
plt.style.use('seaborn')
mc_purple = '#8032ed'
mc_blue = '#05cacc'

# Collection of ranks (ordered)
ranks = ["recruit", "guardian", "watchmen", "defender", "ranger", "vigilante", "challenger", "superhero"]


def calc_avg(rates: list, total: int) -> int:
    """
    Returns the average (mean) value given a range and total.
    :param total: int
    :param rates: list
    """
    return sum(rates) / total


def variance(student_data: list) -> float:
    """
    Returns the variance of the passed in range.
    :param student_data: list
    :return: list
    """
    n = len(student_data)
    x_bar = calc_avg(student_data, n)
    s_2 = sum([((x - x_bar) ** 2) / n for x in student_data])
    return s_2


def standard_deviation(student_data: list) -> float:
    """
    Returns the standard deviation of the input set.
    :param student_data: list
    :return: float
    """
    return np.sqrt(variance(student_data))


def gauss(u: float, sigma: float, x: float) -> float:
    """
    This function models a Gaussian distribution. Run this function through a loop to generate a series to plot.
    :param u: float
    :param sigma: float
    :param x: float
    :return: float
    """
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.power(np.e, np.power((-1 * (1 / 2) * ((x - u) / sigma)), 2))


def strip_outliers(range_to_check, max_element=None, min_element=None) -> list:
    """
    Returns a list with all integers removed, according to set bounds (upper = max_element, lower = min_element).
    :param range_to_check: list
    :param max_element: int, if let as none function will not strip a max outlier
    :param min_element: int, same case as max, None will result in no values being removed.
    :return: list
    """
    stripped_range = range_to_check
    if max_element is not None:
        stripped_range = [i for i in range_to_check if i < max_element]
    if min_element is not None:
        stripped_range = [i for i in range_to_check if i > min_element]
    return stripped_range


def generate_report_card(key, student_dict, **kwargs) -> None:
    """
    Generates a student report card, given student name as key, and dict containing said student object.
    Optional prams: show_covid, which draws a line on plot 2, indicating the covid lock-down start date.
    And save_fig, saves the figure to the project folder.
    :param key: string
    :param student_dict: dict
    :param kwargs: bool, bool
    :return: None
    """
    student = student_dict[key]
    comp_rates = student.lesson_completion_rates
    # TODO look at all completion dates, and see if a visual can be created.
    # comp_dates = student.completion_dates
    rank = student.max_rank
    name = student.name

    number_of_completed_courses = len(comp_rates)
    time_per_rank = student_dict[key].time_spent_per_rank
    avg_rates = student_dict[key].average_completion_rate_per_rank

    avg_lesson_time = calc_avg(comp_rates, number_of_completed_courses)
    avg_rank_time = calc_avg(time_per_rank, len(time_per_rank))
    most_time_lesson = max(comp_rates)
    most_time_rank = max(time_per_rank)
    most_time_rank_name = ranks[time_per_rank.index(max(time_per_rank))]

    fig_student, axs_student = plt.subplots(2, 3, figsize=(10, 4))
    names = ranks[:len(avg_rates)]
    axs_student[0, 0].set_title("Average Completion rates for Ranks and Lessons", size=20, color=mc_purple)
    axs_student[0, 0].axis('off')
    axs_student[0, 0].text(.5, .9, "Avg Time Per Lesson: " + str(int(avg_lesson_time)) + " Days",
                           horizontalalignment="center",
                           verticalalignment="center", size=20, color=mc_purple)
    axs_student[0, 0].text(.5, .7,
                           "Avg Time Per rank: " + str(avg_rank_time) + " Days",
                           horizontalalignment="center",
                           verticalalignment="center", size=20, color=mc_purple)

    axs_student[0, 1].axis('off')

    axs_student[0, 2].set_title("Longest Completion times for Ranks and Lessons", size=20, color=mc_blue)
    axs_student[0, 2].axis('off')
    axs_student[0, 2].text(.5, .9, "Current Rank: " + rank,
                           horizontalalignment="center",
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

    axs_student[1, 0].set_title("Average Lesson Completion rate per Rank")
    axs_student[1, 0].set(xlabel="Ranks", ylabel="Rate (days)")
    axs_student[1, 0].scatter(names, avg_rates, color=mc_blue)
    axs_student[1, 0].plot(names, avg_rates, color=mc_purple)
    # Y: completion time per course, X: months
    axs_student[1, 1].plot(student_dict[key].completion_dates[:len(comp_rates)],
                           comp_rates,
                           color=mc_purple)
    axs_student[1, 1].scatter(student_dict[key].completion_dates[:len(comp_rates)],
                              comp_rates,
                              color=mc_blue)
    date_labels = [date.strftime('%m/%d/%y') for date in
                   student_dict[key].completion_dates[:len(comp_rates)]]
    axs_student[1, 1].set_xticklabels(date_labels, rotation=60)
    # Generate line to mark the time when lock-down started
    if "show_covid" in kwargs and kwargs["show_covid"] == True:
        COVID_point = [datetime.strptime("3/1/20", '%m/%d/%y')] * 55
        time_range = range(0, 55)
        axs_student[1, 1].plot(COVID_point, time_range, '-.', color=mc_blue)
        axs_student[1, 1].annotate('Lock-down Date', xy=(datetime.strptime("3/1/20", '%m/%d/%y'), 45))

    axs_student[1, 1].set_title("Lesson Completion Rate per Date")
    axs_student[1, 1].set(xlabel="Dates", ylabel="Rate (days)")
    # Rank comp rate timeline
    axs_student[1, 2].set_title("Time spent at each rank")
    axs_student[1, 2].scatter(names, time_per_rank, color=mc_blue)
    axs_student[1, 2].plot(names, time_per_rank, color=mc_purple)
    axs_student[1, 2].set(xlabel="Ranks", ylabel="Days spent on rank")

    fig_student.suptitle(name + " Report Card", size=20, color='grey')
    fig_student.set_size_inches(16, 16)
    if "save_fig" in kwargs and kwargs["save_fig"] == True:
        plt.savefig(name + "ReportCard.png", dpi=100)
    plt.show()


def generate_rank_bar_graph(student_dict: dict, *save_fig) -> None:
    """
    Generates a bar graph displaying the total number of students at each rank.
    Optional params: save_fig saves the figure to the project folder.
    :param student_dict: dict
    :param save_fig: bool
    :return: None
    """
    max_ranks_dict = {"recruit": 0, "guardian": 0, "watchmen": 0, "defender": 0, "ranger": 0, "vigilante": 0,
                      "challenger": 0, "superhero": 0}
    # counts the number of students at each rank, mapping it to a dict indexed by those ranks
    for key in student_dict.keys():
        max_ranks_dict[student_dict[key].max_rank] += 1  # for bar all ranks
    plt.title("Number of Students in each rank", color=mc_blue, size=15)
    plt.xlabel("Ranks (Ordered)", size=10)
    plt.ylabel("Number of Students", size=10)
    plt.bar(max_ranks_dict.keys(), max_ranks_dict.values(), color=mc_purple)
    if save_fig:
        plt.savefig("StudentsPerRank.png", dpi=100)
    plt.show()


def generate_lesson_timeline(student_dict, **kwargs) -> None:
    """
    Displays a scatter plot of all completed lessons over all recorded time. Can be set to a monthly or daily range.
    Optional params monthly_rate switches the range from daily to monthly, and save_fig saves the figure to the
    project folder.
    :param student_dict: dict
    :param kwargs: bool, bool
    :return: None
    """
    lesson_dates_dict = {}
    lesson_dates = []
    lesson_totals = []
    # needs alg explanation
    for key in student_dict.keys():
        for curr_date_index in range(0, len(student_dict[key].completion_dates)):
            lesson_date = student_dict[key].completion_dates[curr_date_index]
            if "monthly_rate" in kwargs and kwargs["monthly_rate"] == True:
                lesson_date = datetime.strptime(lesson_date.strftime("%m/%y"), "%m/%y")
            if lesson_date not in lesson_dates:
                lesson_dates.append(lesson_date)
                lesson_dates_dict[lesson_date] = 1
            else:
                lesson_dates_dict[lesson_date] += 1
    # Values are stored as datetime objects, Since the values were taken from a dictionary, they are no longer
    # ordered, thus we need to sort them to graph correctly.
    lesson_dates.sort()
    # generate the y axis range
    for i in range(0, len(lesson_dates)):
        lesson_totals.append(lesson_dates_dict[lesson_dates[i]])
    plt.scatter(lesson_dates, lesson_totals, color=mc_purple)
    plt.title("Timeline of Total Lessons Completed per Month", color=mc_blue, size=15)
    plt.xlabel("Date (mm/yy)", size=10)
    plt.ylabel("Number of Lessons Completed", size=10)
    if "save_fig" in kwargs:
        plt.savefig("LessonTimeline.png", dpi=100)
    plt.show()


def generate_total_lesson_distribution(student_dict, **kwargs) -> list:
    """
    Collections all lesson completion times and returns the set as a list.
    Optional params, min/max_outlier set a minim and maxim bound list will not contain values outside those bounds.
    :param student_dict: dict
    :param kwargs: int, int
    :return: list
    """
    all_completion_rates = []
    # Each students completion rate is stored as a list, we concatenate all completion rates for each student
    # into a single list and return it.
    for key in student_dict.keys():
        all_completion_rates = all_completion_rates + student_dict[key].lesson_completion_rates
    if "max_outlier" in kwargs:
        all_completion_rates = strip_outliers(all_completion_rates, max_element=kwargs["max_outlier"])
    if "min_outlier" in kwargs:
        print("hit test")

        all_completion_rates = strip_outliers(all_completion_rates, min_element=kwargs["min_outlier"])
    return all_completion_rates


def plot_color_histogram(range_to_color: list, number_of_bins: int, *save_fig: bool, **kwargs) -> None:
    """
    Generates a color gradient defined histogram, based of the passed in data.
    Optional params: show_stats adds a text box containing the mean, standard deviation and median of the
    data to the figure. Pass a string to fig_title to change the title of the plot.
    save_fig saves the figure to the project folder.
    :param range_to_color: list
    :param number_of_bins: int
    :param save_fig: bool
    :param kwargs: bool, bool, string
    :return: None
    """
    fig, axs = plt.subplots(1, 1)
    N, bins, patches = axs.hist(range_to_color, bins=number_of_bins)
    fracs = N / N.max()
    norm = colors.Normalize(fracs.min(), fracs.max())
    for this_frac, this_patch in zip(fracs, patches):
        color = plt.cm.viridis(norm(this_frac))
        this_patch.set_facecolor(color)
    tick_range = np.arange(0, max(range_to_color), 5)
    axs.set_xticks(tick_range)
    if "show_stats" in kwargs:
        mu = calc_avg(range_to_color, len(range_to_color))
        median = np.median(range_to_color)
        sigma = standard_deviation(range_to_color)
        textstr = '\n'.join((
            r'$\mu=%.2f$' % (mu,),
            r'$\mathrm{median}=%.2f$' % (median,),
            r'$\sigma=%.2f$' % (sigma,)))
        props = dict(boxstyle='round', facecolor='grey', alpha=0.5)
        axs.text(0.70, 0.95, textstr, transform=axs.transAxes, fontsize=14,
                 verticalalignment='top', bbox=props)
    if "fig_title" in kwargs:
        print(kwargs["fig_title"])
        plt.title(kwargs["fig_title"], color=mc_blue, size=15)
    else:
        plt.title("Distribution of Completed Lessons", color=mc_blue, size=15)
    plt.ylabel("Frequency (Number of Completed Lessons)", size=10)
    plt.xlabel("Grouping by Time (Total Days)", size=10)
    if save_fig:
        if "fig_title" in kwargs:
            plt.savefig(str(kwargs["fig_title"]) + ".png", dpi=100)
        else:
            plt.savefig("Histogram.png", dpi=100)
        print("saved plot")
    plt.show()


def generate_ranges_per_rank(student_dict: dict) -> dict:
    """
    Iterates through all students, mapping each student's lessons into the appropriate rank,
    and counting the total number of lessons per rank.
    :param student_dict:
    :return: dict
    """
    lesson_dist_ranks_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [],
                              6: [], 7: []}
    # key is date, value is int with number of lessons in that date
    # we only care about months && years so if lesson is in same comp date mm/yy then plus 1 to val
    # loops through students
    for key in student_dict.keys():
        for curr_lesson_index in range(0, len(student_dict[key].lesson_completion_rates)):
            if curr_lesson_index > 0:
                lesson_dist_ranks_dict[int(np.ceil(curr_lesson_index / 5)) - 1].append(
                    student_dict[key].lesson_completion_rates[curr_lesson_index])
            else:
                lesson_dist_ranks_dict[0].append(student_dict[key].lesson_completion_rates[curr_lesson_index])
    return lesson_dist_ranks_dict


def generate_rank_histogram(rank: str, student_dict: dict, **kwargs) -> None:
    """
    Displays a histogram of the completed lesson over time for a specified rank.
    Optional params: min/max_outlier set a min and max bound on a list,
    such that it will not contain values outside those bounds. show_stats adds a text box containing the mean,
    standard deviation, and median of the data to the figure.
    fig_title changes the title of the plot.
    save_fig saves the figure to the project folder.
    :param rank: str
    :param student_dict: dict
    :param kwargs: int, int, bool, bool, str
    :return: None
    """
    ranks_dict = generate_ranges_per_rank(student_dict)
    rank_key = ranks.index(rank.lower())
    title = "Distribution of completed lesson at " + rank
    print(title)
    rank_distribution = ranks_dict[rank_key]
    if "max_outlier" in kwargs:
        rank_distribution = strip_outliers(rank_distribution, max_element=kwargs["max_outlier"])
    if "min_outlier" in kwargs:
        rank_distribution = strip_outliers(rank_distribution, min_element=kwargs["min_outlier"])
    if "show_stats" in kwargs and "save_fig" in kwargs:
        plot_color_histogram(rank_distribution, "auto", True, fig_title=title, show_stats=True)
    elif "show_stats" in kwargs and "save_fig" not in kwargs:
        plot_color_histogram(rank_distribution, "auto", fig_title=title, show_stats=True)
    elif "save_fig" in kwargs:
        plot_color_histogram(rank_distribution, "auto", True, fig_title=title)
    else:
        plot_color_histogram(rank_distribution, "auto", fig_title=title)


# MOVE TO EXAMPLE FILE
# load in student objects to visualize
student_obj_dict = {}
student_obj_dict = sos.to_student_object_dict(sos.IO_JSON("students.json")[0])
# generate_report_card("Romesh Mamidi", student_obj_dict, save_fig=True, show_covid=True)
# For all students
# generate_rank_bar_graph(student_obj_dict, True)
# generate_lesson_timeline(student_obj_dict, save_fig=True, monthly_rate=True)
# all_lessons = generate_total_lesson_distribution(student_obj_dict, max_outlier=100, min_outlier=0)
# plot_color_histogram(all_lessons, 100, True, show_stats=True)
# generate_rank_histogram("watchmen", student_obj_dict, max_outlier=150, min_outlier=0, save_fig=True)

# TODO generate matrix display for ranks, in the meantime use per_rank functions
# def plot_rank_histograms(number_of_ranks, student_dict):
#     ranks_dict = generate_ranges_per_rank(student_dict)
#     if number_of_ranks % 2 == 0:
#         number_of_rows,number_of_cols = number_of_ranks
#     else:
#         number_of_rows,number_of_cols = number_of_ranks +
#     print(number_of_cols, number_of_rows)
#     if number_of_ranks == 0 or number_of_ranks >= 8:
#         return
#     elif number_of_ranks == 1:
#         print("relguar plt")
#     else:
#         rank_fig, rank_axs = plt.subplots(number_of_rows, number_of_cols, figsize=(10, 4))
#         for i in range(0, number_of_rows):
#             for j in range(0, number_of_cols):
#                 print(i * number_of_rows + j)
#
#
#                 print(ranks[i * number_of_cols + j])
#                 N, bins, patches = rank_axs[i, j].hist(ranks_dict[i * number_of_cols + j], bins='auto')
#
#                 fracs = N / N.max()
#                 norm = colors.Normalize(fracs.min(), fracs.max())
#                 for this_frac, this_patch in zip(fracs, patches):
#                     color = plt.cm.viridis(norm(this_frac))
#                     this_patch.set_facecolor(color)
#                 tick_range = np.arange(0, max(ranks_dict[i * number_of_cols + j]), 5)
#                 rank_axs[i, j].set_xticks(tick_range)
#                 rank_axs[i, j].set_title("Distribution of Completed Lessons for " + ranks[i * number_of_cols + j], color=mc_blue, size=15)
#                 #rank_axs[j,i].ylabel("Frequency (Number of Completed Lessons)", size=10)
#                 #rank_axs[j,i].xlabel("Grouping by Time (Total Days)", size=10)
#             plt.show()
#
# plot_rank_histograms(7, student_obj_dict)
