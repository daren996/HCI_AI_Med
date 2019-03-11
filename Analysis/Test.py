
"""
Try some naive analyses.

Structure of data_set:
obj{"id": id, "dial": dial}
dial[{"time": time, "speaker": speaker, "content": content}, ...]
"""

import json
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

source_path = "../DataSet/"
data_set = "dial.txt"

font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

# Find Duplicate ID(s)
id_all = set()
with open(source_path + data_set, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        if obj["id"] not in id_all:
            id_all.add(obj["id"])
        else:
            print(obj["id"])


# Find All Results
no_rst_count = 0
rst_id_all = []
rst_all = []
# rst_file_name = "rst.txt"
# rst_output = open(source_path + rst_file_name, "w")
with open(source_path + data_set, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        if obj["dial"][-1]["speaker"] == "client":
            no_rst_count += 1
            continue
        try:
            content = json.loads(obj["dial"][-1]["content"])
            rst_all.append(content)
            rst_id_all.append(obj["id"])
            # rst_output.write(obj["dial"][-1]["content"] + "\n")
        except:
            pass
# rst_output.close()
print("Number of No Results:", no_rst_count)
print("Number of Results:", len(rst_all))

# Find All Diagnoses
count_diagnose = 0
diagnose_all = {}
for rst in rst_all:
    if not rst["rst"]:  # no diagnoses given
        # print("No diagnoses given, session_id:", rst["attachment_dict"]["session_id"])
        continue
    count_diagnose += 1
    diagnose = rst["rst"][0]["name"]
    if diagnose not in diagnose_all:
        diagnose_all[diagnose] = 0
    diagnose_all[diagnose] += 1
print("Number of Diagnoses:", count_diagnose)
print("Number of Type of Diagnoses:", len(diagnose_all))
# rank_diag = sorted(diagnose_all.items(), key=lambda x: x[1], reverse=True)
# for r in rank_diag:
#     print(r)

# pie graph of proportions of different dialogues
dial_proportion = [no_rst_count, len(rst_all)-count_diagnose, count_diagnose]
dial_labels = ["No results %d" % no_rst_count,
               "With results but no diagnose %d" % (len(rst_all)-count_diagnose),
               "With diagnose %d" % count_diagnose]
fig = plt.figure(1)
ax = fig.add_subplot(111)
patches, l_text = ax.pie(dial_proportion, labels=dial_labels, explode=[0, 0.05, 0])
for t in l_text:
    t.set_fontproperties(font)
ax.set_title(u'Proportion of different kinds of dialogues', fontproperties=font)
# fig.savefig("time_cost.png")
plt.show()
