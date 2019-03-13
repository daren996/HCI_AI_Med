
import json
import jieba

source_path = "../DataSet/"
data_set = "dial.txt"
rst_file_name = "rst.txt"


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


category_smp = {"头": [], "耳鼻喉": [], "胸": [], "口咳牙痰": [], "腹肚胃": [], "女经乳": [], "性": [],
                "尿": [], "便肛肠": [], "痒": [], "疼痛": []}
category_cnt = {"头": 0, "耳鼻喉": 0, "胸": 0, "口咳牙痰": 0, "腹肚胃": 0, "女经乳": 0, "性": 0,
                "尿": 0, "便肛肠": 0, "痒": 0, "疼痛": 0}
has_cat = 0
no_cat = []
for smp in symptoms:
    is_cla = False
    for cat in category_smp:
        for c in cat:
            if c in smp:
                category_smp[cat].append((smp, symptoms[smp]))
                category_cnt[cat] += symptoms[smp]
                is_cla = True
    if "白带" in smp:
        category_smp["女经乳"].append((smp, symptoms[smp]))
        category_cnt["女经乳"] += symptoms[smp]
        is_cla = True
    if "前列腺" in smp:
        category_smp["尿"].append((smp, symptoms[smp]))
        category_cnt["尿"] += symptoms[smp]
        is_cla = True
    if "生殖器" in smp or "早泄" in smp or "淫" in smp or "勃起" in smp \
            or "阴茎" in smp or "早泄" in smp or "睾" in smp:
        category_smp["性"].append((smp, symptoms[smp]))
        category_cnt["性"] += symptoms[smp]
        is_cla = True
    if is_cla is False:
        no_cat.append((smp, symptoms[smp]))
    else:
        has_cat += 1
print(category_smp)
# print(has_cat)
# for cat in category_cnt:
#     print(cat, category_cnt[cat])
# for cat in category_smp:
#     print(cat + ":", category_cnt[cat])
#     for smp in category_smp[cat]:
#         print(smp)
#     print("\n")

new_category_smp = {"": []}
for nca in no_cat:
    # print(nca)
    # is_cla = False
    pass


for smp in symptoms:
    seg_smp = jieba.cut(smp, cut_all=False)
    print("/".join(seg_smp))
    print(seg_smp)

