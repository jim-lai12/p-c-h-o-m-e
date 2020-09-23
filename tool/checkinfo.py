# -*- coding: utf-8 -*-
import logging
import sys
from tool import parseJson
import random

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='myLog.log', filemode='a+', format=FORMAT)


class Checkbeforebuy:
    def __init__(self,config,s):
        self.config = config
        self.session = s

        self.header = {'X-Requested': 'With:XMLHttpRequest', 'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br', 'Host': 'ecvip.pchome.com.tw', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Connection': 'keep-alive', 'Referer': 'https://ecvip.pchome.com.tw/', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
        self.header2 = {'Host': 'ecapi.pchome.com.tw', 'Connection': 'keep-alive', 'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': '*/*'}
        self.header["User-Agent"] = self.config.userAgent
        self.header2["User-Agent"] = self.config.userAgent
        self.header2["Referer"] = "https://24h.pchome.com.tw/prod/"+self.config.id
    def checklogin(self):
        result = self.session.get("https://ecvip.pchome.com.tw/fsapi/member/v1/logininfo",headers = self.header)
        try:
            if result.json()["isLogin"] == 0:
                logging.error("Not login")
                sys.exit()
        except:
            logging.error("Checklogin error")
            sys.exit()
        logging.info("login check ok")
    def checkadd(self):#要優先寫
        if self.config.add == "":
            self.config.add = []
        else:
            self.config.add = self.config.add.split(",")
        if self.config.addnum == "":
            self.config.addnum = []
        else:
            self.config.addnum = self.config.addnum.split(",")
        addlist = []
        if len(self.config.add) == len(self.config.addnum):
            if len(self.config.add) != 0:
                url = "https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/prod/" + self.config.id + "/add&fields=Seq,Id,Name,Spec,Group,Price,Pic,Qty,isWarranty&_callback=jsonp_add?_callback=jsonp_add"
                resp = self.session.get(url, headers=self.header2).text
                data = parseJson(resp)
                l = data.keys()
                try:
                    for i in self.config.add:
                        print (data[l[int(i)-1]][0]["Name"])
                        addlist.append(data[l[int(i)-1]][0]["Id"].encode("utf-8"))
                except Exception as e:
                    logging.error("add key Error")
                    logging.error(e)
                    sys.exit()
        else:
            logging.error("add and addnum Error")
        self.config.add = addlist
        logging.info("add check ok")
    def checkfree(self):
        if self.config.free == "":
            self.config.free = []
        else:
            self.config.free = self.config.free.split(",")
        url = "https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/prod/"+self.config.id+"/gift&_callback=jsonp_gift"
        resp = self.session.get(url,headers = self.header2).text
        data = parseJson(resp)
        freelist = []
        freedata = {}
        if len(data) == 1:
            data = data[self.config.id]
            if data[0]["isGiveAll"] == 1:
                for item in data[0]["Item"]:
                    print (item["Name"])
                    freelist.append(item["Id"].encode("utf-8"))
                i = 1
            else:
                i = 0
            n = 1
            while i < len(data):
                for item in data[i]["Item"]:
                    l = []
                    l.append(item["Name"])
                    l.append(item["Id"])
                    freedata[str(n)] = l
                    n += 1
                i += 1
        try:
            if len(self.config.free) != 0:
                for number in self.config.free:
                    print (freedata[number][0])
                    freelist.append(freedata[number][1].encode("utf-8"))
        except Exception as e:
            logging.error("free Error")
            logging.error(e)
            sys.exit()
        self.config.free = freelist
        logging.info("free check ok")
    def checkspecification(self):
        url = "https://ecapi.pchome.com.tw/ecshop/prodapi/v2/prod/button&id="+self.config.id+"&fields=Seq,Id,Price,Qty,ButtonType,SaleStatus,isPrimeOnly,SpecialQty&_callback=jsonp_button"
        resp = self.session.get(url,headers=self.header2).text
        data = parseJson(resp)
        if len(data) == 1:
            self.config.product = self.config.id + "-" + "000"
        else:
            if int(self.config.specification) == 0:
                self.config.product = data[1]["Id"]
            else:
                if int(self.config.specification) < len(data)-1:
                    if data[int(self.config.specification)]["Qty"] != 0:
                        self.config.product = data[int(self.config.specification)]["Id"]
                    else:
                        logging.error("this specification is sell out")
                        n = 0
                        while n == 0:
                            randnum = random.randint(1,len(data)-1)
                            self.config.product = data[randnum]["Id"]
                            n = data[randnum]["Qty"]
                else:
                    logging.error("this specification not found")
                    n = 0
                    while n == 0:
                        randnum = random.randint(1, len(data) - 1)
                        self.config.product = data[randnum]["Id"]
                        n = data[randnum]["Qty"]
        self.config.product = self.config.id + "-" + self.config.specification
        logging.info("product check ok")
    def checkall(self):
        self.checklogin()
        self.checkspecification()
        self.checkadd()
        self.checkfree()



