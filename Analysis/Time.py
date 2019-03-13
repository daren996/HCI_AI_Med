
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
