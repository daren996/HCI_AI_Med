
import Utils
import json
import matplotlib.pylab as plt
import numpy as np
import math
from collections import Counter
import csv


source_path = "../DataSet/"
data_set = "dial_dgn.txt"

with open(source_path + data_set, "r") as in_file:
    lines = in_file.readlines()
    service_needed = Utils.findServices(lines)
    count_no_asked = Utils.noPregnantAsked(lines)
# print("Number of services needed is:", len(service_needed), list(service_needed.keys()))
# print("Number of women who aren't asked about pregnancy:", count_no_asked)

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
                r_time.append((dial["content"], Utils.getTime(dial["time"][1])))
            if dial["speaker"] == "client":
                c_time.append((dial["content"], Utils.getTime(dial["time"][1])))
        que_ans_time = []
        for x in range(0, len(c_time) - 1):
            time_dif = r_time[x + 1][1] - c_time[x][1] + 1
            if time_dif < 0:
                time_dif += 86400
            que_ans_time.append((r_time[x][0], c_time[x][0], time_dif))
        que_ans_time_arr.append(que_ans_time)
        # print(que_ans_time)
print(len(que_ans_time_arr))

# time distribute
# time_arr = []
# for qat in que_ans_time_arr:
#     if len(qat) > 0:
#         time_arr.append(qat[-1][2]+1)
#         # print(qat[-1][2])
#     else:
#         time_arr.append(1)
#         # print(1)
# time_item = Counter(time_arr)
# time_item = sorted(time_item.items(), key=lambda tim: tim[0], reverse=False)
# print(time_item)
# plt.plot([tim[0] for tim in time_item[:-4]], [tim[1] for tim in time_item[:-4]])
# plt.show()

# last questions
time3_arr = []
for qat in que_ans_time_arr:
    if len(qat) == 0:
        continue
    elif len(qat) > 2:
        time3_arr.append([(qat[-3][0], qat[-3][1], qat[-3][2]),
                          (qat[-2][0], qat[-2][1], qat[-2][2]),
                          (qat[-1][0], qat[-1][1], qat[-1][2])])
    # else:
    #     time3_arr.append([qa[2] for qa in qat])
print(time3_arr)
# time3_arr = sorted(time3_arr, key=lambda tim: tim[-1][2], reverse=False)
# for tim in time3_arr:
#     for ti in tim:
#         print(ti[0], "\t", ti[1], "\t", ti[2], end="\t")
#     print()

# save it in csv file
# with open('last3ques.csv', 'w') as csvfile:
#     spam_writer = csv.writer(csvfile, dialect='excel')
#     spam_writer.writerow(["倒数第三个问题", "倒数第三个回答", "时间", "倒数第二个问题", "倒数第二个回答", "时间",
#                          "倒数第一个问题", "倒数第一个回答", "时间"])
#     for tim in time3_arr:
#         row = []
#         for ti in tim:
#             row += [ti[0], ti[1], ti[2]]
#         spam_writer.writerow(row)

# average time
# last_qa_time = {}
# for tim in que_ans_time_arr:
#     for ti in tim:
#         if ti[0] not in last_qa_time:
#             last_qa_time[ti[0]] = []
#         last_qa_time[ti[0]].append(ti[2])
# for que in last_qa_time:
#     print(len(last_qa_time[que]), que, np.mean(np.array(last_qa_time[que])))

# classify questions
que_cate_arr = {}
for cat in Utils.ques_type:
    que_cate_arr[cat] = []
for que in que_ans_time_arr:
    for qu in que:
        classified = False
        for cat in Utils.ques_type:
            for ca in Utils.ques_type[cat]:
                if ca in qu[0]:
                    que_cate_arr[cat].append((qu[0], qu[2]))
                    classified = True
        if not classified:
            # print(qu[0])
            que_cate_arr["else"].append((qu[0], qu[2]))
for cat in que_cate_arr:
    print(cat, len(que_cate_arr[cat]),
          "%.2f" % np.mean(np.array([tim[1] for tim in que_cate_arr[cat]])), Utils.ques_type[cat])


