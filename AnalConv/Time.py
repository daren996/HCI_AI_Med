"""
dial[{"time": time, "speaker": speaker, "content": content}, ...]
que_ans_time_arr[[(que, ans, time), (...), ...], [...], ...]

"""

import json
from collections import Counter

import Utils
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties

font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc', size=6)
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

source_path = "../DataSet/"
data_set = "dial.txt"
data_dgn = "dial_dgn.txt"
data_no_dgn = "dial_no_dgn.txt"
data_no_rst = "dial_no_rst.txt"


# get time array
# que_ans_time_arr = []
# with open(source_path + data_set, "r") as in_file:
#     for line in in_file.readlines():
#         obj = json.loads(line)
#         c_time = []
#         r_time = []
#         if obj["dial"][0]["speaker"] != "Robot":
#             print("ERROR: client start", obj["id"])
#             continue
#         for x in range(1, len(obj["dial"])):  # check no continuous speaker
#             if obj["dial"][x]["speaker"] == obj["dial"][x-1]["speaker"]:
#                 print("ERROR: continuous speaker:", obj["id"])
#         for dial in json.loads(line)["dial"]:
#             if dial["speaker"] == "Robot":
#                 r_time.append((dial["content"], Utils.getTime(dial["time"][1])))
#             if dial["speaker"] == "client":
#                 c_time.append((dial["content"], Utils.getTime(dial["time"][1])))
#         que_ans_time = []
#         for x in range(1, len(c_time)):
#             time_dif = c_time[x][1] - c_time[x-1][1] + 1
#             if time_dif < 0:
#                 time_dif += 86400
#             que_ans_time.append((r_time[x][0], c_time[x][0], time_dif))
#         que_ans_time_arr.append(que_ans_time)
# print(len(que_ans_time_arr))

# get last 3 questions, answers and their times
# for que_ans_time in que_ans_time_arr:
#     if len(que_ans_time) < 3:
#         print(len(que_ans_time), que_ans_time)
#     else:
#         print(len(que_ans_time), que_ans_time[-3:])

# plot all time (in 3d)
# que_ans_time_arr = que_ans_time_arr[150:200]
# px = np.linspace(0, 1, 100)
# py = np.arange(0, len(que_ans_time_arr), 1)
# px, py = np.meshgrid(px, py)
# pz = np.zeros(shape=(len(que_ans_time_arr), 100))
# for _, que_ans_time in enumerate(que_ans_time_arr):
#     ax = np.linspace(0, 1, len(que_ans_time))
#     ay = np.array([x[2] for x in que_ans_time])
#     f = interpolate.interp1d(ax, ay, kind='cubic')
#     nx = np.linspace(0, 1, 100)
#     ny = f(nx)
#     pz[_] = ny
#     # plt.plot(nx, ny)
#     # plt.show()
#     # exit(-1)
# print(px.shape, py.shape, pz.shape)
# fig = plt.figure()
# ax = Axes3D(fig)
# # ax.plot_surface(px, py, pz, rstride=1, cstride=1, cmap='rainbow')
# ax.plot_wireframe(px, py, pz, rstride=1, cstride=1, cmap='rainbow')
# plt.show()

# average time distribution
def get_time_dis():
    ave_rnd_tim_all = []
    with open(source_path + data_set, "r") as in_file:
        for line in in_file.readlines():
            obj = json.loads(line)
            if len(obj["dial"]) > 2:
                print(obj["dial"][3]["content"], end=",")
            tim = Utils.getTime(obj["dial"][-1]["time"][1]) - Utils.getTime(obj["dial"][0]["time"][1])
            if tim < 0:
                tim += 86400
            rnd = int(len(obj["dial"]) / 2)
            print(rnd, ",", "%.2f" % (tim / rnd), end=",")
            ave_rnd_tim_all.append(tim / rnd)
            print()
    ave_rnd_tim_all = sorted(ave_rnd_tim_all, key=lambda x: x, reverse=False)
    print(ave_rnd_tim_all)
    ave_rnd_tim_dst = dict(Counter([int(np.ceil(art)) for art in ave_rnd_tim_all]))
    ave_rnd_tim_dst = sorted(ave_rnd_tim_dst.items(), key=lambda td: td[0])
    print(ave_rnd_tim_dst)
    limit = 80
    ind = [ld[0] for ld in ave_rnd_tim_dst]
    art_dst = [ld[1] for ld in ave_rnd_tim_dst]
    plt.plot(ind, art_dst)
    plt.xlim(-1, 50)
    plt.xlabel('average time')
    plt.ylabel('number of dialogues')
    plt.title('distribution of average time of dialogues')
    plt.show()


# get gender xxx cross dict - xxx : span, time, age, description
def cross_anl_time(cross_group, data_path, time_group, cross_type):
    time_group_arr = {}
    for cg in cross_group:
        time_group_arr[cg] = {}
        for gg in time_group:
            time_group_arr[cg][gg] = 0
    time_group_arr["unknown"] = {}
    for gg in time_group:
        time_group_arr["unknown"][gg] = 0
    with open(data_path, "r") as data_file:
        for li in data_file.readlines():
            obj = json.loads(li)
            if len(obj["dial"]) < 3:
                continue
            else:
                # get cross and des_cat
                time = Utils.get_cross('time', obj)
                if time not in time_group:
                    continue
                cross = Utils.get_cross(cross_type, obj)
                if cross_type == "description":
                    for des in cross:
                        for cg in cross_group:
                            if des == cg and des is not 'unknown':
                                time_group_arr[des][time] += 1
                        if des == "unknown":
                            time_group_arr['unknown'][time] += 1
                else:
                    for cg in cross_group:
                        if cross == cg:
                            time_group_arr[cross][time] += 1
                    if cross == "unknown":
                        time_group_arr['unknown'][time] += 1
    return time_group_arr


# plot cross
def plot_cross_time(time_group_arr, time_group, cross_group, cross_type, title, x_label):
    labels = [num[0] for num in time_group_arr[cross_group[0]].items()]
    ac_count = {}  # count of each dc
    for dc in time_group:
        ac_count[dc] = sum([time_group_arr[cg][dc] for cg in time_group_arr])+1
    dc_arr = {}
    for cg in cross_group:
        dc_arr[cg] = [num[1] for num in time_group_arr[cg].items()]
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
    plt.xticks(np.arange(len(dc_arr[cross_group[0]])) + bar_width * (len(time_group_arr) - 1) / 2, labels,
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
    time_gro = Utils.time_group
    time_cross_group_arr = cross_anl_time(ac_group[cross_type], source_path + data_set, time_gro, cross_type=cross_type)
    print(time_cross_group_arr)
    plot_cross_time(time_cross_group_arr, time_gro, ac_group[cross_type], cross_type=cross_type,
                    title='Comparison between dialogues of different ' + cross_type + '\naccording to time',
                    x_label='')
