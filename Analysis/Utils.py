import json


# format of timeStr: xx:xx:xx
def getTime(timeStr):
    temp = timeStr.split(":")
    timeSec = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2])
    return timeSec


# find all services in dialogues; input: lines of dialogues
def findServices(lines):
    service_needed = {}
    for line in lines:
        obj = json.loads(line)
        if "需要哪方面的服务" not in obj["dial"][0]["content"]:
            # print(obj["id"])
            continue
        if obj["dial"][1]["content"] not in service_needed:
            service_needed[obj["dial"][1]["content"]] = 0
        service_needed[obj["dial"][1]["content"]] += 1
    return service_needed


# whether asked about pregnant information as to women in dialogues
def noPregnantAsked(lines):
    count_no_asked = 0
    for line in lines:
        asked = True
        obj = json.loads(line)
        for dia in obj["dial"]:
            if "女" in dia["content"]:
                asked = False
        for dia in obj["dial"]:
            if "孕妇" in dia["content"]:
                asked = True
        if not asked:
            count_no_asked += 1
            # print(obj["id"])
    return count_no_asked


# get format: Q&A&Time [[(question, answer, time), (...), ...], [...], ...]
def get_que_ans_time_arr(source_path, data_set, ):
    que_ans_time_arr = []
    with open(source_path + data_set, "r") as in_file:
        for line in in_file.readlines():
            obj = json.loads(line)
            c_time = []
            r_time = []
            if obj["dial"][0]["speaker"] != "Robot":
                print("ERROR: client start", obj["id"])
                continue
            for x in range(1, len(obj["dial"])):  # check no continuous speaker
                if obj["dial"][x]["speaker"] == obj["dial"][x - 1]["speaker"]:
                    print("ERROR: continuous speaker:", obj["id"])
            for dial in json.loads(line)["dial"]:
                if dial["speaker"] == "Robot":
                    r_time.append((dial["content"], getTime(dial["time"][1])))
                if dial["speaker"] == "client":
                    c_time.append((dial["content"], getTime(dial["time"][1])))
            que_ans_time = []
            for x in range(0, len(c_time) - 1):
                time_dif = r_time[x + 1][1] - c_time[x][1] + 1
                if time_dif < 0:
                    time_dif += 86400
                que_ans_time.append((r_time[x][0], c_time[x][0], time_dif))
            que_ans_time_arr.append(que_ans_time)
            # print(que_ans_time)
    return que_ans_time_arr


# classify questions
# que_cate_arr = {category: [(question, time), (...), ...]}
def get_que_cate_arr(que_ans_time_arr):
    que_cate_arr = {}
    for cat in ques_type:
        que_cate_arr[cat] = []
    for que in que_ans_time_arr:
        for qu in que:
            classified = False
            for cat in ques_type:
                for ca in ques_type[cat]:
                    if ca in qu[0]:
                        que_cate_arr[cat].append((qu[0], qu[2]))
                        classified = True
            if not classified:
                # print(qu[0])
                que_cate_arr["else"].append((qu[0], qu[2]))
    que_cate_arr_count = sum([len(que_cate_arr[cat]) for cat in que_cate_arr])
    return que_cate_arr, que_cate_arr_count


# classify questions
# que_cate_arr = {category: [(question, time), (...), ...]}
def get_que_cate_arr1(que_ans_time_arr):
    que_cate_arr = {}
    for cat in ques_type1:
        que_cate_arr[cat] = []
    for que in que_ans_time_arr:
        for qu in que:
            classified = False
            for cat in ques_type1:
                for ca in ques_type1[cat]:
                    if ca in qu[0]:
                        que_cate_arr[cat].append((qu[0], qu[2]))
                        classified = True
            if not classified:
                # print(qu[0])
                que_cate_arr["症状信息"].append((qu[0], qu[2]))
    que_cate_arr_count = sum([len(que_cate_arr[cat]) for cat in que_cate_arr])
    return que_cate_arr, que_cate_arr_count


# classify questions
# que_cate_arr = {category: [(question, time), (...), ...]}
def get_que_cate_arr2(que_ans_time_arr):
    que_cate_arr = {}
    for cat in ques_type2:
        que_cate_arr[cat] = []
    for que in que_ans_time_arr:
        for qu in que:
            classified = False
            for cat in ques_type2:
                for ca in ques_type2[cat]:
                    if ca in qu[0]:
                        que_cate_arr[cat].append((qu[0], qu[2]))
                        classified = True
            if not classified:
                # print(qu[0])
                que_cate_arr["else"].append((qu[0], qu[2]))
    que_cate_arr_count = sum([len(que_cate_arr[cat]) for cat in que_cate_arr])
    return que_cate_arr, que_cate_arr_count


ques_type = {"服务": ["请问您需要哪方面的服务"],
             "年龄": ["年龄"],
             "性别": ["性别"],
             "孕妇": ["孕妇", "妊娠"],
             "病史": ["病史"],
             "体征": ["血压", "心率", "体温"],
             "病前": ["发病前是否存在以下行为", "发病前是否有过以下情况？"],
             "多久": ["多久了", "多长时间了"],
             "符合": ["您的描述符合以下哪种症状"],
             "症状": ["请选择您的症状"],
             "重新": ["对不起，没有找到相关症状，请重新输入。"],
             "描述": ["符合以下哪种描述"],
             "伴有": ["是否伴有"],
             "性质": ["性质", "部位", "颜色", "气味", "形状", "范围"],
             "程度": ["程度", "加重"],
             "频率": ["持续性", "阵发性", "频率"],
             "其它": ["如果还有其它症状，请继续输入。如果没有，请点击没有了。"],
             "else": ["No Category but Description about Symptom at Most Time."]}

ques_type1 = {"选择服务": ["请问您需要哪方面的服务"],
              "症状描述": ["请选择您的症状", "对不起，没有找到相关症状，请重新输入"],
              "个人背景": ["年龄", "性别", "孕妇", "妊娠"],
              "个人体征": ["血压", "心率", "体温"],
              "病前行为": ["发病前是否存在以下行为", "发病前是否有过以下情况"],
              "症状信息": ["多久了", "多长时间了", "您的描述符合以下哪种症状", "符合以下哪种描述", "是否伴有", "性质",
                       "部位", "颜色", "气味", "形状", "范围", "程度", "加重", "持续性", "阵发性", "频率",
                       "如果还有其它症状，请继续输入。如果没有，请点击没有了"],
              "病史": ["病史"]}

ques_type2 = {"简答题": ["请问您需要哪方面的服务", "请选择您的症状", "对不起，没有找到相关症状，请重新输入。"],
              "数字题": ["年龄", "血压", "心率", "体温", "多久了", "多长时间了"],
              "单选题": ["性别", "孕妇", "妊娠", "性质", "颜色", "气味", "形状", "程度", "加重", "持续性", "频率", "阵发性",
                      "符合以下哪种描述", "您的描述符合以下哪种症状"],
              "多选题": ["发病前是否存在以下行为", "发病前是否有过以下情况？", "部位", "范围", "是否伴有"],
              "选择加简答": ["病史", "如果还有其它症状，请继续输入。如果没有，请点击没有了。"],
              "else": ["No Category but Description about Symptom at Most Time."]}


def age_num2group(age_num):
    if age_num <= 6:
        return '0~6岁'
    elif age_num <= 15:
        return '7~15岁'
    elif age_num <= 35:
        return '16~35岁'
    elif age_num <= 60:
        return '36~60岁'
    else:
        return '大于60岁'


age_group = ['0~6岁', '7~15岁', '16~35岁', '36~60岁', '大于60岁', 'unknown']
age_decode = {'0~6岁': '0-6 years old', '7~15岁': '7-15 years old', '16~35岁': '16-35 years old',
              '36~60岁': '35-60 years old', '大于60岁': '>60 years old', 'unknown': 'unknown'}


# get time group of a day. format of timeStr: xx:xx:xx
def get_time_group(time_str):
    temp = time_str.split(":")
    tim = int(temp[0])
    if tim < 6:
        return 'night(23-6*)'
    if tim < 12:
        return 'morning(6-12)'
    if tim < 19:
        return 'afternoon(12-19)'
    if tim < 23:
        return 'evening(19-23)'
    else:
        return 'night(23-6*)'


time_group = ['morning(6-12)', 'afternoon(12-19)', 'evening(19-23)', 'night(23-6*)', 'unknown']


# get span group. format of timeStr: xx:xx:xx
def get_span_group(span):
    if span < 2:
        return '0-2'
    if span < 10:
        return '2-10'
    if span < 50:
        return '10-50'
    if span < 100:
        return '50-100'
    if span < 150:
        return '100-150'
    else:
        return '150*'


span_group = ['0-2', '2-10', '10-50', '50-100', '100-150', '150*', 'unknown']
valid_group = ['valid', 'invalid']
gender_group = ['男', '女', 'unknown']
gender_decode = {'男': 'male', '女': 'female', 'unknown': 'unknown'}


def get_cross(cross_type, obj):
    cross = "unknown"
    if cross_type == "age":
        if obj["dial"][-1]["speaker"] == "Robot":
            rst = json.loads(obj["dial"][-1]["content"])
            cross = rst["attachment_dict"]["age_group"]
        else:
            for _, dial in enumerate(obj["dial"]):
                if "年龄" in dial["content"]:
                    age_num = obj["dial"][_ + 1]["content"][0:-1]
                    cross = age_num2group(int(age_num))
    elif cross_type == "gender":
        if obj["dial"][-1]["speaker"] == "Robot":
            rst = json.loads(obj["dial"][-1]["content"])
            if not rst["attachment_dict"]:
                print("ERROR no attachment_dict:", obj["id"])
                return cross
            cross = rst["attachment_dict"]["gender"]
        else:
            for _, dial in enumerate(obj["dial"]):
                if "性别" in dial["content"]:
                    cross = obj["dial"][_ + 1]["content"]
                    if cross not in ["男", "女"]:
                        print("ERROR irregular gender:", cross, obj["id"])
    elif cross_type == "span":
        span = getTime(obj["dial"][-1]["time"][1]) - getTime(obj["dial"][0]["time"][1])
        cross = get_span_group(span)
    elif cross_type == "time":
        cross = get_time_group(obj["dial"][0]["time"][1])
    return cross


dis_cate = ["头", "耳鼻喉", "胸", "口咳牙痰", "腹肚胃", "女经乳", "性", "尿", "便肛肠", "痒", "疼痛"]

