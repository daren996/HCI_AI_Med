
import json
import re
import random
import Utils

"""
three kinds of formats:
raw format, new format and conventional format

new format:
obj{"对话id": , "用户id": , "年龄": , "性别": , "生理状况": , "注册时间": , "hpi": ,
    "报告": , "主诉": , "反馈id": , "反馈结果": , "反馈内容": , "反馈标签": , "dial": []}
dial[{对话时间, 问题, 选择答案, 输入答案}, ...]


break adhesion conversations
cohere broken ones
remove abnormal ones

latest data set is: conv_normal.txt

"""

source_path_ = "../DataSet/"
data_set_raw_ = "conversation.tsv"
data_set_ = "conversation.txt"
data_set_adhesion_ = "conversation_adhesion.txt"
data_set_cohesion_ = "conversation_cohesion.txt"
out_file_name_ = "conv.txt"
out_file_name_adhesion_ = "conv_adhesion.txt"
out_file_name_cohesion_ = "conv_cohesion.txt"
out_file_name_cohesion_no_abnormal_ = "conv_normal.txt"
gaming_file_name_ = "cvs_1000_gaming.txt"

re_clean = re.compile(u'[\U00010000-\U0010ffff]')


# load raw data : 对话id, 对话时间, 用户id, 年龄, 性别, 生理状况, 注册时间, 问题, 选择答案, 输入答案, hpi,
#                 报告, 主诉, 反馈id, 反馈结果, 反馈内容, 反馈标签
# modulate irregular lines
def load_raw(source_path, data_set_raw, data_set):
    count_all = 0
    out_file = open(source_path + data_set, "w")  # , encoding="utf-8")
    with open(source_path + data_set_raw, "r", encoding="utf-8") as in_file:
        labels_str = in_file.readline()
        labels = labels_str.split('\t')
        line = in_file.readline()
        while line:
            temp = line.split('\t')
            while len(temp) < len(labels):
                last_line = line
                line = in_file.readline()
                line = last_line[:-1] + line
                temp = line.split('\t')
            if len(temp) is not len(labels):
                print("ERROR: ", line.strip())
            obj = {}
            for _, lab in enumerate(labels):
                obj[lab.strip()] = temp[_].strip()
            count_all += 1
            out_file.write(json.dumps(obj, ensure_ascii=False) + '\n')
            line = in_file.readline()
    out_file.close()
    print("count of all", count_all)  # 643140


# reformat into format of json with structures:
# obj{"对话id": , "用户id": , "年龄": , "性别": , "生理状况": , "注册时间": , "hpi": ,
# #                 "报告": , "主诉": , "反馈id": , "反馈结果": , "反馈内容": , "反馈标签": , "dial": []}
# dial[{对话时间, 问题, 选择答案, 输入答案}, ...]
def reformat(source_path, data_set, out_file_name):
    count_id = 0
    out_file = open(source_path + out_file_name, "w")  # , encoding="utf-8")
    with open(source_path + data_set, "r") as in_file:
        line = in_file.readline()
        line_obj_last = json.loads(line)
        id_last = line_obj_last["对话id"]
        obj = {"对话id": line_obj_last["对话id"], "用户id": line_obj_last["用户id"], "年龄": line_obj_last["年龄"],
               "性别": line_obj_last["性别"], "生理状况": line_obj_last["生理状况"], "注册时间": line_obj_last["注册时间"],
               "hpi": [], "报告": [], "主诉": [],
               "反馈id": [], "反馈结果": [], "反馈内容": [],
               "反馈标签": [], "dial": []}
        while line:
            line_obj = json.loads(line)
            id_ = line_obj["对话id"]
            if id_ == id_last:
                if line_obj["hpi"] and line_obj["hpi"] != "-":
                    obj["hpi"].append(line_obj["hpi"])
                if line_obj["报告"] and line_obj["报告"] != "-":
                    obj["报告"].append(line_obj["报告"])
                if line_obj["主诉"] and line_obj["主诉"] not in obj["主诉"] and line_obj["主诉"] != "-":
                    obj["主诉"].append(line_obj["主诉"])
                if line_obj["反馈id"] and line_obj["反馈id"] != "-":
                    obj["反馈id"].append(line_obj["反馈id"])
                if line_obj["反馈结果"] and line_obj["反馈结果"] != "-":
                    obj["反馈结果"].append(line_obj["反馈结果"])
                if line_obj["反馈内容"] and line_obj["反馈内容"] != "-":
                    obj["反馈内容"].append(line_obj["反馈内容"])
                if line_obj["反馈标签"] and line_obj["反馈标签"] != "-":
                    obj["反馈标签"].append(line_obj["反馈标签"])
                obj["dial"].append({"对话时间": line_obj["对话时间"], "问题": line_obj["问题"],
                                    "选择答案": line_obj["选择答案"], "输入答案": line_obj["输入答案"]})
            else:
                out_file.write(json.dumps(obj, ensure_ascii=False) + "\n")
                count_id += 1
                obj = {"对话id": line_obj["对话id"], "用户id": line_obj["用户id"], "年龄": line_obj["年龄"],
                       "性别": line_obj["性别"], "生理状况": line_obj["生理状况"], "注册时间": line_obj["注册时间"],
                       "hpi": [], "报告": [], "主诉": [],
                       "反馈id": [], "反馈结果": [], "反馈内容": [],
                       "反馈标签": [], "dial": []}
                if line_obj["hpi"] and line_obj["hpi"] != "-":
                    obj["hpi"].append(line_obj["hpi"])
                if line_obj["报告"] and line_obj["报告"] != "-":
                    obj["报告"].append(line_obj["报告"])
                if line_obj["主诉"] and line_obj["主诉"] not in obj["主诉"] and line_obj["主诉"] != "-":
                    obj["主诉"].append(line_obj["主诉"])
                if line_obj["反馈id"] and line_obj["反馈id"] != "-":
                    obj["反馈id"].append(line_obj["反馈id"])
                if line_obj["反馈结果"] and line_obj["反馈结果"] != "-":
                    obj["反馈结果"].append(line_obj["反馈结果"])
                if line_obj["反馈内容"] and line_obj["反馈内容"] != "-":
                    obj["反馈内容"].append(line_obj["反馈内容"])
                if line_obj["反馈标签"] and line_obj["反馈标签"] != "-":
                    obj["反馈标签"].append(line_obj["反馈标签"])
                obj["dial"].append({"对话时间": line_obj["对话时间"], "问题": line_obj["问题"],
                                    "选择答案": line_obj["选择答案"], "输入答案": line_obj["输入答案"]})
            id_last = id_
            line = in_file.readline()
    print("count of id", count_id)  # 47684


# reload data into conventional format
def reload(source_path, data_path, out_path):
    reload_file = open(source_path + out_path, "w")
    with open(source_path + data_path) as in_file:
        for line in in_file.readlines():
            obj = json.loads(line.strip())
            reload_file.write(obj["对话id"] + " " + ' '.join(obj["主诉"]) + "\n")
            for dial in obj["dial"]:
                reload_file.write(dial["对话时间"] + " Robot ")
                reload_file.write(dial["问题"] + "\n")
                reload_file.write(dial["对话时间"] + " User  ")
                reload_file.write(dial["选择答案"] + " ")
                reload_file.write(dial["输入答案"] + "\n")
            reload_file.write("\n\n")
    reload_file.close()


# from id from conventional format
def get_conventional_id(source_path, data_set_arr, ):
    id_set = set()
    for data_set in data_set_arr:
        with open(source_path + data_set, "r", encoding="utf-8") as in_file:
            line = in_file.readline()
            while line:
                id_ = line.split(' ')[0]
                # if id_ in id_set:
                #     print("duplicate", id_)
                id_set.add(id_)
                # print(id_)
                while len(line) > 10:
                    line = in_file.readline()
                line = in_file.readline()
    print("get %d ids" % len(id_set))
    return id_set


# reload data with selected ids into conventional format
def user_id_reload(source_path, data_path, out_path, id_set, write_type='w'):
    reload_file = open(source_path + out_path, write_type)
    with open(source_path + data_path) as in_file:
        for line in in_file.readlines():
            obj = json.loads(line.strip())
            if obj["用户id"] in id_set:
                reload_file.write(obj["对话id"] + " " + obj["用户id"] + ' ' + ' '.join(obj["主诉"]) + "\n")
                for dial in obj["dial"]:
                    reload_file.write(dial["对话时间"] + " Robot ")
                    reload_file.write(dial["问题"] + "\n")
                    reload_file.write(dial["对话时间"] + " User  ")
                    reload_file.write(dial["选择答案"] + " ")
                    reload_file.write(dial["输入答案"] + "\n")
                reload_file.write("\n")
    reload_file.close()


# reload data with selected ids into conventional format
def id_reload(source_path, data_path, out_path, id_set, write_type='w'):
    reload_file = open(source_path + out_path, write_type)
    with open(source_path + data_path) as in_file:
        for line in in_file.readlines():
            obj = json.loads(line.strip())
            if obj["对话id"] in id_set:
                reload_file.write(obj["对话id"] + " " + ' '.join(obj["主诉"]) + "\n")
                for dial in obj["dial"]:
                    reload_file.write(dial["对话时间"] + " Robot ")
                    reload_file.write(dial["问题"] + "\n")
                    reload_file.write(dial["对话时间"] + " User  ")
                    reload_file.write(dial["选择答案"] + " ")
                    reload_file.write(dial["输入答案"] + "\n")
                reload_file.write("\n")
    reload_file.close()


def get_rdm(source_path, data_path, out_path, num):
    with open(source_path + data_path) as in_file:
        lines = in_file.readlines()
        choices = random.sample(lines, num)
    with open(source_path + out_path, "w") as out_file:
        for cho in choices:
            out_file.write(cho)


# break adhesion conversation in raw data set: add count in their ids
def raw_break_adhesion(source_path, data_path, out_path, ):
    out_file = open(source_path + out_path, "w")  # , encoding="utf-8")
    with open(source_path + data_path) as in_file:
        lines = in_file.readlines()
        count = 1
        for _, line in enumerate(lines[1:]):
            obj = json.loads(line.strip())
            id_ = obj["对话id"]
            if id_ == json.loads(lines[_])["对话id"]:
                days, seconds = Utils.datetime_division(obj["对话时间"], json.loads(lines[_])["对话时间"])
                if (days > 1 or (days < 1 and seconds > 3600)) and ('您已进入智能' in obj["问题"]):
                    count += 1
                obj["对话id"] += "%d" % count
            else:
                count = 1
                obj["对话id"] += "%d" % count
            out_file.write(json.dumps(obj, ensure_ascii=False) + '\n')
    out_file.close()


# get adhesion conversations
def get_adhesion(source_path, data_path, out_path='cvs_adhesion.txt', ):
    id_set = set()
    with open(source_path + data_path) as in_file:
        for line in in_file.readlines():
            obj = json.loads(line.strip())
            if obj["对话id"] in id_set:
                print("ERROR: duplicate id -", obj["对话id"])
            id_set.add(obj["对话id"])
    count = 0
    id_adhesion_set = set()
    with open(source_path + data_path) as in_file:
        for line in in_file.readlines():
            obj = json.loads(line.strip())
            for _, dial in enumerate(obj["dial"][1:]):
                days, seconds = Utils.datetime_division(dial["对话时间"], obj["dial"][_]["对话时间"])
                # criterion for adhesion
                if (days < 1 and seconds > 3600 and '您已进入智能' in dial["问题"]) or (days < 0 and seconds < 0):
                    # print(obj["对话id"], len(obj['hpi']), len(obj["报告"]))
                    # print(dial["问题"])
                    count += 1
                    id_adhesion_set.add(obj["对话id"])
    print("adhesion", count)
    # id_reload(source_path, data_path, out_path, id_adhesion_set)


# cohere broken conversations
def get_cohesion(source_path, conversation_data_path, conv_data_path, out_path, ):
    id_transfer = get_cohesion_trasnfer(source_path, conv_data_path)
    # id_abnormal_set, id_ending_set = get_abnormal(source_path, data_path)
    id2obj = {}
    with open(source_path + conversation_data_path) as in_file:
        for line in in_file.readlines():
            obj = json.loads(line.strip())
            if obj["对话id"] in id_transfer:
                obj["对话id"] = id_transfer[obj["对话id"]]
                if obj["对话id"] not in id2obj:
                    id2obj[obj["对话id"]] = []
                id2obj[obj["对话id"]].append(obj)
            else:
                if obj["对话id"] not in id2obj:
                    id2obj[obj["对话id"]] = []
                id2obj[obj["对话id"]].append(obj)
    with open(source_path + out_path, 'w') as out_file:
        for id_ in id2obj:
            obj_arr = id2obj[id_]
            obj_arr = sorted(obj_arr, key=lambda x: Utils.datetime_division(x["对话时间"], '2017-10-04 0:0:0')[1] +
                                    86400 * Utils.datetime_division(x["对话时间"], '2017-10-04 0:0:0')[0])  # sort
            for obj in obj_arr:
                out_file.write(json.dumps(obj, ensure_ascii=False) + '\n')


# cohere broken conversations | 这个属于偷懒的做法了 ***
def get_cohesion_trasnfer(source_path, conv_data_path, out_path='cvs_cohesion.txt', ):
    _, id_ending_set = get_abnormal(source_path, conv_data_path)
    id2time_abnormal_dic = {}
    with open(source_path + conv_data_path) as in_file:
        for line in in_file.readlines():
            obj = json.loads(line.strip())
            if obj["对话id"] in id_ending_set:
                id2time_abnormal_dic[obj["用户id"]] = []
                id2time_abnormal_dic[obj["用户id"]].append([obj["dial"][0]["对话时间"], obj["dial"][-1]["对话时间"], obj["对话id"]])
    count = 0
    id_cohesion_set = set()
    id_transfer = {}
    with open(source_path + conv_data_path) as in_file:
        for line in in_file.readlines():
            obj = json.loads(line.strip())
            if obj["用户id"] in id2time_abnormal_dic and obj["对话id"] not in id_ending_set:
                for abs_time in id2time_abnormal_dic[obj["用户id"]]:
                    ab_time0 = abs_time[0]
                    # ab_time1 = abs_time[1]
                    # days0, seconds0 = Utils.datetime_division(obj["dial"][0]["对话时间"], ab_time1)
                    days1, seconds1 = Utils.datetime_division(ab_time0, obj["dial"][-1]["对话时间"])
                    if days1 == 0 and 0 <= seconds1 < 180:
                        # id_reload(source_path, data_path, out_path, {abs_time[2], obj["对话id"]}, write_type='a')
                        id_cohesion_set.add(obj["对话id"])
                        id_cohesion_set.add(abs_time[2])
                        # user_id_reload(source_path, data_path, 'user_id_' + obj["用户id"] + '.txt', [obj["用户id"]])
                        id_transfer[abs_time[2]] = obj["对话id"]
                        count += 1
                        break
    print("cohesion", count)
    # id_reload(source_path, data_path, out_path, id_cohesion_set)
    return id_transfer


# get abnormal / ending ids set
def get_abnormal(source_path, conv_data_path, out_path='NOTHING', ):
    count = 0
    count_abnormal = 0
    count_both = 0
    id_ending_set = set()
    id_abnormal_set = set()
    with open(source_path + conv_data_path, 'r') as in_file:
        for line in in_file.readlines():
            obj = json.loads(line.strip())
            is_abnormal = True
            has_greeting = False
            has_ending = False
            for _, dial in enumerate(obj["dial"]):
                if "您已进入智能" in dial["问题"]:
                    has_greeting = True
                if "谢谢您的回答" in dial["问题"]:
                    has_ending = True
            for _, dial in enumerate(obj["dial"][1:]):
                days, seconds = Utils.datetime_division(dial["对话时间"], obj["dial"][_]["对话时间"])
                if days < 0 or seconds < 0:
                    print("ERROR time order", obj["对话id"])
            if has_ending and has_greeting:
                count_both += 1
            if has_ending and not has_greeting:
                id_ending_set.add(obj["对话id"])
            if has_greeting:
                is_abnormal = False
            if is_abnormal:
                count_abnormal += 1
                id_abnormal_set.add(obj["对话id"])
            count += 1
    print("abnormal:", count_abnormal, end=' ')
    print("has greeting and ending:", count_both, end=' ')
    print("all:", count)
    # id_reload(source_path, data_path, out_path, id_abnormal_set)
    return id_abnormal_set, id_ending_set


def remove_abnormal(source_path, conv_data_path, out_path, gaming_path=gaming_file_name_):
    id_abnormal_set, __ = get_abnormal(source_path, conv_data_path)
    gaming_id_set = get_gaming_id(source_path, conv_data_path, gaming_path)
    with open(source_path + out_path, 'w') as out_file:
        with open(source_path + conv_data_path, 'r') as in_file:
            for line in in_file.readlines():
                obj = json.loads(line.strip())
                if obj["对话id"] not in id_abnormal_set and obj["对话id"] not in gaming_id_set:
                    out_file.write(line)


def get_gaming_id(source_path, conv_data_path, gaming_path, ):
    count_gaming_id = 0
    count_gaming = 0
    gaming_id_set = set()
    result_id_set = set()
    with open(source_path + gaming_path, 'r') as in_file:
        line = in_file.readline()
        while line:
            id_l = line.split(' ')[0]
            gaming_id_set.add(id_l)
            count_gaming_id += 1
            # print(id_)
            while len(line) > 10:
                line = in_file.readline()
            line = in_file.readline()
    print("gaming id:", count_gaming_id, end=' ')
    with open(source_path + conv_data_path, 'r') as in_file:
        for line in in_file.readlines():
            obj = json.loads(line.strip())
            if obj["对话id"][:-1] in gaming_id_set:
                count_gaming += 1
                result_id_set.add(obj["对话id"])
    print("gaming conversations:", count_gaming)
    # print(set([gis for gis in gaming_id_set]) - set([ris[:-1] for ris in result_id_set]))
    return result_id_set


data_set_j = "gaming_1000_jhx.txt"
data_set_c = "gaming_1000_cdr.txt"

if __name__ == '__main__':
    # load_raw(source_path_, data_set_raw_, data_set_)
    # reformat(source_path_, data_set_cohesion_, out_file_name_cohesion_)
    # reload(source_path_, out_file_name_, 'cvs_convention.txt')
    # get_rdm(source_path_, out_file_name_, 'cvs_1000', 1000)
    # reload(source_path_, 'cvs_1000', 'cvs_1000_conventional.txt')
    # id_set_ = get_conventional_id(source_path_, [data_set_c, data_set_j])
    # id_reload(source_path_, out_file_name_, 'cvs_1000_gaming.txt', id_set_)
    # raw_break_adhesion(source_path_, data_set_, data_set_adhesion_)
    # reformat(source_path_, data_set_adhesion_, out_file_name_adhesion_)
    # get_adhesion(source_path_, out_file_name_cohesion_, )
    # get_cohesion_trasnfer(source_path_, out_file_name_cohesion_, )
    # get_cohesion(source_path_, data_set_adhesion_, out_file_name_adhesion_, data_set_cohesion_)
    # get_abnormal(source_path_, out_file_name_cohesion_, )
    # remove_abnormal(source_path_, out_file_name_cohesion_, out_file_name_cohesion_no_abnormal_)
    get_adhesion(source_path_, out_file_name_cohesion_no_abnormal_, )
    get_cohesion_trasnfer(source_path_, out_file_name_cohesion_no_abnormal_, )
    get_gaming_id(source_path_, out_file_name_cohesion_no_abnormal_, gaming_file_name_)
    pass

