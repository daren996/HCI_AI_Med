"""
load raw conversation data into format of json with structures:
obj{"对话id": , "用户id": , "年龄": , "性别": , "生理状况": , "注册时间": , "hpi": ,
    "报告": , "主诉": , "反馈id": , "反馈结果": , "反馈内容": , "反馈标签": , "dial": []}
dial[{对话时间, 问题, 选择答案, 输入答案}, ...]

split data set regarding to completeness of dialogue

"""

import json
import re
import random

source_path = "../DataSet/"
data_set_raw = "conversation.tsv"
data_set = "conversation.txt"
out_file_name = "conv.txt"

re_clean = re.compile(u'[\U00010000-\U0010ffff]')


# load raw data : 对话id, 对话时间, 用户id, 年龄, 性别, 生理状况, 注册时间, 问题, 选择答案, 输入答案, hpi,
#                 报告, 主诉, 反馈id, 反馈结果, 反馈内容, 反馈标签
# modulate irregular lines
def load_raw():
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


# into format of json with structures:
# obj{"对话id": , "用户id": , "年龄": , "性别": , "生理状况": , "注册时间": , "hpi": ,
# #                 "报告": , "主诉": , "反馈id": , "反馈结果": , "反馈内容": , "反馈标签": , "dial": []}
# dial[{对话时间, 问题, 选择答案, 输入答案}, ...]
def reformat():
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
                if line_obj["主诉"] and line_obj["主诉"] not in obj["主诉"]  and line_obj["主诉"] != "-":
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


def reload(data_path, out_path):
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


def get_rdm(data_path, out_path, num):
    with open(source_path + data_path) as in_file:
        lines = in_file.readlines()
        choices = random.sample(lines, num)
    with open(source_path + out_path, "w") as out_file:
        for cho in choices:
            out_file.write(cho)


if __name__ == '__main__':
    # load_raw()
    # reformat()
    # reload(out_file_name, 'cvs_convention.txt')
    # get_rdm(out_file_name, 'cvs_1000', 1000)
    # reload('cvs_1000', 'cvs_1000_conventional.txt')
    pass

