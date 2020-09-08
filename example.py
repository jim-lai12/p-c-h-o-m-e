# -*- coding: utf-8 -*-
from tool import getconfig
from tool import checkinfo
import requests
from tool import add
from tool import order

s = requests.session()
config = getconfig.Config(s)
config.data_fill_check()


step1 = checkinfo.Checkbeforebuy(config,s)
step1.checkall()


step2 = add.Add2car(config,s)
step2.setTimer()
step2.snapup()


#已完成全自動化付款,歡迎商業合作
"""
step3 = order.Order(config,s)
step3.checkCar()#not necessary
step3.senOrder()
"""


