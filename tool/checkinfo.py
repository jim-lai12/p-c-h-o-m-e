# -*- coding: utf-8 -*-
import logging
import sys

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='myLog.log', filemode='a+', format=FORMAT)


class Checkbeforebuy:
    def __init__(self,config,s):
        self.config = config
        self.session = s
        self.header = {'X-Requested': 'With:XMLHttpRequest', 'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br', 'Host': 'ecvip.pchome.com.tw', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0', 'Connection': 'keep-alive', 'Referer': 'https://ecvip.pchome.com.tw/', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
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
        if self.config.add & self.config.addnum =="":
            logging.info("add check ok")
    def checkfree(self):
        if self.config.free == "":
            logging.info("free check ok")
    def checkspecification(self):#要優先寫
        print "ok"
    def checkall(self):
        self.checklogin()

        self.config.product = self.config.id+"-"+self.config.specification


