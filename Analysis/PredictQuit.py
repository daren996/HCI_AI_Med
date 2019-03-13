

import Utils
import json
import matplotlib.pylab as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import math
from collections import Counter
import csv
from scipy import interpolate


font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

source_path = "../DataSet/"
data_dgn = "dial_dgn.txt"
data_no_rst = "dial_no_rst.txt"

# get dgn and no_rst data
# get format: Q&A&Time [[(question, answer, time), (...), ...], [...], ...]
que_ans_time_arr_dgn = Utils.get_que_ans_time_arr(source_path, data_dgn)
que_ans_time_arr_no_rst = Utils.get_que_ans_time_arr(source_path, data_no_rst)


# according to round
all_dial_count = len(que_ans_time_arr_dgn) + len(que_ans_time_arr_no_rst)
len_dial_dgn = dict(Counter([len(qat) for qat in que_ans_time_arr_dgn]))
len_dial_dgn = sorted(len_dial_dgn.items(), key=lambda x: x[0])
len_dial_no_rst = dict(Counter([len(qat) for qat in que_ans_time_arr_no_rst]))
len_dial_no_rst = sorted(len_dial_no_rst.items(), key=lambda x: x[0])
ind = np.arange(len_dial_no_rst[-1][0]+1)
width = 0.6
prob = []
for i in range(len(ind)):
    prob.append(0)
for _, ld in enumerate(len_dial_no_rst):
    prob[ld[0]] = ld[1]/all_dial_count*100
    print("round:", ld[0], "number:", ld[1], "probability: %.2f" % (ld[1]/all_dial_count*100) + "%")
    all_dial_count = all_dial_count - len_dial_dgn[_][1] - len_dial_no_rst[_][1]
print(all_dial_count)
p1 = plt.bar(ind, prob, width)
for p in p1:
    x = p.get_x()
    height = p.get_height()
    plt.text(x-0.1, height+0.02, "%.2f" % p.get_height())
plt.ylabel('probability (%)')
plt.title('The probability of quitting on problem X')
plt.show()

# according to time
all_dial_count = len(que_ans_time_arr_dgn) + len(que_ans_time_arr_no_rst)
tim_dial_dgn = dict(Counter([int(np.ceil(sum([qa[2] for qa in qat])/10)) for qat in que_ans_time_arr_dgn]))
tim_dial_dgn = sorted(tim_dial_dgn.items(), key=lambda td: td[0])
tim_dial_no_rst = dict(Counter([int(np.ceil(sum([qa[2] for qa in qat])/10)) for qat in que_ans_time_arr_no_rst]))
tim_dial_no_rst = sorted(tim_dial_no_rst.items(), key=lambda td: td[0])
print(tim_dial_dgn)
print(tim_dial_no_rst)
# plot it
ind = np.arange(tim_dial_no_rst[-1][0]+1)
width = 0.6
prob = {}
# for i in range(len(ind)):
#     prob.append(0)
for _, ld in enumerate(tim_dial_no_rst):
    prob[ld[0]] = ld[1]/all_dial_count*100
    # print(ld[0], ld[1], "%.2f" % (ld[1]/all_dial_count*100) + "%")
    all_dial_count = all_dial_count - tim_dial_dgn[_][1] - tim_dial_no_rst[_][1]
# print(all_dial_count)
limit = 80
prob[limit] = sum([ld[1] for ld in tim_dial_no_rst if ld[0] > limit])/all_dial_count*100
# print(limit, sum([ld[1] for ld in tim_dial_no_rst if ld[0] > limit]), "%.2f" % prob[limit] + "%")
prob = list(prob.items())
for pr in prob:
    print("time:", "%d" % int(pr[0]*10) + "s", "probability:", "%.2f" % pr[1] + "%")
f = interpolate.interp1d([pr[0]*10 for pr in prob], [pr[1] for pr in prob], kind='cubic')
nx = np.linspace(0, limit*10, 1000)
ny = f(nx)
plt.plot(nx[0:800], ny[0:800])
plt.xlabel('time (s)')
plt.ylabel('probability (%)')
plt.title('The probability of quitting on problem X\naccording to time cost')
plt.show()

