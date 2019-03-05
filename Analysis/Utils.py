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
