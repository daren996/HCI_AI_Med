
"""
Try some naive analyses.

Structure of data_set:
obj{"id": id, "dial": dial}
dial[{"time": time, "speaker": speaker, "content": content}, ...]
"""

import json

source_path = "../DataSet/"
data_set = "dial.txt"


# Find Duplicate ID(s)
# id_all = set()
# with open(source_path + data_set, "r") as in_file:
#     for line in in_file.readlines():
#         obj = json.loads(line)
#         if obj["id"] not in id_all:
#             id_all.add(obj["id"])
#         else:
#             print(obj["id"])


# Find All Results
rst_id_all = []
rst_all = []
with open(source_path + data_set, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        if obj["dial"][-1]["speaker"] == "client":
            continue
        try:
            content = json.loads(obj["dial"][-1]["content"])
            rst_all.append(content)
            rst_id_all.append(obj["id"])
        except:
            pass
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

