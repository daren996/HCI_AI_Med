
"""
load raw data into format of json with structures:
obj{"id": id, "dial": dial}
dial[{"time": time, "speaker": speaker, "content": content}, ...]

split data set regarding to completeness of dialogue

"""

import json
import re
import random

source_path = "../DataSet/"
data_set = "gaming.txt"
out_file_name = "dial_gaming.txt"

re_clean = re.compile(u'[\U00010000-\U0010ffff]')


# load raw data into format of json with structures:
# obj{"id": id, "dial": dial}; dial[{"time": time, "speaker": speaker, "content": content}, ...]
dial_all = []
out_file = open(source_path + out_file_name, "w")  # , encoding="utf-8")
with open(source_path + data_set, "r", encoding="utf-8") as in_file:
    line = in_file.readline()
    while line:
        if not line.strip():
            line = in_file.readline()
        else:
            temp_sen = []
            while line.strip():
                temp_sen.append(line)
                line = in_file.readline()
            obj = {"id": temp_sen[0][:-6]}  # obj{"id": id, "dial": dial}
            dial = []  # dial[{"time": time, "speaker": speaker, "content": content}, ...]
            for sen in temp_sen[1:]:
                tmp = sen.split()
                dial.append({"time": tmp[0:2], "speaker": tmp[2][:-1], "content": " ".join(tmp[3:])})
            obj["dial"] = dial
            dial_all.append(obj)
            try:
                out_file.write(json.dumps(obj, ensure_ascii=False) + "\n")
            except UnicodeEncodeError:
                for dia in obj["dial"]:
                    dia["content"] = re_clean.sub(u'', dia["content"])
                out_file.write(json.dumps(obj, ensure_ascii=False) + "\n")
out_file.close()

# split data set regarding to completeness of dialogue
# dial_no_rst_all = []
# dial_rst_all = []
# dial_no_dgn_all = []
# dial_dgn_all = []
# with open(source_path + out_file_name, "r") as in_file:
#     for line in in_file.readlines():
#         obj = json.loads(line.strip())
#         if obj["dial"][-1]["speaker"] == "client":
#             dial_no_rst_all.append(line.strip())
#             continue
#         dial_rst_all.append(line.strip())
# print("Number of Uncompleted Dialogues:", len(dial_no_rst_all))
# print("Number of Dialogues with Results:", len(dial_rst_all))
# for line in dial_rst_all:
#     obj = json.loads(line.strip())
#     rst = json.loads(obj["dial"][-1]["content"])
#     if not rst["rst"]:  # no diagnoses given
#         dial_no_dgn_all.append(line.strip())
#         continue
#     dial_dgn_all.append(line.strip())
# print("Number of Dialogues with Results and without Diagnose:", len(dial_no_dgn_all))
# print("Number of Dialogues with Diagnoses:", len(dial_dgn_all))

# save them
# dial_no_rst_file = open(source_path + out_file_name[0:4] + "_no_rst.txt", "w")
# dial_rst_file = open(source_path + out_file_name[0:4] + "_rst.txt", "w")
# dial_no_dgn_file = open(source_path + out_file_name[0:4] + "_no_dgn.txt", "w")
# dial_dgn_file = open(source_path + out_file_name[0:4] + "_dgn.txt", "w")
# for line in dial_no_rst_all:
#     dial_no_rst_file.write(line + "\n")
# for line in dial_rst_all:
#     dial_rst_file.write(line + "\n")
# for line in dial_no_dgn_all:
#     dial_no_dgn_file.write(line + "\n")
# for line in dial_dgn_all:
#     dial_dgn_file.write(line + "\n")
# dial_no_rst_file.close()
# dial_rst_file.close()
# dial_no_dgn_file.close()
# dial_dgn_file.close()


# reload json format data into human-friendly data format
# reload_file = open(source_path + "dial_conventional.txt", "w")
# with open(source_path + "dial.txt", "r") as in_file:
#     for line in in_file.readlines():
#         obj = json.loads(line.strip())
#         reload_file.write(obj["id"] + "\n")
#         for dial in obj["dial"]:
#             reload_file.write(dial["time"][0] + " " + dial["time"][1] + " ")
#             reload_file.write(dial["speaker"] + " ")
#             reload_file.write(dial["content"] + "\n")
#         reload_file.write("\n\n")
# reload_file.close()


# choose 200 dialogues randomly
# with open(source_path + "dial_dgn.txt", "r") as in_file:
#     lines = in_file.readlines()
#     choices = random.sample(lines, 200)
# with open(source_path + "dial_dgn_200.txt", "w") as out_file:
#     for cho in choices:
#         out_file.write(cho)

