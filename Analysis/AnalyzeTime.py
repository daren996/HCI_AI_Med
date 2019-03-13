"""
The occurrence time of each dialogue

"""

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
data_no_dgn = "dial_no_dgn.txt"
data_no_rst = "dial_no_rst.txt"

# get dgn and no_rst data
# get format: Q&A&Time [[(question, answer, time), (...), ...], [...], ...]
que_ans_time_arr_dgn = Utils.get_que_ans_time_arr(source_path, data_dgn)
que_ans_time_arr_no_dgn = Utils.get_que_ans_time_arr(source_path, data_no_dgn)
que_ans_time_arr_no_rst = Utils.get_que_ans_time_arr(source_path, data_no_rst)
# print(len(que_ans_time_arr_dgn))
# print(len(que_ans_time_arr_no_dgn))
# print(len(que_ans_time_arr_no_rst))
# print(len(que_ans_time_arr_dgn) + len(que_ans_time_arr_no_dgn) + len(que_ans_time_arr_no_rst))


