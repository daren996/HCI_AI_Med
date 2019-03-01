
"""
dial[{"time": time, "speaker": speaker, "content": content}, ...]
que_ans_time_arr[[(que, ans, time), (...), ...], [...], ...]

"""


import json
import Utils
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


source_path = "../DataSet/"
# data_set = "dial_dgn.txt"
data_set = "dial_no_rst.txt"


que_ans_time_arr = []
with open(source_path + data_set, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        c_time = []
        r_time = []
        if obj["dial"][0]["speaker"] != "Robot":
            print("ERROR: client start", obj["id"])
            continue
        for x in range(1, len(obj["dial"])):  # check no continuous speaker
            if obj["dial"][x]["speaker"] == obj["dial"][x-1]["speaker"]:
                print("ERROR: continuous speaker:", obj["id"])
        for dial in json.loads(line)["dial"]:
            if dial["speaker"] == "Robot":
                r_time.append((dial["content"], Utils.getTime(dial["time"][1])))
            if dial["speaker"] == "client":
                c_time.append((dial["content"], Utils.getTime(dial["time"][1])))
        que_ans_time = []
        for x in range(1, len(c_time)):
            time_dif = c_time[x][1] - c_time[x-1][1] + 1
            if time_dif < 0:
                time_dif += 86400
            que_ans_time.append((r_time[x][0], c_time[x][0], time_dif))
        que_ans_time_arr.append(que_ans_time)
print(len(que_ans_time_arr))
for que_ans_time in que_ans_time_arr:
    if len(que_ans_time) < 3:
        print(len(que_ans_time), que_ans_time)
    else:
        print(len(que_ans_time), que_ans_time[-3:])

# plot all time (3d)
# que_ans_time_arr = que_ans_time_arr[100:200]
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
# ax.plot_surface(px, py, pz, rstride=1, cstride=1, cmap='rainbow')
# # ax.plot_wireframe(px, py, pz, rstride=1, cstride=1, cmap='rainbow')
# plt.show()

