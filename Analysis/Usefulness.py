
"""
obj{"对话id": , "用户id": , "年龄": , "性别": , "生理状况": , "注册时间": , "hpi": ,
    "报告": , "主诉": , "反馈id": , "反馈结果": , "反馈内容": , "反馈标签": , "dial": []}
dial[{对话时间, 问题, 选择答案, 输入答案}, ...]

"""

import json


source_path = "../DataSet/"
data_set = "conv.txt"


user_id = set()
fb_id = []
fb_rst = []
fb_con = []
fb_lab = []
reports = []
with open(source_path + data_set, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        user_id.add(obj["用户id"])
        fb_id.append(obj["反馈id"])
        fb_rst.append(obj["反馈结果"])
        fb_con.append(obj["反馈内容"])
        fb_lab.append(obj["反馈标签"])
        reports.append(obj["报告"])
        for con in obj["反馈内容"]:
            if "test" in con or "测试" in con:
                print(obj)
user_count = 0
for id_ in user_id:
    user_count += 1
print("user count ", user_count)

rst_count0 = 0
rst_count1 = 0
for id_, rst, con, lab in zip(fb_id, fb_rst, fb_con, fb_lab):
    for rs in rst:
        if rs == '0':
            rst_count0 += 1
        elif rs == '1':
            rst_count1 += 1
    # for la in lab:
    #     if "#" in la:
    #         tmp = la.split("#")
    #         for tm in tmp:
    #             print(tm)
    #     else:
    #         print(la)
print("0:", rst_count0, "%.3f  1:" % (rst_count0/(rst_count0+rst_count1)), rst_count1, "%.3f" % (rst_count1/(rst_count0+rst_count1)))

rep_count = 0
for rep in reports:
    if len(rep) > 0:
        rep_count += 1
    # if len(rep) > 1:
    #     print(rep)
print("rep", rep_count)


