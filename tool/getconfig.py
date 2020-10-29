# -*- coding: utf-8 -*-
import logging
import re
import sys
import cookielib
import requests
from tool import cj_reqcj
import os
import random

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename='myLog.log', filemode='a+', format=FORMAT)

def checkFile(filepath):
    if os.path.isfile(filepath):
        logging.info(filepath+" is exist")
    else:
        logging.error(filepath +" file not found")
        sys.exit()

class Config:
    def __init__(self,s,cookiefile = "cookie.txt",configfile = "config.txt"):
        checkFile(cookiefile)
        cj = cookielib.MozillaCookieJar()
        cj.load(cookiefile, ignore_expires=True, ignore_discard=True)
        cj_reqcj(s, cj)
        checkFile(configfile)
        file = open(configfile, 'r')
        txt = file.readlines()
        file.close()
        if os.path.isfile("userAgent.txt"):
            file = open('userAgent.txt', 'r')
            self.userAgent = file.read()
            file.close()
        else:
            logging.error("userAgent.txt" + " file not found")
            userAgentl = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"]
            self.userAgent = userAgentl[random.randint(0,len(userAgentl)-1)]
        self.user = txt[0].split("#")[0].replace('user"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.password = txt[1].split("#")[0].replace('password"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.time = txt[2].split("#")[0].replace('time"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.id = txt[3].split("#")[0].replace('id"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.specification = txt[4].split("#")[0].replace('specification"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.num = txt[5].split("#")[0].replace('num"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.add = txt[6].split("#")[0].replace('add"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.addnum = txt[7].split("#")[0].replace('addnum"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.free = txt[8].split("#")[0].replace('free"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.payWay = txt[9].split("#")[0].replace('payWay"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.cusName = txt[10].split("#")[0].replace('cusName"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.cusMobile = txt[11].split("#")[0].replace('cusMobile"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.cusZip = txt[12].split("#")[0].replace('cusZip"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.cusAddress = txt[13].split("#")[0].replace('cusAddress"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.recName = txt[14].split("#")[0].replace('recName"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.recMobile = txt[15].split("#")[0].replace('recMobile"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.recZip = txt[16].split("#")[0].replace('recZip"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.recAddress = txt[17].split("#")[0].replace('recAddress"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.cardNO = txt[18].split("#")[0].replace('cardNO"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.cardType = txt[19].split("#")[0].replace('cardType"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.cusBirthday = txt[20].split("#")[0].replace('cusBirthday"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.cusSID = txt[21].split("#")[0].replace('cusSID"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.cusGender = txt[22].split("#")[0].replace('cusGender"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.cardSecurityNO = txt[23].split("#")[0].replace('cardSecurityNO"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.cardExpireDate = txt[24].split("#")[0].replace('cardExpireDate"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.accountMode = txt[25].split("#")[0].replace('accountMode"', "").replace('\n', "").replace('\r', "").replace('"', "")
        self.product = ""
        self.orderData = {}
    def data_fill_check(self):
        Error = 0
        if self.payWay == "card":
            if self.cardType != "VISA" and self.cardType != "MASTER" and self.cardType != "JCB" and self.cardType != "AE":
                Error += 1
                logging.error("cardType error")
            if re.search("[1-2]{1}[0-9]{3}\/[0-9]{2}\/[0-9]{2}", self.cusBirthday) == None:
                Error += 1
                logging.error("cusBirthday error")
            if self.cusGender != "M" and "F":
                Error += 1
                logging.error("cusGender error")
            if re.search("20+[2,3]{1}[0-9]{1}[0,1]{1}[0-9]{1}", self.cardExpireDate) == None:
                Error += 1
                logging.error("cardExpireDate error")
        else:
            Error += 1
            logging.error("payWay error")
        if Error != 0:
            logging.error("Have "+str(Error)+" error in config.")
            sys.exit()
    def savecookie(self,s,cookiefile = "cookie.txt"):
        cj = cookielib.MozillaCookieJar()
        for s_cookie in s.cookies:
            cj.set_cookie(
                cookielib.Cookie(version=0, name=s_cookie.name, value=s_cookie.value, port='80', port_specified=False,
                                 domain=s_cookie.domain, domain_specified=True, domain_initial_dot=False,
                                 path="/", path_specified=True, secure=True,
                                 expires="1569592763",  # s_cookie['expiry']
                                 discard=False, comment=None, comment_url=None, rest=None,
                                 rfc2109=False))
        cj.save(cookiefile)


if __name__ == '__main__':
    print re.search("20+[2,3]{1}[0-9]{1}[0,1]{1}[0-9]{1}", "202610")
    a = "MASTER"
    print a== "MASTER" and a == "v"
    """
    ss = requests.session()
    test = Config(ss)
    print ss.cookies
    print test.user
    print test.password
    print test.time
    print test.id
    print test.specification
    print test.num
    print test.add
    print test.addnum
    print test.free
    print test.payWay
    print test.cusName
    print test.cusMobile
    print test.cusZip
    print test.cusAddress
    print test.recName
    print test.recMobile
    print test.recZip
    print test.recAddress
    print test.cardNO
    print test.cardType
    print test.cusBirthday
    print test.cusSID
    print test.cusGender
    print test.cardSecurityNO
    print test.cardExpireDate
    """




