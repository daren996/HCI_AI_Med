"""
Analyze Users' Description.

Structure of dial.txt:
obj{"id": id, "dial": dial}
dial[{"time": time, "speaker": speaker, "content": content}, ...]
"""

import json
from collections import Counter
import jieba
import numpy as np
import matplotlib.pyplot as plt
import Utils
from matplotlib.font_manager import FontProperties
from scipy import interpolate


font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

source_path = "../DataSet/"
data_set = "dial.txt"

# average time distribution
ave_rnd_tim_all = []
with open(source_path + data_set, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        if len(obj["dial"]) > 2:
            print(obj["dial"][3]["content"] + ", ", end="")
        tim = Utils.getTime(obj["dial"][-1]["time"][1]) - Utils.getTime(obj["dial"][0]["time"][1])
        if tim < 0:
            tim += 86400
        rnd = int(len(obj["dial"]) / 2)
        print("%d" % rnd + ", " + "%.2f" % (tim / rnd) + ", ", end="")
        ave_rnd_tim_all.append(tim / rnd)
        print(obj["id"])

