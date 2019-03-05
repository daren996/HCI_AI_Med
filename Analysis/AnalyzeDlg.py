# -*- coding: utf-8 -*-


"""
Structure of dial.txt:
obj{"id": id, "dial": dial}
dial[{"time": time, "speaker": speaker, "content": content}, ...]
"""

import json
import matplotlib.pylab as plt
import numpy as np
import math
from collections import Counter
from matplotlib.font_manager import FontProperties
import csv


font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')


source_path = "../DataSet/"
data_set = "dial_dgn.txt"

# all services
# service_needed = {}
# with open(source_path + data_set, "r") as in_file:
#     for line in in_file.readlines():
#         obj = json.loads(line)
#         if "需要哪方面的服务" not in obj["dial"][0]["content"]:
#             # print(obj["id"])
#             continue
#         if obj["dial"][1]["content"] not in service_needed:
#             service_needed[obj["dial"][1]["content"]] = 0
#         service_needed[obj["dial"][1]["content"]] += 1
# print("Number of services needed is:", len(service_needed), list(service_needed.keys()))


# whether pregnant
# count_no_asked = 0
# with open(source_path + data_set, "r") as in_file:
#     for line in in_file.readlines():
#         asked = True
#         obj = json.loads(line)
#         for dia in obj["dial"]:
#             if "女" in dia["content"]:
#                 asked = False
#         for dia in obj["dial"]:
#             if "孕妇" in dia["content"]:
#                 asked = True
#         if not asked:
#             count_no_asked += 1
#             print(obj["id"])
# print("Number of women who aren't asked about pregnancy:", count_no_asked)


def getTime(timeStr):
    temp = timeStr.split(":")
    timeSec = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2])
    return timeSec


# total time
# time_arr = []
# with open(source_path + data_set, "r") as in_file:
#     for line in in_file.readlines():
#         obj = json.loads(line)
#         time_start = getTime(obj["dial"][0]["time"][1])
#         time_end = getTime(obj["dial"][-1]["time"][1])
#         if time_end - time_start < 0:
#             time_end += 86400
#         time_arr.append(time_end - time_start + 1)
# print("Average time: %.3f" % np.mean(np.array(time_arr)))
# time_draw = {}
# for time in time_arr:
#     if math.ceil(time) not in time_draw:
#         time_draw[math.ceil(time)] = 0
#     time_draw[math.ceil(time)] += 1
# time_draw = sorted(time_draw.items(), key=lambda x: x[0], reverse=False)
# # for time in time_draw:
# #     print(time)
# fig = plt.figure(1, figsize=(10, 8))
# ax = fig.add_subplot(111)
# ax.set_title("time_distribute")
# ax.bar([x[0] for x in time_draw], [x[1] for x in time_draw])
# ax.set_ylim(0, 62)
# ax.set_xlim(-10, 500)
# fig.savefig("time_dist.png")
# plt.show()

# get format: Q&A&Time [[(question, answer, time), (...), ...], [...], ...]
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
                r_time.append((dial["content"], getTime(dial["time"][1])))
            if dial["speaker"] == "client":
                c_time.append((dial["content"], getTime(dial["time"][1])))
        que_ans_time = []
        for x in range(1, len(c_time)):
            time_dif = c_time[x][1] - c_time[x-1][1] + 1
            if time_dif < 0:
                time_dif += 86400
            que_ans_time.append((r_time[x][0], c_time[x][0], time_dif))
        que_ans_time_arr.append(que_ans_time)
print(len(que_ans_time_arr))

with open('quesTime.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')
    spamwriter.writerow(["问题", "时间", "问题", "时间", "问题", "时间"])
    for tim in que_ans_time_arr:
        row = []
        for ti in tim:
            row += [ti[0], ti[1], ti[2]]
        spamwriter.writerow(row)

# most time-cost question
# fir_ques = []
# for que_ans_time in que_ans_time_arr:
#     rank_que_ans_time = sorted(que_ans_time, key=lambda x: x[2], reverse=True)
#     fir_ques.append(rank_que_ans_time[0][0])
#     # print(rank_que_ans_time)
# fir_que_cnt = [x for x in dict(Counter(fir_ques)).items()]
# print(fir_que_cnt)
# rank_show_sym = 20
# fir_que_cnt = fir_que_cnt[0:rank_show_sym] + [('else', sum([sym[1] for sym in fir_que_cnt[rank_show_sym:]]))]
# fig = plt.figure(3, figsize=(10, 8))
# ax = fig.add_subplot(111)
# ax.set_title('symptom')
# labels = ['{}:{}'.format(que, num) for que, num in zip([que[0] for que in fir_que_cnt], [que[1] for que in fir_que_cnt])]
# ax.pie([que[1] for que in fir_que_cnt], labels=labels, explode=[0] * rank_show_sym + [0.1], shadow=True)
# fig.savefig('symptoms_info.png')
# plt.show()


# past medical history
# ask_med_hst = []
# with open(source_path + data_set, "r") as in_file:
#     for _, line in enumerate(in_file.readlines()):
#         asked = False
#         obj = json.loads(line)
#         for __, que in enumerate(obj["dial"]):
#             if not asked and "史" in que["content"] and que["speaker"] == "Robot" and __ < len(obj["dial"])-1:
#                 print(_, que["content"], obj["dial"][__+1]["content"])
#                 ask_med_hst.append(que["content"])
#                 asked = True
# print(len(ask_med_hst))


