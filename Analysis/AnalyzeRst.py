
import json
import numpy as np
import matplotlib.pyplot as plt

source_path = "../DataSet/"
data_set = "dial.txt"
rst_file_name = "rst.txt"

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9


# gender
gender = {"male": 0, "female": 0}
with open(source_path + rst_file_name, "r") as in_file:
    for line in in_file.readlines():
        rst = json.loads(line)
        if not rst["attachment_dict"]:
            continue
        if rst["attachment_dict"]["gender"] == "男":
            gender["male"] += 1
        elif rst["attachment_dict"]["gender"] == "女":
            gender["female"] += 1
        else:
            print(rst["attachment_dict"]["gender"], rst["attachment_dict"]["session_id"])
print(gender)


# age
age_group = {}
with open(source_path + rst_file_name, "r") as in_file:
    for line in in_file.readlines():
        rst = json.loads(line)
        if not rst["attachment_dict"]:
            continue
        if rst["attachment_dict"]["age_group"] not in age_group:
            age_group[rst["attachment_dict"]["age_group"]] = 0
        age_group[rst["attachment_dict"]["age_group"]] += 1
print(age_group)


# diagnose
count_diagnose = 0
diagnose_all = {}
with open(source_path + rst_file_name, "r") as in_file:
    for line in in_file.readlines():
        rst = json.loads(line)
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
rank_dgn = sorted(diagnose_all.items(), key=lambda x: x[1], reverse=True)
# for r in rank_dgn:
#     print(r)
rank_show_dgn = 30
rank_dgn = rank_dgn[0:rank_show_dgn] + [('else', sum([dgn[1] for dgn in rank_dgn[rank_show_dgn:]]))]
# for r in rank_dgn:
#     print(r)


# symptom
symptoms = {}
with open(source_path + rst_file_name, "r") as in_file:
    for line in in_file.readlines():
        rst = json.loads(line)
        if not rst["attachment_dict"]:
            continue
        if rst["attachment_dict"]["raw_sentence"] not in symptoms:
            symptoms[rst["attachment_dict"]["raw_sentence"]] = 0
        symptoms[rst["attachment_dict"]["raw_sentence"]] += 1
print("Number of symptoms is:", len(symptoms))
rank_sym = sorted(symptoms.items(), key=lambda x: x[1], reverse=True)
# for sym in rank_sym:
#     print(sym)
rank_show_sym = 10
rank_sym = rank_sym[0:rank_show_sym] + [('else', sum([sym[1] for sym in rank_sym[rank_show_sym:]]))]
# for sym in rank_sym:
#     print(sym)
 

# plot
# fig1 = plt.figure(1, figsize=(12, 5))
# # ax1 = fig1.add_subplot(121)
# # ax1.set_title('gender')
# # labels1 = ['{}:{}'.format(gen, per) for gen, per in zip(gender.keys(), gender.values())]
# # ax1.pie(list(gender.values()), labels=labels1, shadow=True)
# # ax2 = fig1.add_subplot(122)
# # ax2.set_title('age')
# # labels2 = ['{}:{}'.format(age, per) for age, per in zip(age_group.keys(), age_group.values())]
# # ax2.pie(list(age_group.values()), labels=labels2, shadow=True)
# # fig1.savefig('clients_info.png')
# #
# # fig2 = plt.figure(2, figsize=(10, 8))
# # ax3 = fig2.add_subplot(111)
# # ax3.set_title('diagnose')
# # labels3 = ['{}:{}'.format(age, per) for age, per in zip([dgn[0] for dgn in rank_dgn], [dgn[1] for dgn in rank_dgn])]
# # ax3.pie([dgn[1] for dgn in rank_dgn], labels=labels3, explode=[0] * rank_show_dgn + [0.1], shadow=True)
# # fig2.savefig('diagnoses_info.png')
# #
# # fig3 = plt.figure(3, figsize=(10, 8))
# # ax4 = fig3.add_subplot(111)
# # ax4.set_title('symptom')
# # labels4 = ['{}:{}'.format(sym, num) for sym, num in zip([sym[0] for sym in rank_sym], [sym[1] for sym in rank_sym])]
# # ax4.pie([sym[1] for sym in rank_sym], labels=labels4, explode=[0] * rank_show_sym + [0.1], shadow=True)
# # fig3.savefig('symptoms_info.png')
# #
# # plt.show()



