
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

