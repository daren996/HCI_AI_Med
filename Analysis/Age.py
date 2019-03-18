"""
Analyze Info of Age.

Structure of dial.txt:
obj{"id": id, "dial": dial}
dial[{"time": time, "speaker": speaker, "content": content}, ...]
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import Utils
from matplotlib.font_manager import FontProperties

font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc', size=6)
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

source_path = "../DataSet/"
data = "dial.txt"
data_dgn = "dial_dgn.txt"
data_no_dgn = "dial_no_dgn.txt"
data_no_rst = "dial_no_rst.txt"


# query as others 代替别人询问
# age_group = {}
# age_0_6 = []
# age_60 = []
# age_7_15 = []
# with open(source_path + data_dgn, "r") as in_file:
#     for line in in_file.readlines():
#         obj = json.loads(line)
#         rst = json.loads(obj["dial"][-1]["content"])
#         if not rst["attachment_dict"]:
#             continue
#         age = rst["attachment_dict"]["age_group"]
#         if age == "0~6岁":
#             age_0_6.append(obj["dial"][3]["content"])
#         if age == "大于60岁":
#             age_60.append(obj["dial"][3]["content"])
#         if age == "7~15岁":
#             age_7_15.append(obj["dial"][3]["content"])
#         if age not in age_group:
#             age_group[age] = 0
#         age_group[age] += 1
# print(age_group)
# for c in age_0_6:
#     print(c)
# print("\n")
# for c in age_7_15:
#     print(c)
# print("\n")
# for c in age_60:
#     print(c)

# get gender xxx cross dict - xxx : span, time, age, description
def cross_anl_age(cross_group, data_path, age_group, cross_type):
    age_group_arr = {}
    for cg in cross_group:
        age_group_arr[cg] = {}
        for gg in age_group:
            age_group_arr[cg][gg] = 0
    age_group_arr["unknown"] = {}
    for gg in age_group:
        age_group_arr["unknown"][gg] = 0
    with open(data_path, "r") as data_file:
        for li in data_file.readlines():
            obj = json.loads(li)
            if len(obj["dial"]) < 3:
                continue
            else:
                # get cross and des_cat
                age = Utils.get_cross('age', obj)
                if age not in age_group:
                    continue
                cross = Utils.get_cross(cross_type, obj)
                if cross_type == "description":
                    for des in cross:
                        for cg in cross_group:
                            if des == cg and des is not 'unknown':
                                age_group_arr[des][age] += 1
                        if des == "unknown":
                            age_group_arr['unknown'][age] += 1
                else:
                    for cg in cross_group:
                        if cross == cg:
                            age_group_arr[cross][age] += 1
                    if cross == "unknown":
                        age_group_arr['unknown'][age] += 1
    return age_group_arr


# plot cross
def plot_cross_age(age_group_arr, age_group, cross_group, cross_type, title, x_label):
    labels = [num[0] for num in age_group_arr[cross_group[0]].items()]
    ac_count = {}  # count of each dc
    for dc in age_group:
        ac_count[dc] = sum([age_group_arr[cg][dc] for cg in age_group_arr])
    dc_arr = {}
    for cg in cross_group:
        dc_arr[cg] = [num[1] for num in age_group_arr[cg].items()]
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
    plt.xticks(np.arange(len(dc_arr[cross_group[0]])) + bar_width * (len(age_group_arr) - 1) / 2, labels,
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
    age_gro = Utils.age_group
    age_cross_group_arr = cross_anl_age(ac_group[cross_type], source_path + data, age_gro, cross_type=cross_type)
    print(age_cross_group_arr)
    plot_cross_age(age_cross_group_arr, age_gro, ac_group[cross_type], cross_type=cross_type,
                   title='Comparison between dialogues of different ' + cross_type + '\naccording to age',
                   x_label='')
