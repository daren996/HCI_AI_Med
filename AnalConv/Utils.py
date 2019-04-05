import datetime
import json
from collections import Counter
import jieba
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy import interpolate

font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc', size=8)
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

source_path_ = "../DataSet/"
data_set_ = "conv.txt"

reason_group = ['饮食所致', '刺激气体诱发', '饮水所致', '生活行为所致', '行为习惯所致', '异物所致', '矫正过度或不足', '正常生理现象', '医源性损伤', '食物药物所致', '睡姿不正确所致',
                '剧烈运动所致', '心理压力所致', '退行性变化', '饮食习惯所致', '肩关节退化', '疲劳所致', '假性血尿', '超重所致关节受压']
reason_decode = {'饮食所致': '饮食\n所致', '刺激气体诱发': '刺激气\n体诱发', '饮水所致': '饮水\n所致', '生活行为所致': '生活行\n为所致', '行为习惯所致': '行为习\n惯所致',
                 '异物所致': '异物\n所致', '矫正过度或不足': '矫正\n过度\n或不足', '正常生理现象': '正常生\n理现象', '医源性损伤': '医源\n性损伤',
                 '食物药物所致': '食物药\n物所致', '睡姿不正确所致': '睡姿\n不正\n确所致', '剧烈运动所致': '剧烈运\n动所致', '心理压力所致': '心理压\n力所致',
                 '退行性变化': '退行\n性变化', '饮食习惯所致': '饮食习\n惯所致', '肩关节退化': '肩关\n节退化', '疲劳所致': '疲劳\n所致', '假性血尿': '假性\n血尿',
                 '超重所致关节受压': '超重\n所致关\n节受压'}
department_group = ['皮肤性病科', '内分泌与代谢科', '眼科', '心脏与血管外科', '感染科', '神经外科', '骨科', '口腔颌面科', '儿科', '烧伤科', '神经内科', '肾内科',
                    '泌尿外科', '男科', '急诊科', '内科', '整形美容科', '精神科', '耳鼻喉科', '心血管内科', '呼吸内科', '普外科', '风湿免疫科', '肿瘤科', '心理科',
                    '血液病科', '胸外科', '新生儿科', '产科', '妇科', '甲状腺乳腺外科', '消化内科']
department_decode = {'皮肤性病科': '皮肤\n性病科', '内分泌与代谢科': '内分\n泌与\n代谢科', '眼科': '眼科', '心脏与血管外科': '心脏\n与血\n管外科', '感染科': '感染科',
                     '神经外科': '神经\n外科', '骨科': '骨科', '口腔颌面科': '口腔颌\n面科', '儿科': '儿科', '烧伤科': '烧伤科', '神经内科': '神经\n内科',
                     '肾内科': '肾内科', '泌尿外科': '泌尿\n外科', '男科': '男科', '急诊科': '急诊科', '内科': '内科', '整形美容科': '整形\n美容科',
                     '精神科': '精神科',
                     '耳鼻喉科': '耳鼻\n喉科', '心血管内科': '心血管\n内科', '呼吸内科': '呼吸\n内科', '普外科': '普外科', '风湿免疫科': '风湿\n免疫科',
                     '肿瘤科': '肿瘤科',
                     '心理科': '心理科', '血液病科': '血液\n病科', '胸外科': '胸外科', '新生儿科': '新生\n儿科', '产科': '产科', '妇科': '妇科',
                     '甲状腺乳腺外科': '甲状\n腺乳\n腺外科', '消化内科': '消化\n内科'}
eval_rst_group = ['1', '0', 'unknown']
eval_rst_decode = {'1': 'useful', '0': 'useless', 'unknown': 'unknown'}
des_cate = ["胸腰", "肺肝肾", "脑", "眼", "脸", "耳鼻喉咳痰咽", "口牙嘴舌", "腹肚胃", "手脚腿指", "身汗胖", "女乳",
            "性", "尿", "便肛肠", "血", "头晕", "痘", "疮疤疹糜", "肿胀", "睡寐梦醒眠", "孩", "痒", "疼痛", "unknown"]
des_decode = {"胸腰": "腰部\n胸部", "肺肝肾": "肺肝肾和\n心脏", "脑": "大脑", "眼": "眼部", "脸": "脸部", "耳鼻喉咳痰咽": "耳鼻喉",
              "口牙嘴舌": "口腔", "腹肚胃": "腹部肠胃疾病", "手脚腿指": "四肢", "身汗胖": "全身性", "女乳": "女性疾病",
              "性": "性疾病", "尿": "泌尿", "便肛肠": "肛肠", "血": "血液", "头晕": "头晕发烧", "痒": "发痒", "疼痛": "疼痛",
              "痘": "过敏长痘", "疮疤疹糜": "疮疤糜烂", "肿胀": "肿胀", "睡寐梦醒眠": "睡眠质量", "孩": "儿科",
              "unknown": "unknown"}


def age_str2group(age_str):
    if "岁" in age_str:
        tmp = age_str.split('岁')
        year = int(tmp[0])
        return age_num2group(year)
    else:
        return '0~6岁'


def age_num2group(age_num):
    if age_num <= 6:
        return '0~6岁'
    elif age_num <= 15:
        return '7~15岁'
    elif age_num <= 35:
        return '16~35岁'
    elif age_num <= 60:
        return '36~60岁'
    else:
        return '大于60岁'


age_group = ['0~6岁', '7~15岁', '16~35岁', '36~60岁', '大于60岁', 'unknown']
age_decode = {'0~6岁': '0-6 years old', '7~15岁': '7-15 years old', '16~35岁': '16-35 years old',
              '36~60岁': '35-60 years old', '大于60岁': '>60 years old', 'unknown': 'unknown'}


# get time group of a day. format of timeStr: xx:xx:xx
def get_time_group(time_str):
    temp = time_str.split(":")
    tim = int(temp[0])
    if tim < 6:
        return 'night(23-6*)'
    if tim < 12:
        return 'morning(6-12)'
    if tim < 19:
        return 'afternoon(12-19)'
    if tim < 23:
        return 'evening(19-23)'
    else:
        return 'night(23-6*)'


time_group = ['morning(6-12)', 'afternoon(12-19)', 'evening(19-23)', 'night(23-6*)', 'unknown']


# get span group. format of timeStr: xx:xx:xx
def get_span_group(span):
    if span < 2:
        return '0-2'
    if span < 10:
        return '2-10'
    if span < 50:
        return '10-50'
    if span < 100:
        return '50-100'
    if span < 150:
        return '100-150'
    else:
        return '150*'


span_group = ['0-2', '2-10', '10-50', '50-100', '100-150', '150*', 'unknown']
valid_group = ['valid', 'invalid']
gender_group = ['男', '女', 'unknown']
gender_decode = {'男': 'male', '女': 'female', 'unknown': 'unknown'}


def decode(ori, type_):
    if type_ == "age":
        return age_decode[ori]
    elif type_ == "gender":
        return gender_decode[ori]
    elif type_ == 'span':
        return ori
    elif type_ == 'time':
        return ori
    elif type_ == 'eval_rst':
        return eval_rst_decode[ori]
    elif type_ == "description":
        return des_decode[ori]
    elif type_ == 'department':
        return department_decode[ori]
    elif type_ == 'reason':
        return reason_decode[ori]
    else:
        print('ERROR Utils.decode: informal type')
        exit(-1)


# time_str format: 2018-10-14 05:17:40
def datetime_division(time_str1, time_str2):
    date_parts1 = time_str1.split(' ')[0].split('-')
    date_parts2 = time_str2.split(' ')[0].split('-')
    time_parts1 = time_str1.split(' ')[1].split(':')
    time_parts2 = time_str2.split(' ')[1].split(':')
    datetime1 = datetime.datetime(int(date_parts1[0]), int(date_parts1[1]), int(date_parts1[2]),
                                  int(time_parts1[0]), int(time_parts1[1]), int(time_parts1[2]))
    datetime2 = datetime.datetime(int(date_parts2[0]), int(date_parts2[1]), int(date_parts2[2]),
                                  int(time_parts2[0]), int(time_parts2[1]), int(time_parts2[2]))
    return (datetime1 - datetime2).days, (datetime1 - datetime2).seconds


# time_str format: 2018-10-14 05:17:40
def cmp_date(time_str1, time_str2):
    date_parts1 = time_str1.split(' ')[0].split('-')
    date_parts2 = time_str2.split(' ')[0].split('-')
    date1 = datetime.datetime(int(date_parts1[0]), int(date_parts1[1]), int(date_parts1[2]))
    date2 = datetime.datetime(int(date_parts2[0]), int(date_parts2[1]), int(date_parts2[2]))
    return (date1 - date2).days


# format of timeStr: xx:xx:xx
def get_time(time_str):
    temp = time_str.split(":")
    time_sec = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2])
    return time_sec


# get format: Q&A&Time [[(question, answer, time), (...), ...], [...], ...]
def get_que_ans_time_arr(source_path, data_set, ):
    que_ans_time_arr = []
    with open(source_path + data_set, "r") as in_file:
        for line in in_file.readlines():
            obj = json.loads(line)
            qat_arr = []
            for dial in obj["dial"]:
                qat_arr.append((get_time(dial["对话时间"].split(' ')[1]), dial["问题"], dial["选择答案"], dial["输入答案"]))
            que_ans_time = []
            for x in range(1, len(qat_arr)):
                time_dif = qat_arr[x][0] - qat_arr[x - 1][0] + 0  # smooth
                if time_dif < 0:
                    time_dif += 86400
                que_ans_time.append((qat_arr[x][1], qat_arr[x][2], qat_arr[x][3], time_dif))
            que_ans_time_arr.append(que_ans_time)
            # print(que_ans_time)
    return que_ans_time_arr


def get_feature(cross_type, obj):
    cross = "unknown"
    if cross_type == "age":
        age = obj["年龄"]
        cross = age_str2group(age)
    elif cross_type == "gender":
        gender = obj["性别"]
        if gender in gender_group:
            cross = gender
        else:
            cross = 'unknown'
    elif cross_type == "span":
        span = get_time(obj["dial"][-1]["对话时间"].split(' ')[1]) - \
               get_time(obj["dial"][0]["对话时间"].split(' ')[1])
        if span < 0:
            span += 86400
        cross = get_span_group(span)
    elif cross_type == "time":
        cross = get_time_group(obj["dial"][0]["对话时间"].split(' ')[1])
    elif cross_type == "eval_rst":
        if len(obj["反馈结果"]) > 0:
            cross = obj["反馈结果"][0]
        else:
            cross = 'unknown'
    elif cross_type == "department":
        if len(obj["报告"]) > 0:
            dep = obj["报告"][0].split('##')[0].split(' ')[0].split('【')[1].split('--')[-1]
            if dep[-1] == '科':
                cross = dep
            elif dep == "暂无":
                cross = '心血管内科'
    elif cross_type == "reason":
        if len(obj["报告"]) > 0:
            dep = obj["报告"][0].split('##')[0].split(' ')[0].split('【')[1].split('--')[-1]
            if dep[-1] != '科' and dep != "暂无":
                cross = obj["报告"][0].split('】')[0].split('【')[1]
    # elif cross_type == "description":
    #     des = obj["dial"][3]["content"]
    #     des_cut = list(jieba.cut(des, cut_all=True))
    #     cross = get_des_caste(des, des_cut)
    return cross


# get cross dict - type : span, time, age, gender, description
def cross_anl(data_path, cross_group_a, cross_group_b, cross_type_a, cross_type_b):
    cross_arr = {}
    for cgb in cross_group_b:
        cross_arr[cgb] = {}
        for cga in cross_group_a:
            cross_arr[cgb][cga] = 0
    with open(data_path, "r") as data_file:
        for li in data_file.readlines():
            obj = json.loads(li)
            if len(obj["dial"]) < 1:
                continue
            else:
                # get cross and des_cat
                cross_b = get_feature(cross_type_b, obj)
                cross_a = get_feature(cross_type_a, obj)
                for cgb in cross_group_b:
                    if cross_b == cgb and cross_b in cross_group_b and cross_a in cross_group_a:
                        cross_arr[cross_b][cross_a] += 1
    return cross_arr


# plot cross
def plot_cross(cross_arr, cross_group_a, cross_group_b, cross_type_a, cross_type_b, title, x_label):
    labels = [decode(cg[0], cross_type_a) for cg in cross_arr[cross_group_b[0]].items()]
    ca_count = {}  # count of each type a
    for cga in cross_group_a:
        ca_count[cga] = sum([cross_arr[cg][cga] for cg in cross_arr])
    ca_arr = {}
    for cg in cross_group_b:
        ca_arr[cg] = [num[1] for num in cross_arr[cg].items()]
    bar_width = 0.8 / len(cross_group_b)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for _, cg in enumerate(cross_group_b):
        if cross_type_b == 'age':
            ax1.bar(np.arange(len(ca_arr[cg])) + bar_width * _, ca_arr[cg],
                    label=age_decode[cg], alpha=0.8, width=bar_width)
        elif cross_type_b == "gender":
            ax1.bar(np.arange(len(ca_arr[cg])) + bar_width * _, ca_arr[cg],
                    label=gender_decode[cg], alpha=0.8, width=bar_width)
        else:
            ax1.bar(np.arange(len(ca_arr[cg])) + bar_width * _, ca_arr[cg],
                    label=cg, alpha=0.8, width=bar_width)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel('number')
    ax1.set_title(title)
    plt.xticks(np.arange(len(ca_arr[cross_group_b[0]])) + bar_width * (len(cross_arr) - 1) / 2, labels,
               fontproperties=font)
    # for _, num in enumerate(dc_arr[cross_group[0]]):
    #     for __, cg in enumerate(cross_group):
    #         plt.text(_ + bar_width * (__ - 0.5), dc_arr[cg][_] + 1,
    #                  '%s(%.f' % (dc_arr[cg][_], dc_arr[cg][_] / list(dc_count.items())[_][1] * 100) + "%)")
    ax1.set_ylim(0, )
    # ax1.set_xlim(-0.5, )
    ax1.legend()
    plt.show()


gc_group = {'time': time_group, 'span': span_group, 'age': age_group,
            'gender': gender_group, 'description': des_cate, 'eval_rst': eval_rst_group,
            'department': department_group, 'reason': reason_group}


def cross_cmp(cross_type_a, cross_type_b):
    cross_type_a = 'reason'
    cross_type_b = 'gender'
    cross_group_a = gc_group[cross_type_a][:-1]
    cross_group_b = gc_group[cross_type_b][:-1]
    get_que_ans_time_arr(source_path_, data_set_)
    cross_arr = cross_anl(source_path_ + data_set_, cross_group_a, cross_group_b, cross_type_a, cross_type_b)
    print(cross_arr)
    plot_cross(cross_arr, cross_group_a, cross_group_b, cross_type_a, cross_type_b,
               title='Comparison between dialogues of different ' + cross_type_b + '\naccording to ' + cross_type_a,
               x_label='')


if __name__ == '__main__':
    print(datetime_division('2018-10-9 13:04:06', '2018-9-30 12:03:05'))
    # cross_cmp('reason', 'gender')
    pass
