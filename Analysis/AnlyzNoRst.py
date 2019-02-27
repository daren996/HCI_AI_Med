
import Utils
import json
import matplotlib.pylab as plt
import numpy as np
import math

source_path = "../DataSet/"
data_set = "dial_no_rst.txt"

with open(source_path + data_set, "r") as in_file:
    lines = in_file.readlines()
    service_needed = Utils.findServices(lines)
    count_no_asked = Utils.noPregnantAsked(lines)
# print("Number of services needed is:", len(service_needed), list(service_needed.keys()))
# print("Number of women who aren't asked about pregnancy:", count_no_asked)

for line in lines:
    obj = json.loads(line.strip())
    print(obj["dial"][-2]["speaker"], obj["dial"][-2]["content"],
          obj["dial"][-1]["speaker"], obj["dial"][-1]["content"], "\t", obj["id"])

