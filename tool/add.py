# -*- coding: utf-8 -*-
import logging
import time
from tool import dict2str
from tool import parseJson

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename='myLog.log', filemode='a+', format=FORMAT)



class Add2car:
    def __init__(self,config,s):
        self.config = config
        self.session = s
        self.header = {
            "Host": "24h.pchome.com.tw",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "TE": "Trailers",
            "Upgrade-Insecure-Requests": "1"
        }
        self.header["Referer"] = "https://24h.pchome.com.tw/prod/" + self.config.id
        self.header["User-Agent"] = self.config.userAgent
        self.header2 = {
            "Host": "24h.pchome.com.tw",
            'Origin': 'https://24h.pchome.com.tw',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.header2["Referer"] = "https://24h.pchome.com.tw/prod/" + self.config.id
        self.header2["User-Agent"] = self.config.userAgent
    def setTimer(self):
        a = time.strftime("%H"":""%M"":""%S")
        if self.config.time == "xx:xx:xx":
            logging.info("start")
        else:
            while a != self.config.time:
                a = time.strftime("%H"":""%M"":""%S")
                time.sleep(0.01)

    def snapup(self,timeout1 = 1.5,timeout2 = 1):
        pro = 0
        while pro == 0:
            mac = ""
            while mac == "":
                t1 = time.time()
                try:
                    r = self.session.get("https://24h.pchome.com.tw/prod/cart/v1/prod/" + self.config.product + "/snapup?_=" + str(int(time.time() * 1000)),headers=self.header, timeout=timeout1)
                    logging.info( "status code : "+ str(r.status_code))
                    logging.info( r.text )
                    mac = r.json()["MAC"]
                    data = {
                        "G": [],
                        "A": [],
                        "B": [],
                        "TB": "24H",
                        "TP": 2,
                        "T": "ADD",
                        "TI": self.config.product,
                        "RS": "",
                        "YTQ": self.config.num,
                        "CAX": r.json()["MAC"].encode('utf-8'),
                        "CAXE": r.json()["MACExpire"].encode('utf-8')
                    }
                    if len(self.config.free) !=0:
                        for i in self.config.free:
                            data["G"].append({"TI": i})
                    if len(self.config.add) !=0:
                        for i in range(len(self.config.add)):
                            data["A"].append({"TI": self.config.add[i],"YTQ":int(self.config.addnum[i])})
                    data = "data=" + dict2str(data)

                except Exception as e:
                    logging.info( "add2car step 1 error" )
                    logging.info( e )
                    t2 = time.time()
                    if t2 - t1 < 1:
                        time.sleep(1 - (t2 - t1))
                logging.info( "add2car step 1 ok")
            t3 = time.time()
            try:
                r2 = self.session.post("https://24h.pchome.com.tw/fscart/index.php/prod/modify?callback=jsonp_addcart&" + str(int(time.time() * 1000)), headers=self.header2, data=data, timeout=timeout2)
                logging.info("status code : "+ str(r2.status_code))
                logging.info( r2.text )
                dat = parseJson(r2.text)
                pro = dat["PRODTOTAL"]
            except Exception as e:
                logging.info("add2car step 2 error")
                logging.info(e)
            t4 = time.time()
            if t4 - t3 < 1:
                time.sleep(1 - (t4 - t3))
            logging.info( "add2car step 2 ok")



