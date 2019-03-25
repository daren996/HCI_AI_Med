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

font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc', size=8)
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

source_path = "../DataSet/"
data_set = "dial.txt"


# get description category distribution
def get_distribution(des_group):
    des_all = []
    des_cat = {}
    des_cat_dis = {}
    for dc in des_group:
        des_cat_dis[dc] = 0
        des_cat[dc] = []
    # des_cat_dis['unknown'] = 0
    # des_cat['unknown'] = []
    dial_count = 0
    with open(source_path + data_set, "r") as in_file:
        for line in in_file.readlines():
            obj = json.loads(line)
            if len(obj["dial"]) > 2:
                dial_count += 1
                cat_arr = Utils.get_cross("description", obj)
                des = obj["dial"][3]["content"]
                for cat in cat_arr:
                    if cat in des_group:
                        des_cat_dis[cat] += 1
                        des_cat[cat].append(des)
                        # if cat == 'unknown':
                        #     print(des)
    print(des_cat_dis)
    des_cat_dis_sorted = sorted(des_cat_dis.items(), key=lambda x: x[1], reverse=True)
    # for cat in des_cat:
    #     print(cat, des_cat_dis[cat], Utils.des_decode[cat])
    #     for des in des_cat[cat]:
    #         print("\t" + des)
    #     print()
    # plot distribution
    plt.bar(np.arange(len(des_cat_dis_sorted)), [dcd[1] for dcd in des_cat_dis_sorted])
    plt.xlabel('category')
    plt.ylabel('distribution')
    plt.title('The distribution of category of description')
    for _, des_num in enumerate(des_cat_dis_sorted):
        plt.text(_ - 0.5, des_num[1] + 0.5,
                 Utils.des_decode[des_num[0]] + ":%d" % (des_num[1]/dial_count*100) + "%",
                 fontproperties=font)
    plt.show()


# get description category xxx cross dict - xxx : span, time, age, gender
def cross_anl_des(cross_group, data_path, cross_type):
    des_group_arr = {}
    for cg in cross_group:
        des_group_arr[cg] = {}
        for dc in Utils.des_cate:
            des_group_arr[cg][dc] = 0
    des_group_arr["unknown"] = {}
    for dc in Utils.des_cate:
        des_group_arr["unknown"][dc] = 0
    with open(data_path, "r") as data_file:
        for li in data_file.readlines():
            obj = json.loads(li)
            if len(obj["dial"]) < 3:
                continue
            else:
                # get cross and des_cat
                cross = Utils.get_cross(cross_type, obj)
                des = obj["dial"][3]["content"]
                des_cut = list(jieba.cut(des, cut_all=True))
                cat_arr = Utils.get_des_caste(des, des_cut)
                for cat in cat_arr:
                    for cg in cross_group:
                        if cross == cg:
                            des_group_arr[cross][cat] += 1
                    if cross == "unknown":
                        des_group_arr['unknown'][cat] += 1
    return des_group_arr


# plot cross
def plot_cross_des(des_group_arr, cross_group, cross_type, title, x_label):
    labels = [Utils.des_decode[num[0]] for num in des_group_arr[cross_group[0]].items()]
    dc_count = {}  # count of each dc
    for dc in Utils.des_cate:
        dc_count[dc] = sum([des_group_arr[cg][dc] for cg in des_group_arr])
    dc_arr = {}
    for cg in cross_group:
        dc_arr[cg] = [num[1] for num in des_group_arr[cg].items()]
    bar_width = 0.8 / len(cross_group)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for _, cg in enumerate(cross_group):
        if cross_type == 'age':
            ax1.bar(np.arange(len(dc_arr[cg])) + bar_width * _, dc_arr[cg],
                    label=Utils.age_decode[cg], alpha=0.8, width=bar_width)
        elif cross_type == "gender":
            ax1.bar(np.arange(len(dc_arr[cg])) + bar_width * _, dc_arr[cg],
                    label=Utils.gender_decode[cg], alpha=0.8, width=bar_width)
        else:
            ax1.bar(np.arange(len(dc_arr[cg])) + bar_width * _, dc_arr[cg],
                    label=cg, alpha=0.8, width=bar_width)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel('number')
    ax1.set_title(title)
    plt.xticks(np.arange(len(dc_arr[cross_group[0]])) + bar_width * (len(des_group_arr) - 1) / 2, labels,
               fontproperties=font)
    # for _, num in enumerate(dc_arr[cross_group[0]]):
    #     for __, cg in enumerate(cross_group):
    #         plt.text(_ + bar_width * (__ - 0.5), dc_arr[cg][_] + 1,
    #                  '%s(%.f' % (dc_arr[cg][_], dc_arr[cg][_] / list(dc_count.items())[_][1] * 100) + "%)")
    ax1.set_ylim(0, )
    ax1.set_xlim(-0.5, )
    ax1.legend()
    plt.show()


dc_group = {'time': Utils.time_group, 'span': Utils.span_group, 'age': Utils.age_group, 'gender': Utils.gender_group}

if __name__ == '__main__':
    des_gro = Utils.des_cate[:-3]
    get_distribution(des_gro)
    # cross_type = 'time'  # time, span, age, gender
    # des_cross_group_arr = cross_anl_des(dc_group[cross_type], source_path + data_set, cross_type=cross_type)
    # print(des_cross_group_arr)
    # plot_cross_des(des_cross_group_arr, dc_group[cross_type], cross_type=cross_type,
    #                title='Comparison between dialogues of different ' + cross_type +
    #                      '\naccording to descriptions categories', x_label='')
