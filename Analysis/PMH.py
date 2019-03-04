"""
Past medical history (PMH) is an important information

"""


import json


source_path = "../DataSet/"
data_set = "dial_dgn.txt"

# past medical history
ask_med_hst = []
with open(source_path + data_set, "r") as in_file:
    for _, line in enumerate(in_file.readlines()):
        asked = False
        obj = json.loads(line)
        for __, que in enumerate(obj["dial"]):
            if not asked and "史" in que["content"] and que["speaker"] == "Robot" \
                    and __ < len(obj["dial"])-1 and "没有" not in obj["dial"][__+1]["content"] \
                    and "不清楚" not in obj["dial"][__+1]["content"] and "啦啦啦" not in obj["dial"][__+1]["content"]:
                print(_, que["content"], obj["dial"][__+1]["content"],
                      json.loads(obj["dial"][-1]["content"])["attachment_dict"]["age_group"])
                ask_med_hst.append(que["content"])
                asked = True
print(len(ask_med_hst))

