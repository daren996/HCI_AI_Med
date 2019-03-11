

import Utils
import json
import matplotlib.pylab as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import math
from collections import Counter
import csv

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

# simple frequency
all_dial_count = len(que_ans_time_arr_dgn) + len(que_ans_time_arr_no_rst)
len_dial_no_rst = dict(Counter([len(qat) for qat in que_ans_time_arr_no_rst]))
len_dial_no_rst = sorted(len_dial_no_rst.items(), key=lambda x: x[0])
for ld in len_dial_no_rst:
    print(ld[0], ld[1], "%.2f" % (ld[1]/all_dial_count*100) + "%")
ind = np.arange(len_dial_no_rst[-1][0]+1)
width = 0.6
prob = []
for i in range(len(ind)):
    prob.append(0)
for _, ld in enumerate(len_dial_no_rst):
    prob[ld[0]] = ld[1]/all_dial_count*100
p1 = plt.bar(ind, prob, width)
for p in p1:
    x = p.get_x()
    height = p.get_height()
    plt.text(x-0.1, height+0.02, "%.2f" % p.get_height())
plt.ylabel('probability (%)')
plt.title('The probability of quitting on problem X')
plt.show()

