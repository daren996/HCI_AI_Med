"""
Analyze Info of Genders.

Structure of dial.txt:
obj{"id": id, "dial": dial}
dial[{"time": time, "speaker": speaker, "content": content}, ...]
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import Utils
from matplotlib.font_manager import FontProperties

font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc', size=7)
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 7

source_path = "../DataSet/"
data = "dial.txt"
data_dgn = "dial_dgn.txt"
data_no_dgn = "dial_no_dgn.txt"
data_no_rst = "dial_no_rst.txt"


# Comparison between complete and uncompleted dialogues according genders
def gender_completeness_cross():
    gender_dgn = {'男': 0, '女': 0}
    gender_no_dgn = {'男': 0, '女': 0}
    gender_no_rst = {'男': 0, '女': 0}
    with open(source_path + data_dgn, "r") as in_file:
        for line in in_file.readlines():
            obj = json.loads(line)
            rst = json.loads(obj["dial"][-1]["content"])
            if not rst["attachment_dict"]:
                print("ERROR no attachment_dict:", line)
                continue
            gender = rst["attachment_dict"]["gender"]
            if gender not in ["男", "女"]:
                print("ERROR irregular gender:", gender, line)
            if gender not in gender_dgn:
                gender_dgn[gender] = 0
            gender_dgn[gender] += 1
    with open(source_path + data_no_dgn, "r") as in_file:
        for line in in_file.readlines():
            obj = json.loads(line)
            rst = json.loads(obj["dial"][-1]["content"])
            if not rst["attachment_dict"]:
                print("ERROR no attachment_dict:", line)
                continue
            gender = rst["attachment_dict"]["gender"]
            if gender not in ["男", "女"]:
                print("ERROR irregular gender:", gender, line)
            if gender not in gender_no_dgn:
                gender_no_dgn[gender] = 0
            gender_no_dgn[gender] += 1
    with open(source_path + data_no_rst, "r") as in_file:
        for line in in_file.readlines():
            obj = json.loads(line)
            has_gender = False
            for _, dial in enumerate(obj["dial"]):
                if "性别" in dial["content"]:
                    gender = obj["dial"][_ + 1]["content"]
                    if gender not in ["男", "女"]:
                        print("ERROR irregular gender:", gender, line)
                    if gender not in gender_no_rst:
                        gender_no_rst[gender] = 0
                    gender_no_rst[gender] += 1
                    has_gender = True
            if not has_gender:
                print("ERROR no gender:", line)
    print(gender_dgn, gender_no_dgn, gender_no_rst)
    labels = [num[0] for num in gender_no_rst.items()]
    gender_dgn = [num[1] + list(gender_no_dgn.items())[_][1] for _, num in enumerate(gender_dgn.items())]
    gender_no_rst = [num[1] for num in gender_no_rst.items()]
    ratio = [num / gender_no_rst[_] for _, num in enumerate(gender_dgn)]
    bar_width = 0.3
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.bar(np.arange(2), gender_dgn, label='complete', alpha=0.8, width=bar_width)
    ax1.bar(np.arange(2) + bar_width, gender_no_rst, label='uncompleted', alpha=0.8, width=bar_width)
    ax1.set_xlabel('gender')
    ax1.set_ylabel('number')
    ax1.set_title('Comparison between complete and uncompleted dialogues\nand their ratios at genders')
    plt.xticks(np.arange(2) + bar_width / 2, labels, fontproperties=font)
    for _, num_dgn in enumerate(gender_dgn):
        plt.text(_ - bar_width * 0.5, num_dgn + 1, '%s' % num_dgn)
        plt.text(_ + bar_width * 0.5, gender_no_rst[_] + 1, '%s' % gender_no_rst[_])
    ax1.set_ylim(0, 650)
    ax1.legend(loc=2)
    ax2 = ax1.twinx()
    ax2.plot(np.arange(2) + bar_width / 2, ratio, 'r*',
             label='ratio between the number of the\n complete and the uncompleted')
    ax2.set_ylabel('ratio')
    ax2.set_ylim(0, 6)
    for _, ra in enumerate(ratio):
        plt.text(_ + bar_width / 2, ra + 0.1, '%.2f' % ra)
    ax2.legend()
    plt.show()


# get gender xxx cross dict - xxx : span, time, age, description
def cross_anl_gender(cross_group, data_path, cross_type):
    gender_group_arr = {}
    for cg in cross_group:
        gender_group_arr[cg] = {}
        for gg in Utils.gender_group[:-1]:
            gender_group_arr[cg][gg] = 0
    gender_group_arr["unknown"] = {}
    for gg in Utils.gender_group[:-1]:
        gender_group_arr["unknown"][gg] = 0
    with open(data_path, "r") as data_file:
        for li in data_file.readlines():
            obj = json.loads(li)
            if len(obj["dial"]) < 3:
                continue
            else:
                # get cross and des_cat
                gender = Utils.get_cross('gender', obj)
                if gender == "unknown":
                    continue
                cross = Utils.get_cross(cross_type, obj)
                if cross_type == "description":
                    for des in cross:
                        for cg in cross_group:
                            if des == cg and des is not 'unknown':
                                gender_group_arr[des][gender] += 1
                        if des == "unknown":
                            gender_group_arr['unknown'][gender] += 1
                else:
                    for cg in cross_group:
                        if cross == cg:
                            gender_group_arr[cross][gender] += 1
                    if cross == "unknown":
                        gender_group_arr['unknown'][gender] += 1
    return gender_group_arr


# plot cross
def plot_cross_gender(gender_group_arr, cross_group, cross_type, title, x_label):
    labels = [num[0] for num in gender_group_arr[cross_group[0]].items()]
    dc_count = {}  # count of each dc
    for dc in Utils.gender_group[:-1]:
        dc_count[dc] = sum([gender_group_arr[cg][dc] for cg in gender_group_arr])
    dc_arr = {}
    for cg in cross_group:
        dc_arr[cg] = [num[1] for num in gender_group_arr[cg].items()]
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
    plt.xticks(np.arange(len(dc_arr[cross_group[0]])) + bar_width * (len(gender_group_arr) - 1) / 2, labels,
               fontproperties=font)
    for _, num in enumerate(dc_arr[cross_group[0]]):
        for __, cg in enumerate(cross_group):
            if cross_type == "description":
                plt.text(_ + bar_width * (__ - 0.5), dc_arr[cg][_] + 1,
                         Utils.des_decode[cg] + '\n%d(%.f' % (
                             dc_arr[cg][_], dc_arr[cg][_] / list(dc_count.items())[_][1] * 100) + "%)",
                         fontproperties=font)
            else:
                plt.text(_ + bar_width * (__ - 0.5), dc_arr[cg][_] + 1,
                         '\n%d(%.f' % (dc_arr[cg][_], dc_arr[cg][_] / list(dc_count.items())[_][1] * 100) + "%)",
                         fontproperties=font)
    ax1.set_ylim(0, )
    ax1.set_xlim(-0.3, )
    if cross_type is not "description":
        ax1.legend()
    plt.show()


gc_group = {'time': Utils.time_group, 'span': Utils.span_group, 'age': Utils.age_group,
            'gender': Utils.gender_group, 'description': Utils.des_cate}


if __name__ == '__main__':
    cross_type = 'description'  # time, span, age, gender, description
    gender_cross_group_arr = cross_anl_gender(gc_group[cross_type], source_path + data, cross_type=cross_type)
    print(gender_cross_group_arr)
    plot_cross_gender(gender_cross_group_arr, gc_group[cross_type], cross_type=cross_type,
                      title='Comparison between dialogues of different ' + cross_type + '\naccording to gender',
                      x_label='')


