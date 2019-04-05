
"""
obj{"对话id": , "用户id": , "年龄": , "性别": , "生理状况": , "注册时间": , "hpi": ,
    "报告": , "主诉": , "反馈id": , "反馈结果": , "反馈内容": , "反馈标签": , "dial": []}
dial[{对话时间, 问题, 选择答案, 输入答案}, ...]

"""

import json


source_path = "../DataSet/"
data_set = "conv.txt"


with open(source_path + data_set, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)




