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
            self.orderData = {
                'PayWay': 'CC',  # 付款方式，COD為貨到付款。CC信用卡
                'CusName': self.cusName,  # 購買人姓名。
                'CusMobile': self.cusMobile,  # 購買人連絡電話 - 手機。
                'AcceptEDM': 'N',  # 是否願意收到PChome商品特惠通知。
                'CusTel': '',  # 購買人連絡電話 - 市話。
                'CusZip': self.cusZip,  # 購買人郵遞區號。
                'CusAddress': self.cusAddress,  # 購買人地址。
                'ShowCusName': 'N',  # 收貨地址顯示購買人姓名。
                'ContactNo': '',
                'isSyncCust': 'N',
                'RecName': self.recName,  # 收貨人中文姓名。
                'RecTel': '',  # 收貨人連絡電話 - 市話。
                'RecMobile': self.recMobile,  # 收貨人連絡電話 - 手機。
                'RecZip': self.recZip,  # 收貨人郵遞區號。
                'RecAddress': self.recAddress,  # 收貨人地址。
                'AddContact': 'N',  # 資料加入收貨人通訊錄。
                'ConfirmIsLand': 'N',
                'RecMail': '',
                'PaperInvoice': 'N',  # 是否願意將發票進行捐贈。
                'InvoiceType': 'P',  # 個人電子發票。
                'TaxNO': '',  # 發票種類為公司戶電子發票時，統一編號。
                'AddTaxNO': 'N',  # 資料加入公司統編備忘錄。
                'CashPoint': '0',
                'DeviceID': '',
                'DeviceOS': '',
                'DeviceName': '',
                'DeviceOSVersion': '',
                'DeviceAppVersion': '',
                'IsSkipOTP': 'N',
                'availableDepositPoint': '0',
                'availableVoucherPoint': '0',
                'depositUsed': '0',
                'voucherUsed': '0',
                'BindMobile': '',
                # -----------------------信用卡才要
                "RememberCard": "N",  # 記得卡號
                "CardNO": self.cardNO,  # 卡號
                "useRealName": "N",  # 購買同會員資訊
                "CardType": self.cardType,  # 卡別
                "CusBirthday": self.cusBirthday,  # 持卡人生日
                "CusSID": self.cusSID,  # 持卡人身分證字號
                "CusGender": self.cusGender,  # 持卡人性別
                "CardSecurityNO": self.cardSecurityNO,  # 後三碼
                "CardExpireDate": self.cardExpireDate,  # 卡片期限
                "CardMac": "",
                "BankId": "",
                "BUID": "",
                "ship_type": "delivery",  # delivery是貨運
                "ship_only": "N",

            }
        elif self.payWay == "home":
            self.orderData = {
                'PayWay': 'COD',  # 付款方式，COD為貨到付款。CC信用卡
                'CusName': self.cusName,  # 購買人姓名。
                'CusMobile': self.cusMobile,  # 購買人連絡電話 - 手機。
                'AcceptEDM': 'N',  # 是否願意收到PChome商品特惠通知。
                'CusTel': '',  # 購買人連絡電話 - 市話。
                'CusZip': self.cusZip,  # 購買人郵遞區號。
                'CusAddress': self.cusAddress,  # 購買人地址。
                'ShowCusName': 'N',  # 收貨地址顯示購買人姓名。
                'ContactNo': '',
                'isSyncCust': 'N',
                'RecName': self.recName,  # 收貨人中文姓名。
                'RecTel': '',  # 收貨人連絡電話 - 市話。
                'RecMobile': self.recMobile,  # 收貨人連絡電話 - 手機。
                'RecZip': self.recZip,  # 收貨人郵遞區號。
                'RecAddress': self.recAddress,  # 收貨人地址。
                'AddContact': 'N',  # 資料加入收貨人通訊錄。
                'ConfirmIsLand': 'N',
                'RecMail': '',
                'PaperInvoice': 'N',  # 是否願意將發票進行捐贈。
                'InvoiceType': 'P',  # 個人電子發票。
                'TaxNO': '',  # 發票種類為公司戶電子發票時，統一編號。
                'AddTaxNO': 'N',  # 資料加入公司統編備忘錄。
                'CashPoint': '0',
                'DeviceID': '',
                'DeviceOS': '',
                'DeviceName': '',
                'DeviceOSVersion': '',
                'DeviceAppVersion': '',
                'IsSkipOTP': 'N',
                'availableDepositPoint': '0',
                'availableVoucherPoint': '0',
                'depositUsed': '0',
                'voucherUsed': '0',
                'BindMobile': '',
                "ship_type": "delivery",  # delivery是貨運
                "ship_only": "N",
            }
        else:
            Error += 1
            logging.error("payWay error")
        if Error != 0:
            logging.error("Have "+str(Error)+" error in config.")
            sys.exit()
        if self.cusMobile[0:2] != "09":
            self.orderData["CusMobile"] = ""
            self.orderData["CusTel"] = self.cusMobile
        if self.recMobile[0:2] != "09":
            self.orderData["RecMobile"] = ""
            self.orderData["RecTel"] = self.recMobile
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




