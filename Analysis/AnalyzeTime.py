"""
The occurrence time of each dialogue

Structure of dial.txt:
obj{"id": id, "dial": dial}
dial[{"time": time, "speaker": speaker, "content": content}, ...]
"""

import Utils
import json
import matplotlib.pylab as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import math
from collections import Counter
import csv
from scipy import interpolate

font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc', size=6)
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

source_path = "../DataSet/"
data_set = "dial.txt"
data_dgn = "dial_dgn.txt"
data_no_dgn = "dial_no_dgn.txt"
data_no_rst = "dial_no_rst.txt"

# get occurrence time distribution
# time_group = {'morning(6-12)': 0, 'afternoon(12-19)': 0, 'evening(19-23)': 0, 'night(23-6*)': 0}
# with open(source_path + data_set, "r") as in_file:
#     for line in in_file.readlines():
#         obj = json.loads(line)
#         if len(obj["dial"]) > 0:
#             tim = Utils.get_time_group(obj["dial"][0]["time"][1])
#             if tim not in time_group:
#                 time_group[tim] = 0
#             time_group[tim] += 1
# print(time_group)
# labels = [tim[0] for tim in time_group.items()]
# plt.bar(np.arange(4), [tim[1] for tim in time_group.items()])
# plt.xticks(np.arange(4), labels)
# plt.xlabel('time')
# plt.ylabel('number')
# plt.title('distribution of occurrence times of each dialogue')
# plt.show()

# gender distribution over time
# time_group_male = {'morning(6-12)': 0, 'afternoon(12-19)': 0, 'evening(19-23)': 0, 'night(23-6*)': 0}
# time_group_female = {'morning(6-12)': 0, 'afternoon(12-19)': 0, 'evening(19-23)': 0, 'night(23-6*)': 0}
# time_group_unknown = {'morning(6-12)': 0, 'afternoon(12-19)': 0, 'evening(19-23)': 0, 'night(23-6*)': 0}
# with open(source_path + data_set, "r") as in_file:
#     for line in in_file.readlines():
#         obj = json.loads(line)
#         if len(obj["dial"]) > 0:
#             gender = "未知"
#             if obj["dial"][-1]["speaker"] == "Robot":
#                 rst = json.loads(obj["dial"][-1]["content"])
#                 gender = rst["attachment_dict"]["gender"]
#             else:
#                 for _, dial in enumerate(obj["dial"]):
#                     if "性别" in dial["content"]:
#                         gender = obj["dial"][_ + 1]["content"]
#             tim = Utils.get_time_group(obj["dial"][0]["time"][1])
#             if gender == "男":
#                 if tim not in time_group_male:
#                     time_group_male[tim] = 0
#                 time_group_male[tim] += 1
#             if gender == "女":
#                 if tim not in time_group_female:
#                     time_group_female[tim] = 0
#                 time_group_female[tim] += 1
#             if gender == "未知":
#                 if tim not in time_group_unknown:
#                     time_group_unknown[tim] = 0
#                 time_group_unknown[tim] += 1
# labels = [num[0] for num in time_group_male.items()]
# tg_male = [num[1] for num in time_group_male.items()]
# tg_female = [num[1] for num in time_group_female.items()]
# ratio = [num/tg_female[_] for _, num in enumerate(tg_male)]
# bar_width = 0.3
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.bar(np.arange(len(tg_male)), tg_male, label='male', alpha=0.8, width=bar_width)
# ax1.bar(np.arange(len(tg_female)) + bar_width, tg_female, label='female', alpha=0.8, width=bar_width)
# ax1.set_xlabel('time')
# ax1.set_ylabel('number')
# ax1.set_title('Comparison between male and female dialogues\nand their ratios at different time')
# plt.xticks(np.arange(len(tg_male))+bar_width/2, labels, fontproperties=font)
# for _, num_dgn in enumerate(tg_male):
#     plt.text(_-bar_width*0.5, num_dgn+1, '%s' % num_dgn)
#     plt.text(_+bar_width*0.5, tg_female[_]+1, '%s' % tg_female[_])
# ax1.set_ylim(0, )
# ax1.legend(loc=2)
# ax2 = ax1.twinx()
# ax2.plot(np.arange(len(labels))+bar_width/2, ratio, 'r*', label='ratio between the number of\n the male and the female')
# ax2.set_ylabel('ratio')
# ax2.set_ylim(0.4, 1.6)
# for _, ra in enumerate(ratio):
#     plt.text(_+bar_width/2, ra+0.03, '%.2f' % ra)
# ax2.legend()
# plt.show()


# get gender xxx cross dict - xxx : span, time, age, description
def cross_anl_span(cross_group, data_path, span_group, cross_type):
    span_group_arr = {}
    for cg in cross_group:
        span_group_arr[cg] = {}
        for gg in span_group:
            span_group_arr[cg][gg] = 0
    span_group_arr["unknown"] = {}
    for gg in span_group:
        span_group_arr["unknown"][gg] = 0
    with open(data_path, "r") as data_file:
        for li in data_file.readlines():
            obj = json.loads(li)
            if len(obj["dial"]) < 3:
                continue
            else:
                # get cross and des_cat
                span = Utils.get_cross('span', obj)
                if span not in span_group:
                    continue
                cross = Utils.get_cross(cross_type, obj)
                if cross_type == "description":
                    for des in cross:
                        for cg in cross_group:
                            if des == cg and des is not 'unknown':
                                span_group_arr[des][span] += 1
                        if des == "unknown":
                            span_group_arr['unknown'][span] += 1
                else:
                    for cg in cross_group:
                        if cross == cg:
                            span_group_arr[cross][span] += 1
                    if cross == "unknown":
                        span_group_arr['unknown'][span] += 1
    return span_group_arr


# plot cross
def plot_cross_span(span_group_arr, span_group, cross_group, cross_type, title, x_label):
    labels = [num[0] for num in span_group_arr[cross_group[0]].items()]
    ac_count = {}  # count of each dc
    for dc in span_group:
        ac_count[dc] = sum([span_group_arr[cg][dc] for cg in span_group_arr])+1
    dc_arr = {}
    for cg in cross_group:
        dc_arr[cg] = [num[1] for num in span_group_arr[cg].items()]
    bar_width = 0.8 / len(cross_group)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for _, cg in enumerate(cross_group):
        if cross_type == 'age':
            ax1.bar(np.arange(len(dc_arr[cg])) + bar_width * _, dc_arr[cg],
                    label=Utils.age_decode[cg], alpha=0.8, width=bar_width)
        elif cross_type == "gender":
            ax1.bar(np.arange(len(dc_arr[cg])) + bar_width * _, dc_arr[cg],
                    label=Utils.gender_decode[cg], alpha=0.8, width=bar_width)
        elif cross_type == "description":
            ax1.bar(np.arange(len(dc_arr[cg])) + bar_width * _, dc_arr[cg],
                    label=Utils.des_decode[cg], alpha=0.8, width=bar_width)
        else:
            ax1.bar(np.arange(len(dc_arr[cg])) + bar_width * _, dc_arr[cg],
                    label=cg, alpha=0.8, width=bar_width)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel('number')
    ax1.set_title(title)
    plt.xticks(np.arange(len(dc_arr[cross_group[0]])) + bar_width * (len(span_group_arr) - 1) / 2, labels,
               fontproperties=font)
    for _, num in enumerate(dc_arr[cross_group[0]]):
        for __, cg in enumerate(cross_group):
            if cross_type == "description":
                plt.text(_ + bar_width * (__ - 0.5), dc_arr[cg][_] + 1,
                         Utils.des_decode[cg] + '\n%d(%.f' % (
                             dc_arr[cg][_], dc_arr[cg][_] / list(ac_count.items())[_][1] * 100) + "%)",
                         fontproperties=font)
            else:
                plt.text(_ + bar_width * (__ - 0.5), dc_arr[cg][_] + 1,
                         '\n%d(%.f' % (dc_arr[cg][_], dc_arr[cg][_] / list(ac_count.items())[_][1] * 100) + "%)",
                         fontproperties=font)
    ax1.set_ylim(0, )
    # ax1.set_xlim(-0.5, )
    if cross_type is not "description":
        ax1.legend()
    plt.show()


ac_group = {'time': Utils.time_group, 'span': Utils.span_group, 'age': Utils.age_group,
            'gender': Utils.gender_group, 'description': Utils.des_cate}

if __name__ == '__main__':
    cross_type = 'description'  # time, span, age, gender, description
    span_gro = Utils.span_group
    span_cross_group_arr = cross_anl_span(ac_group[cross_type], source_path + data_set, span_gro, cross_type=cross_type)
    print(span_cross_group_arr)
    plot_cross_span(span_cross_group_arr, span_gro, ac_group[cross_type], cross_type=cross_type,
                    title='Comparison between dialogues of different ' + cross_type + '\naccording to span',
                    x_label='')
