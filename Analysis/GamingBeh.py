
"""
Analyze gaming behavior.


"""


import json
from collections import Counter
import jieba
import numpy as np
import matplotlib.pyplot as plt
import Utils
from matplotlib.font_manager import FontProperties
from scipy import interpolate

font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc', size=8)
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

source_path = "../DataSet/"
data_set = "dial_gaming.txt"


# average time
# get format: Q&A&Time [[(question, answer, time), (...), ...], [...], ...]
que_ans_time_arr = Utils.get_que_ans_time_arr(source_path, data_set)
all_dial_count = len(que_ans_time_arr)
tim_dial = dict(Counter([int(np.ceil(sum([qa[2] for qa in qat])/len(qat))) for qat in que_ans_time_arr if len(qat) is not 0]))
tim_dial[0] = 0
tim_dial = sorted(tim_dial.items(), key=lambda td: td[0])
print(tim_dial)
std_dial = dict(Counter([np.ceil(np.std([tim[2] for tim in qat])) for qat in que_ans_time_arr if len(qat) is not 0]))
std_dial = sorted(std_dial.items(), key=lambda sd: sd[0])
print(std_dial)

width = 0.6
limit = 50
# f = interpolate.interp1d([td[0] for td in std_dial],
#                          [td[1] for td in std_dial], kind='cubic')
# nx = np.linspace(0, limit, 1000)
# ny = f(nx)
# plt.plot(nx[:300], ny[:300])
plt.bar([td[0] for td in tim_dial], [td[1] for td in tim_dial])
plt.xlabel('time (s)')
plt.ylabel('number')
plt.title('The distribution of average round span - gaming')
plt.show()

