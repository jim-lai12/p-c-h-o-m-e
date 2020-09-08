# -*- coding: utf-8 -*-
header = """
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
accept-encoding: gzip, deflate, br
accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6
dnt: 1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36



"""

reduce =  header.split("\n")

output = {}

for item in reduce :
    if item != "":
        output[item.split(": ")[0]] = item.split(": ")[1]
if "user-agent" in output:
    del output["user-agent"]
if "cookie" in output:
    del output["cookie"]
print output





