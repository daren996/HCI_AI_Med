
import json


source_path = "../DataSet/"
data_set = "PMH.txt"


with open(source_path + data_set, "r") as in_file:
    for line in in_file.readlines():
        temp = line.strip().split(" ")
        ind = temp[0]
        ans = temp[1]
        age = temp[2]
        dgn = temp[3:8]
        dis = temp[8]
        try:
            rev = temp[9]
            svr = temp[10]
        except IndexError:
            print("Error", ind, ans, age, dgn, dis)
        print(ind, ans, age, dgn, dis, rev, svr)

