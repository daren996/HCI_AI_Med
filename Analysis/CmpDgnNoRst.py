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

# get dgn data
# get format: Q&A&Time [[(question, answer, time), (...), ...], [...], ...]
que_ans_time_arr_dgn = Utils.get_que_ans_time_arr(source_path, data_dgn)
print(len(que_ans_time_arr_dgn))
# que_cate_arr = {category: [(question, time), (...), ...]}
que_cate_arr_dgn, que_cate_arr_count_dgn = Utils.get_que_cate_arr(que_ans_time_arr_dgn)

# get no_rst data
que_ans_time_arr_no_rst = Utils.get_que_ans_time_arr(source_path, data_no_rst)
print(len(que_ans_time_arr_no_rst))
que_cate_arr_no_rst, que_cate_arr_count_no_rst = Utils.get_que_cate_arr(que_ans_time_arr_no_rst)

# compare statistics of dgn and no_rst
cate_cmp_arr = {}
for cat in que_cate_arr_dgn:
    cate_cmp_arr[cat] = [(len(que_cate_arr_dgn[cat]), len(que_cate_arr_no_rst[cat])),
                         (len(que_cate_arr_dgn[cat]) / que_cate_arr_count_dgn * 100,
                          len(que_cate_arr_no_rst[cat]) / que_cate_arr_count_no_rst * 100),
                         (np.mean(np.array([tim[1] for tim in que_cate_arr_dgn[cat]])),
                          np.mean(np.array([tim[1] for tim in que_cate_arr_no_rst[cat]])))]
# print("dgn")
# for cat in que_cate_arr_dgn:
#     print(cat, len(que_cate_arr_dgn[cat]), "%.2f" % (len(que_cate_arr_dgn[cat]) / que_cate_arr_count_dgn * 100) + "%",
#           "%.2f" % np.mean(np.array([tim[1] for tim in que_cate_arr_dgn[cat]])) + "s", Utils.ques_type[cat])
# print("no_rst")
# for cat in que_cate_arr_no_rst:
#     print(cat, len(que_cate_arr_no_rst[cat]),
#           "%.2f" % (len(que_cate_arr_no_rst[cat]) / que_cate_arr_count_no_rst * 100) + "%",
#           "%.2f" % np.mean(np.array([tim[1] for tim in que_cate_arr_no_rst[cat]])) + "s", Utils.ques_type[cat])

# plot percentage of complete dialogue and uncompleted dialogue and their ratio
# ind = np.arange(len(cate_cmp_arr))    # the x locations for the groups
# width = 0.6       # the width of the bars: can also be len(x) sequence
# per_dgn = [cate_cmp_arr[cat][1][0] for cat in cate_cmp_arr]
# per_no_rst = [cate_cmp_arr[cat][1][1] for cat in cate_cmp_arr]
# p1 = plt.bar(ind, per_dgn, width)
# p2 = plt.bar(ind, per_no_rst, width, bottom=per_dgn)
# for p_, p__ in zip(p1, p2):
#     x = p_.get_x()
#     height = p_.get_height() + p__.get_height()
#     plt.text(x, height+0.7, "%.2f" % (p_.get_height() / p__.get_height()))
# plt.ylabel('percentage')
# plt.title('percentage of complete dialogue and uncompleted dialogue and their ratio')
# plt.xticks(ind, [cat for cat in cate_cmp_arr], fontproperties=font)
# # plt.yticks(np.arange(0, 81, 10))
# plt.legend((p1[0], p2[0]), ('percentage of complete dialogue', 'percentage of uncompleted dialogue'))
# plt.show()

# plot average time of complete dialogue and uncompleted dialogue and their ratio
ind = np.arange(len(cate_cmp_arr))    # the x locations for the groups
width = 0.6       # the width of the bars: can also be len(x) sequence
time_dgn = [cate_cmp_arr[cat][2][0] for cat in cate_cmp_arr]
time_no_rst = [cate_cmp_arr[cat][2][1] for cat in cate_cmp_arr]
p1 = plt.bar(ind, time_dgn, width)
p2 = plt.bar(ind, time_no_rst, width, bottom=time_dgn)
for p_, p__ in zip(p1, p2):
    x = p_.get_x()
    height = p_.get_height() + p__.get_height()
    plt.text(x, height+0.7, "%.2f" % (p_.get_height() / p__.get_height()))
plt.ylabel('average time (s)')
plt.title('average time of complete dialogue and uncompleted dialogue and their ratio')
plt.xticks(ind, [cat for cat in cate_cmp_arr], fontproperties=font)
# plt.yticks(np.arange(0, 81, 10))
plt.legend((p1[0], p2[0]), ('average time of complete dialogue', 'average time of uncompleted dialogue'))
plt.show()

# 每个问题退出对话的占比
# all_dial_count = len(que_ans_time_arr_dgn) + len(que_ans_time_arr_no_rst)
# len_dial_dgn = dict(Counter([len(qat) for qat in que_ans_time_arr_dgn]))
# len_dial_dgn = sorted(len_dial_dgn.items(), key=lambda x: x[0])
# len_dial_no_rst = dict(Counter([len(qat) for qat in que_ans_time_arr_no_rst]))
# len_dial_no_rst = sorted(len_dial_no_rst.items(), key=lambda x: x[0])
# # plot it
# ind = np.arange(len_dial_no_rst[-1][0]+1)
# width = 0.6
# prob = []
# for i in range(len(ind)):
#     prob.append(0)
# for _, ld in enumerate(len_dial_no_rst):
#     prob[ld[0]] = ld[1]/all_dial_count*100
#     print(ld[0], ld[1], "%.2f" % (ld[1]/all_dial_count*100) + "%")
#     # all_dial_count = all_dial_count - len_dial_dgn[_][1] - len_dial_no_rst[_][1]
# print(all_dial_count)
# p1 = plt.bar(ind, prob, width)
# for p in p1:
#     x = p.get_x()
#     height = p.get_height()
#     plt.text(x-0.1, height+0.02, "%.2f" % p.get_height())
# plt.ylabel('proportion (%)')
# plt.title('The proportion of quitting on problem X')
# plt.show()
