
import json
import re

source_path = "../DataSet/"
data_set = "znzd.txt"
out_file = "dial.txt"

re_clean = re.compile(u'[\U00010000-\U0010ffff]')

dial_all = []
out_file = open(source_path + out_file, "w")  # , encoding="utf-8")
with open (source_path + data_set, "r", encoding="utf-8") as in_file:
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
