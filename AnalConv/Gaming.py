"""

Analyze gaming behavior
Gaming detector

data format:
obj{"对话id": , "用户id": , "年龄": , "性别": , "生理状况": , "注册时间": , "hpi": ,
    "报告": , "主诉": , "反馈id": , "反馈结果": , "反馈内容": , "反馈标签": , "dial": []}
dial[{对话时间, 问题, 选择答案, 输入答案}, ...]

"""

import json
import pandas as pd
from pandas import Series, DataFrame
import statsmodels.api as sm
import copy
import pylab as pl
import numpy as np
from sklearn.metrics import auc
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy import interpolate

font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc', size=8)
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

import Utils

source_path_ = "../DataSet/"
data_set_ = "cvs_1000"  # "conv_normal.txt"
data_set_j = "gaming_1000_jhx.txt"
data_set_c = "gaming_1000_cdr.txt"


def get_id_set(source_path, data_path):
    id_arr = []
    with open(source_path + data_path, 'r') as in_file:
        line = in_file.readline()
        while line:
            id_l = line.split(' ')[0]
            id_arr.append(id_l)
            # print(id_)
            while len(line) > 10:
                line = in_file.readline()
            line = in_file.readline()
    return id_arr


def get_feature(feature_type, obj):
    span = Utils.get_time(obj["dial"][-1]["对话时间"].split(' ')[1]) - \
           Utils.get_time(obj["dial"][0]["对话时间"].split(' ')[1])
    if span < 0:
        span += 86400
    if feature_type == 'rounds':
        return len(obj["dial"])
    elif feature_type == 'age':
        if '岁' in obj["年龄"]:
            return int(obj["年龄"].split('岁')[0])
        else:
            return 0
    elif feature_type == 'span':
        return span
    elif feature_type == 'gender':
        gender = obj["性别"]
        if gender == '男':
            return 1
        else:
            return 0
    elif feature_type == 'time':
        return int(obj["dial"][0]["对话时间"].split(' ')[1].split(':')[0])
    elif feature_type == 'ave_span':
        return span / len(obj["dial"])
    elif feature_type == 'span_std':
        span_arr = []
        for _, dial in enumerate(obj["dial"][1:]):
            days, seconds = Utils.datetime_division(dial["对话时间"], obj["dial"][_]["对话时间"])
            if days == 1 and seconds < 0:
                seconds += 86400
            span_arr.append(seconds)
        if len(span_arr) > 0:
            return np.std(np.array(span_arr))
        else:
            return -1
    elif feature_type == 'unclear':  # continuous unclear or nothing
        unclear = 0
        for dial in obj["dial"]:
            if "不清楚" in dial["选择答案"] or "不清楚" in dial["输入答案"] or \
                    "都没有" in dial["选择答案"] or "都没有" in dial["输入答案"]:
                unclear += 1
        return unclear
    elif feature_type == 'department':
        dep = 'unknown'
        if len(obj["报告"]) > 0:
            tmp = obj["报告"][0].split('##')[0].split(' ')[0].split('【')[1].split('--')[-1]
            if tmp[-1] == '科':
                dep = tmp
            elif tmp == "暂无":
                dep = '心血管内科'
            else:
                temp__ = obj["报告"][0].split('##')[0].split(' ')[0].split('【')[1].split('--')[-1]
                if temp__[-1] != '科' and temp__ != "暂无":
                    dep = obj["报告"][0].split('】')[0].split('【')[1]
        if dep != 'unknown':
            return (Utils.department_group + Utils.reason_group).index(dep)
        else:
            return -1
    elif feature_type == 'index':
        return 1
    else:
        print("ERROR unknown feature:", feature_type)
        return -1


def get_data_frame(source_path, data_path, columns):
    gaming_id_arr = set(get_id_set(source_path, data_set_c) + get_id_set(source_path, data_set_j))
    count_gaming = 0
    data_raw = {}
    for col in columns:
        data_raw[col] = []
    with open(source_path + data_path, 'r') as in_file:
        for line in in_file.readlines():
            obj = json.loads(line.strip())
            for col in columns[:-1]:
                data_raw[col].append(get_feature(col, obj))
            if obj["对话id"] in gaming_id_arr:
                is_gaming = 1
                count_gaming += 1
            else:
                is_gaming = 0
            data_raw['is_gaming'].append(is_gaming)
    print("gaming", count_gaming)
    return data_raw


def get_gaming_data_frame(source_path, data_path, columns):
    gaming_id_arr = set(get_id_set(source_path, data_set_c) + get_id_set(source_path, data_set_j))
    gaming_data_raw = {}
    gaming_count = 0
    for col in columns:
        gaming_data_raw[col] = []
    with open(source_path + data_path, 'r') as in_file:
        for line in in_file.readlines():
            obj = json.loads(line.strip())
            if obj["对话id"] in gaming_id_arr:
                for col in columns[:-1]:
                    gaming_data_raw[col].append(get_feature(col, obj))
                gaming_data_raw['is_gaming'].append(1)
                gaming_count += 1
    print("gaming count", gaming_count)
    return gaming_data_raw


def log_reg(data, columns):
    train_cols = data.columns[:-1]
    logit = sm.Logit(data[columns[-1]], data[train_cols])
    result = logit.fit()
    return result


def get_pre(result, data_pre):
    predict_cols = data_pre.columns[:-1]
    data_pre['predict'] = result.predict(data_pre[predict_cols])
    return data_pre


def get_hit(data_pre, threshold):
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for value in data_pre[['predict', 'is_gaming']].values:
        predict = value[0]
        gaming = value[1]
        if predict > threshold:  # positive
            if gaming == 1:  # true positive
                tp += 1
            else:  # false positive
                fp += 1
        else:  # negative
            if gaming == 1:  # true negative
                fn += 1
            else:  # false negative
                tn += 1
    if (tp + fp) == 0:
        return 0, tp / (tp + fn), fp / (fp + tn)
    # return : best_acc, best_recall, best_fpr
    return tp / (tp + fp), tp / (tp + fn), fp / (fp + tn)


def get_best_threshold(data_pre):
    thr = 0.002
    best_thr = 0.001
    best_acc, best_recall, best_fpr = get_hit(data_pre, best_thr)
    while thr < 0.5:
        cur_acc, cur_recall, cur_fpr = get_hit(data_pre, thr)
        # print("threshold: %.4f, acc: %.4f, rec: %.4f" % (thr, cur_acc, cur_recall))
        # if cur_acc > best_acc:
        # if cur_recall > best_recall:
        if cur_acc * cur_recall > best_acc * best_recall:
            best_acc = cur_acc
            best_recall = cur_recall
            best_thr = thr
            # print("change to %.4f" % thr)
        thr += 0.001
    return best_thr, best_acc, best_recall


def recall_acc_arr(data_pre):
    rec_arr = []
    fpr_arr = []
    width = 0.001
    thr = 0.001
    while thr < 0.315:
        cur_acc, cur_recall, cur_fpr = get_hit(data_pre, thr)
        rec_arr.append(cur_recall)
        fpr_arr.append(cur_fpr)
        thr += width
    return rec_arr, fpr_arr


if __name__ == '__main__':
    # id_c = get_id_set(source_path_, data_set_c)
    # id_j = get_id_set(source_path_, data_set_j)
    pass

    # columns_ = ['name', 'marks', 'price']
    # data_raw_ = {"name": [10, 25, 45, 40], "marks": [60, 50, 200, 450], "price": [0, 0, 1, 1]}
    # columns_ = ['rounds', 'age', 'span', 'gender', 'time', 'ave_span', 'is_gaming']
    # columns_ = ['rounds', 'age', 'span', 'gender', 'time', 'ave_span', 'span_std', 'is_gaming']
    # columns_ = ['index', 'span', 'gender', 'time', 'ave_span', 'span_std', 'is_gaming']
    # columns_ = ['index', 'span', 'gender', 'time', 'ave_span', 'span_std', 'unclear', 'is_gaming']
    columns_ = ['index', 'gender', 'span', 'time', 'ave_span', 'span_std', 'unclear', 'department', 'is_gaming']
    data_raw_ = get_data_frame(source_path_, data_set_, columns_)
    gaming_data_raw_ = get_gaming_data_frame(source_path_, data_set_, columns_)
    data_ = DataFrame(data_raw_, columns=columns_)
    gaming_data_ = DataFrame(gaming_data_raw_, columns=columns_)
    print(data_.columns)
    # print(data_.describe())
    result_ = log_reg(data_, columns_)
    data_pre_ = get_pre(result_, copy.deepcopy(data_))
    print("all data:\n", data_pre_[['predict', 'is_gaming']].describe())
    gaming_data_pre_ = get_pre(result_, copy.deepcopy(gaming_data_))
    print("gaming data:\n", gaming_data_pre_['predict'].describe())

    best_thr_, best_hit_, best_recall_ = get_best_threshold(data_pre_)
    print("best threshold: %.4f, acc: %.4f, rec: %.4f" % (best_thr_, best_hit_, best_recall_))

    rec_arr_, fpr_arr_ = recall_acc_arr(data_pre_)
    fpr_rec_arr_ = [(fpr_arr_[__], rec) for __, rec in enumerate(rec_arr_)]
    fpr_rec_arr_ = sorted(fpr_rec_arr_, key=lambda x: x[0])
    fpr_rec_arr_ = [(0, 0)] + fpr_rec_arr_

    # auc = auc([0, 0, 1, 0, 1, 0, 0], [1.1, 0.2, 3.4, 5.1, 2.1, 0.4, 2.4])
    auc = auc([fra[0] for fra in fpr_rec_arr_], [fra[1] for fra in fpr_rec_arr_])
    plt.plot([fra[0] for fra in fpr_rec_arr_], [fra[1] for fra in fpr_rec_arr_])
    plt.xlabel('fpr')
    plt.ylabel('rec')
    plt.title('roc: fpr and rec, auc / area: %.4f' % auc + '\n' + ', '.join(columns_[1:-1]))
    plt.show()

    # data_pre_['predict'].hist()
    # pl.show()


