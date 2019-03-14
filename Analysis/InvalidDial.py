"""
Analyze Invalid Dialogues

Structure of dial.txt:
obj{"id": id, "dial": dial}
dial[{"time": time, "speaker": speaker, "content": content}, ...]
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import Utils
from matplotlib.font_manager import FontProperties

font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

source_path = "../DataSet/"
data = "dial.txt"
data_dgn = "dial_dgn.txt"
data_no_dgn = "dial_no_dgn.txt"
data_no_rst = "dial_no_rst.txt"
data_invalid = "invalid.txt"

# get invalid id set
invalid_id = set()
with open(source_path + data_invalid, 'r') as in_file:
    for line in in_file.readlines():
        temp = line.strip().split('\t')
        dis = temp[0]
        rnd = int(temp[1])
        ave_time = float(temp[2])
        id_ = temp[3].strip()
        invalid_id.add(id_)
print("length of invalid dials", len(invalid_id))


# compare valid and invalid dials according to age, time, span, ..
def cross_anl_valid(cross_group, data_path, cross_type):
    valid_group_arr = {}
    for cg in cross_group:
        valid_group_arr[cg] = {}
        for vg in Utils.valid_group:
            valid_group_arr[cg][vg] = 0
    valid_group_arr["unknown"] = {}
    for vg in Utils.valid_group:
        valid_group_arr["unknown"][vg] = 0
    with open(data_path, "r") as data_file:
        for li in data_file.readlines():
            obj = json.loads(li)
            if len(obj["dial"]) == 0:
                continue
            else:
                # get cross and valid
                cross = Utils.get_cross(cross_type, obj)
                if obj["id"] in invalid_id:
                    valid = "invalid"
                else:
                    valid = "valid"
                for cg in cross_group:
                    if cross == cg:
                        valid_group_arr[cross][valid] += 1
                if cross == "unknown":
                    valid_group_arr['unknown'][valid] += 1
    return valid_group_arr


def plot_cross_valid(valid_group_arr, cross_group, cross_type, title, x_label):
    labels = [num[0] for num in valid_group_arr[cross_group[0]].items()]
    vg_count = {}  # count of each vg
    for vg in Utils.valid_group:
        vg_count[vg] = sum([valid_group_arr[cg][vg] for cg in valid_group_arr])
    vg_arr = {}
    for cg in cross_group:
        vg_arr[cg] = [num[1] for num in valid_group_arr[cg].items()]
    bar_width = 0.8 / len(cross_group)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for _, cg in enumerate(cross_group):
        if cross_type == 'age':
            ax1.bar(np.arange(len(vg_arr[cg])) + bar_width * _, vg_arr[cg],
                    label=Utils.age_decode[cg], alpha=0.8, width=bar_width)
        elif cross_type == "gender":
            ax1.bar(np.arange(len(vg_arr[cg])) + bar_width * _, vg_arr[cg],
                    label=Utils.gender_decode[cg], alpha=0.8, width=bar_width)
        else:
            ax1.bar(np.arange(len(vg_arr[cg])) + bar_width * _, vg_arr[cg],
                    label=cg, alpha=0.8, width=bar_width)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel('number')
    ax1.set_title(title)
    plt.xticks(np.arange(len(vg_arr[cross_group[0]])) + bar_width * (len(valid_group_arr)-1) / 2, labels, fontproperties=font)
    for _, num in enumerate(vg_arr[cross_group[0]]):
        for __, cg in enumerate(cross_group):
            plt.text(_ + bar_width * (__ - 0.5), vg_arr[cg][_] + 1,
                     '%s(%.f' % (vg_arr[cg][_], vg_arr[cg][_]/list(vg_count.items())[_][1]*100) + "%)")
    ax1.set_ylim(0, )
    ax1.legend()
    plt.show()


# age and validity crossing analysis
# valid_cross_group_arr = cross_anl_valid(Utils.age_group, source_path + data, cross_type='age')
# print(valid_cross_group_arr)
# plot_cross_valid(valid_cross_group_arr, Utils.age_group, cross_type='age',
#                  title='Comparison between dialogues of different ages\nat the validity',
#                  x_label='')

# gender and validity crossing analysis
# valid_cross_group_arr = cross_anl_valid(Utils.gender_group, source_path + data, cross_type='gender')
# print(valid_cross_group_arr)
# plot_cross_valid(valid_cross_group_arr, Utils.gender_group, cross_type='gender',
#                  title='Comparison between dialogues of different gender\nat the validity',
#                  x_label='')

# span and validity crossing analysis
# valid_cross_group_arr = cross_anl_valid(Utils.span_group, source_path + data, cross_type='span')
# print(valid_cross_group_arr)
# plot_cross_valid(valid_cross_group_arr, Utils.span_group, cross_type='span',
#                  title='Comparison between dialogues of different time span\naccording to validity',
#                  x_label='')

# time and validity crossing analysis
valid_cross_group_arr = cross_anl_valid(Utils.time_group, source_path + data, cross_type='time')
print(valid_cross_group_arr)
plot_cross_valid(valid_cross_group_arr, Utils.time_group, cross_type='time',
                 title='Comparison between dialogues of different occurrence time\naccording to validity',
                 x_label='')
