"""
Past medical history (PMH) is an important information

"""


import json


source_path = "../DataSet/"
data_set = "dial_dgn.txt"

# past medical history
ask_med_hst = []
age_gender = {}
all_age = {}
with open(source_path + data_set, "r") as in_file:
    for _, line in enumerate(in_file.readlines()):
        asked = False
        obj = json.loads(line)
        rst = json.loads(obj["dial"][-1]["content"])
        for __, que in enumerate(obj["dial"]):
            if not asked and "史" in que["content"] and que["speaker"] == "Robot" and __ < len(obj["dial"])-1:
                if rst["attachment_dict"]["age_group"] not in all_age:
                    all_age[rst["attachment_dict"]["age_group"]] = 0
                all_age[rst["attachment_dict"]["age_group"]] += 1
            if not asked and "史" in que["content"] and que["speaker"] == "Robot" \
                    and __ < len(obj["dial"])-1 and "没有" not in obj["dial"][__+1]["content"] \
                    and "不清楚" not in obj["dial"][__+1]["content"] and "啦啦啦" not in obj["dial"][__+1]["content"]:
                print(_, obj["dial"][__+1]["content"], rst["attachment_dict"]["age_group"],
                      rst["attachment_dict"]["gender"],
                      [x["name"] for x in rst["rst"]], obj["dial"][3]["content"], "")
                if rst["attachment_dict"]["age_group"] not in age_gender:
                    age_gender[rst["attachment_dict"]["age_group"]] = []
                age_gender[rst["attachment_dict"]["age_group"]].append(rst["attachment_dict"]["gender"])
                ask_med_hst.append(que["content"])
                asked = True
count = len(ask_med_hst)
print(count)

# whether a substitute of return visit
for age in age_gender:
    male = 0
    female = 0
    for gen in age_gender[age]:
        if gen == "男":
            male += 1
        elif gen == "女":
            female += 1
        else:
            print("ERROR:", gen)
    # print(age, male, male / count, female, female / count, male + female, (male + female) / count)
all_count = sum([x[1] for x in all_age.items()])
num_no = {}
num_yes = {}
with open("../Log/past_med_hst", "r") as in_file:
    lines = in_file.readlines()
    for line in lines[4:]:
        temp = line.strip().split(" ")
        age = temp[2]
        if temp[-2] == "否":
            if age not in num_no:
                num_no[age] = 0
            num_no[age] += 1
        elif temp[-2] == "是":
            if age not in num_yes:
                num_yes[age] = 0
            num_yes[age] += 1
        else:
            print("ERROR!", temp)
for age in all_age:
    no = 0
    yes = 0
    if age in num_no:
        no = num_no[age]
    if age in num_yes:
        yes = num_yes[age]
    print(age, all_age[age]-no-yes, "%.4f" % ((all_age[age]-no-yes)/all_count),
          no, "%.4f" % (no/all_count), yes, "%.4f" % (yes/all_count),
          all_age[age], "%.4f" % (all_age[age]/all_count))

# whether severe
for age in age_gender:
    male = 0
    female = 0
    for gen in age_gender[age]:
        if gen == "男":
            male += 1
        elif gen == "女":
            female += 1
        else:
            print("ERROR:", gen)
    # print(age, male, male / count, female, female / count, male + female, (male + female) / count)
all_count = sum([x[1] for x in all_age.items()])
num_mild = {}
num_severe = {}
with open("../Log/past_med_hst", "r") as in_file:
    lines = in_file.readlines()
    for line in lines[4:]:
        temp = line.strip().split(" ")
        age = temp[2]
        if temp[-1] == "否":
            if age not in num_mild:
                num_mild[age] = 0
            num_mild[age] += 1
        elif temp[-1] == "是":
            if age not in num_severe:
                num_severe[age] = 0
            num_severe[age] += 1
for age in all_age:
    mild = 0
    severe = 0
    if age in num_mild:
        mild = num_mild[age]
    if age in num_severe:
        severe = num_severe[age]
    print(age, all_age[age]-mild-severe, "%.4f" % ((all_age[age]-mild-severe)/all_count),
          mild, "%.4f" % (mild/all_count), severe, "%.4f" % (severe/all_count),
          all_age[age], "%.4f" % (all_age[age]/all_count))
