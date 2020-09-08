import json
import re
import cookielib
import requests
from Crypto.Cipher import AES
import base64
from hashlib import md5
from Crypto import Random
import random
import logging
import sys
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='myLog.log', filemode='a+', format=FORMAT)

#data ='try{jsonp_button([{"Seq":19197500,"Id":"DXAO4V-A9008LS5W-000","Price":{"M":0,"P":8990,"Prime":""},"Qty":20,"ButtonType":"ForSale","SaleStatus":1,"isPrimeOnly":0,"SpecialQty":0},{"Seq":20418680,"Id":"DXAO4V-A9008LS5W-004","Price":{"M":0,"P":8990,"Prime":""},"Qty":0,"ButtonType":"OrderRefill","SaleStatus":0,"isPrimeOnly":0,"SpecialQty":0},{"Seq":19197501,"Id":"DXAO4V-A9008LS5W-001","Price":{"M":0,"P":8990,"Prime":""},"Qty":20,"ButtonType":"ForSale","SaleStatus":1,"isPrimeOnly":0,"SpecialQty":0},{"Seq":19197502,"Id":"DXAO4V-A9008LS5W-002","Price":{"M":0,"P":8990,"Prime":""},"Qty":20,"ButtonType":"ForSale","SaleStatus":1,"isPrimeOnly":0,"SpecialQty":0}]);}catch(e){if(window.console){console.log(e);}}'
#'try{jsonp_gift({"DGBJDE-1900ARTRQ":[{"Id":1941619,"Name":"\u8d08\u54c1","isGiveAll":1,"isShowPic":0,"MaxPick":0,"Item":[{"Seq":24566964,"Id":"DGBJAS-A900ALH6F-000","Name":"Switch \u9ad8\u6e05\u92fc\u5316\u73bb\u7483\u4fdd\u8b77\u8cbc \u4fdd\u8b77\u819c\uff08\u96d9\u5165\uff09","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJASA900ALH6F\/000001_1586339272.jpg","S":"\/items\/DGBJASA900ALH6F\/000002_1586339272.jpg"},"Qty":20,"Volume":{"Length":19,"Width":12,"Height":1}}]},{"Id":1937515,"Name":"\u4efb\u9078\u904a\u6232x2","isGiveAll":0,"isShowPic":1,"MaxPick":2,"Item":[{"Seq":22775285,"Id":"DGBJBH-A900A29JQ-000","Name":"Switch\u904a\u6232 \u661f\u4e4b\u5361\u6bd4 \u65b0\u661f\u540c\u76df-\u4e2d\u6587\u7248(\u5c08)","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900A29JQ\/000001_1559722397.jpg","S":"\/items\/DGBJBHA900A29JQ\/000002_1559722397.jpg"},"Qty":20,"Volume":{"Length":17,"Width":10,"Height":1}},{"Seq":23779823,"Id":"DGBJBH-A900AC5OO-000","Name":"Switch\u904a\u6232 \u8d85\u7d1a\u746a\u5229\u6b50\u5275\u4f5c\u5bb62 (Super Mario Maker2)-\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AC5OO\/000001_1572591826.jpg","S":"\/items\/DGBJBHA900AC5OO\/000002_1572591826.jpg"},"Qty":20,"Volume":{"Length":17,"Width":12,"Height":1}},{"Seq":23779824,"Id":"DGBJBH-A900AC5OP-000","Name":"Switch\u904a\u6232 \u746a\u5229\u6b50\u7db2\u7403 \u738b\u724c\u9ad8\u624b-\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AC5OP\/000001_1572591719.jpg","S":"\/items\/DGBJBHA900AC5OP\/000002_1572591719.jpg"},"Qty":19,"Volume":{"Length":17,"Width":12,"Height":1}},{"Seq":23779828,"Id":"DGBJBH-A900AC5OT-000","Name":"Switch\u904a\u6232 \u8def\u6613\u5409\u6d0b\u6a133 (\u8def\u6613\u5409\u9b3c\u5c4b3)-\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AC5OT\/000001_1572591598.jpg","S":"\/items\/DGBJBHA900AC5OT\/000002_1572591598.jpg"},"Qty":0,"Volume":{"Length":17,"Width":11,"Height":1}},{"Seq":23779811,"Id":"DGBJBH-A900AC5PD-000","Name":"Switch\u904a\u6232 \u746a\u5229\u6b50&\u7d22\u5c3c\u514bAT\u6771\u4eac\u5967\u904b\u2013\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AC5PD\/000001_1572591305.jpg","S":"\/items\/DGBJBHA900AC5PD\/000002_1572591305.jpg"},"Qty":10,"Volume":{"Length":17,"Width":11,"Height":1}},{"Seq":23779817,"Id":"DGBJBH-A900AC5PJ-000","Name":"Switch\u904a\u6232 New \u8d85\u7d1a\u746a\u5229\u6b50\u5144\u5f1f U \u8c6a\u83ef\u7248\u2013\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AC5PJ\/000001_1572591077.jpg","S":"\/items\/DGBJBHA900AC5PJ\/000002_1572591077.jpg"},"Qty":20,"Volume":{"Length":17,"Width":11,"Height":1}},{"Seq":23779851,"Id":"DGBJBH-A900AC5PX-000","Name":"Switch\u904a\u6232 \u7267\u5834\u7269\u8a9e \u91cd\u805a\u7926\u77f3\u93ae\u2013\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AC5PX\/000001_1572590416.jpg","S":"\/items\/DGBJBHA900AC5PX\/000002_1572590416.jpg"},"Qty":12,"Volume":{"Length":17,"Width":10,"Height":1}},{"Seq":23780294,"Id":"DGBJBH-A900AC5WA-000","Name":"Switch\u904a\u6232 \u6e1b\u91cd\u62f3\u64ca(\u5065\u8eab\u62f3\u64ca)Fitness Boxing\u2013\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AC5WA\/000001_1572507893.jpg","S":"\/items\/DGBJBHA900AC5WA\/000002_1572507893.jpg"},"Qty":20,"Volume":{"Length":17,"Width":12,"Height":2}},{"Seq":24005698,"Id":"DGBJBH-A900AET4O-000","Name":"Switch\u904a\u6232 \u738b\u724c\u91e3\u624bNintendo Switch\u7248(Ace Angler)\u2013\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AET4O\/000001_1576049853.jpg","S":"\/items\/DGBJBHA900AET4O\/000002_1576049853.jpg"},"Qty":0,"Volume":{"Length":17,"Width":11,"Height":1}},{"Seq":24914901,"Id":"DGBJBH-A900APLYI-000","Name":"Switch\u904a\u6232 \u6f06\u5f48\u5927\u4f5c\u62302-\u65e5\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900APLYI\/000001_1591929567.jpg","S":"\/items\/DGBJBHA900APLYI\/000002_1591929567.jpg"},"Qty":20,"Volume":{"Length":17,"Width":11,"Height":1}},{"Seq":25083430,"Id":"DGBJBH-A900ARJ7Y-000","Name":"Switch\u904a\u6232 \u521d\u97f3\u672a\u4f86 Project DIVA MEGA39s\u2013\u4e2d\u65e5\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900ARJ7Y\/000001_1594784535.jpg","S":"\/items\/DGBJBHA900ARJ7Y\/000002_1594784535.jpg"},"Qty":2,"Volume":{"Length":17,"Width":11,"Height":1}},{"Seq":25036713,"Id":"DGBJBH-A900AR06K-000","Name":"Switch\u904a\u6232 \u8000\u897f\u7684\u624b\u5de5\u4e16\u754c\u2013\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AR06K\/000001_1594109997.jpg","S":"\/items\/DGBJBHA900AR06K\/000002_1594109997.jpg"},"Qty":0,"Volume":{"Length":17,"Width":10,"Height":1}},{"Seq":23779876,"Id":"DGBJBH-A900AC5QG-000","Name":"Switch\u904a\u6232 \u8056\u706b\u964d\u9b54\u9304 \u98a8\u82b1\u96ea\u6708-\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AC5QG\/000001_1572590119.jpg","S":"\/items\/DGBJBHA900AC5QG\/000002_1572590119.jpg"},"Qty":19,"Volume":{"Length":17,"Width":12,"Height":1}},{"Seq":23780252,"Id":"DGBJBH-A900AC5V9-000","Name":"Switch\u904a\u6232 2020 \u6771\u4eac\u5967\u904b THE OFFICIAL VIDEO GAME-\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AC5V9\/000001_1572589961.jpg","S":"\/items\/DGBJBHA900AC5V9\/000002_1572589961.jpg"},"Qty":10,"Volume":{"Length":17,"Width":12,"Height":1}},{"Seq":24005804,"Id":"DGBJBH-A900AET6Z-000","Name":"Switch\u904a\u6232 \u5deb\u5e2b3\uff1a\u72c2\u7375 \u5b8c\u5168\u7248(The Witcher 3: Wild Hunt)\u2013\u4e2d\u82f1\u6587\u5408\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AET6Z\/000001_1576050229.jpg","S":"\/items\/DGBJBHA900AET6Z\/000002_1576050229.jpg"},"Qty":0,"Volume":{"Length":18,"Width":12,"Height":2}},{"Seq":23843550,"Id":"DGBJBH-A900ACYJT-000","Name":"Switch\u904a\u6232 \u5bf6\u53ef\u5922 \u76fe-\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900ACYJT\/000001_1573456642.jpg","S":"\/items\/DGBJBHA900ACYJT\/000002_1573456642.jpg"},"Qty":2,"Volume":{"Length":17,"Width":11,"Height":1}},{"Seq":24476307,"Id":"DGBJBH-A900AKBQB-000","Name":"Switch\u904a\u6232 \u85a9\u723e\u9054\u50b3\u8aaa \u66e0\u91ce\u4e4b\u606f\u2013\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AKBQB\/000001_1584679223.jpg","S":"\/items\/DGBJBHA900AKBQB\/000002_1584679223.jpg"},"Qty":20,"Volume":{"Length":17,"Width":11,"Height":1}}]},{"Id":1937517,"Name":"\u4efb\u9078\u904a\u6232x1","isGiveAll":0,"isShowPic":1,"MaxPick":1,"Item":[{"Seq":22856928,"Id":"DGBJBH-A900A3ENM-000","Name":"Switch\u904a\u6232 BLADE ARCUS Rebellion from Shining-\u4e2d\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900A3ENM\/000001_1561004484.jpg","S":"\/items\/DGBJBHA900A3ENM\/000002_1561004484.jpg"},"Qty":0,"Volume":{"Length":17,"Width":11,"Height":1}},{"Seq":25036666,"Id":"DGBJBH-A900AR04K-000","Name":"Switch\u904a\u6232 \u6975\u9650\u51f8\u8d77 \u840c\u60c5\u6c34\u6676 H (\u9650\u754c\u51f8\u8d77) -\u4e2d\u65e5\u6587\u7248","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AR04K\/000001_1594109368.jpg","S":"\/items\/DGBJBHA900AR04K\/000002_1594109368.jpg"},"Qty":0,"Volume":{"Length":17,"Width":11,"Height":1}},{"Seq":25036663,"Id":"DGBJBH-A900AR04I-000","Name":"Switch\u904a\u6232 \u65b0\u6b21\u5143\u6230\u8a18 \u6230\u6a5f\u5c11\u5973 VII-\u97d3\u6587\u7248(\u652f\u63f4\u4e2d\u6587)","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJBHA900AR04I\/000001_1594110922.jpg","S":"\/items\/DGBJBHA900AR04I\/000002_1594110922.jpg"},"Qty":0,"Volume":{"Length":17,"Width":11,"Height":1}}]},{"Id":1946672,"Name":"\u5468\u908a","isGiveAll":0,"isShowPic":1,"MaxPick":2,"Item":[{"Seq":24693634,"Id":"DGBJC0-A900AMY4Q-000","Name":"\u4efb\u5929\u5802Switch JoyCon\u624b\u628a\u5957\u88dd2\u5165-\u7d93\u5178\u9ed1 (TNS-851)","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJC0A900AMY4Q\/000001_1588232178.jpg","S":"\/items\/DGBJC0A900AMY4Q\/000002_1588232178.jpg"},"Qty":20,"Volume":{"Length":15,"Width":15,"Height":5}},{"Seq":24119523,"Id":"DGBJC0-A900AG5MC-000","Name":"Switch\u5468\u908a \u4efb\u5929\u5802\u5c08\u5c6c \u904a\u6232\u7247\/\u8a18\u61b6\u536124\u5165\u6536\u7d0d\u76d2-\u6676\u900f\u9ed1","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJC0A900AG5MC\/000001_1578029968.jpg","S":"\/items\/DGBJC0A900AG5MC\/000002_1578029968.jpg"},"Qty":20,"Volume":{"Length":10,"Width":8,"Height":3}},{"Seq":21055160,"Id":"DGBJDE-A9009ENCH-000","Name":"\u4efb\u5929\u5802Switch\u73bb\u7483\u87a2\u5e55\u4fdd\u8b77\u8cbc+\u9632\u587510\u4ef6\u7d44+\u985e\u6bd4\u6416\u687f\u5957\u5957\u88dd","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJDEA9009ENCH\/000001_1536735525.jpg","S":"\/items\/DGBJDEA9009ENCH\/000002_1536735525.jpg"},"Qty":20,"Volume":{"Length":23,"Width":11,"Height":2}},{"Seq":24119560,"Id":"DGBJC0-A900AG5MU-000","Name":"Switch\u5468\u908a \u4efb\u5929\u5802 \u591a\u529f\u80fd\u767e\u8b8a\u4e3b\u6a5f\u6536\u7d0d\u5305","Spec":"","Group":"","Pic":{"B":"\/items\/DGBJC0A900AG5MU\/000001_1578030621.jpg","S":"\/items\/DGBJC0A900AG5MU\/000002_1578030621.jpg"},"Qty":20,"Volume":{"Length":25,"Width":18,"Height":3}}]}]});}catch(e){if(window.console){console.log(e);}}'
#'try{jsonp_add({"DEAXCA-A900AM1EQ":[{"Seq":24617921,"Id":"DEAXCA-A900AM1EQ-000","Name":"\u3010SUPER LIGTH\u301113\u74e6\u767d\u5149\u9ad8\u4eae\u5ea6LED\u7bc0\u80fd\u71c8\u6ce1-1\u5165","Spec":"","Group":"","Price":{"M":199,"P":55},"Pic":{"B":"\/items\/DEAXCAA900AM1EQ\/000001_1591331656.jpg","S":"\/items\/DEAXCAA900AM1EQ\/000002_1591331656.jpg"},"Qty":20,"isWarranty":0}],"DEBD9V-A900AR9SO":[{"Seq":25060228,"Id":"DEBD9V-A900AR9SO-000","Name":"\u2261SPACE\u2261 45\u54081-\u7cbe\u5bc6\u87ba\u7d72\u8d77\u5b50\u7d44","Spec":"","Group":"","Price":{"M":0,"P":249},"Pic":{"B":"\/items\/DEBD9VA900AR9SO\/000001_1594362600.jpg","S":"\/items\/DEBD9VA900AR9SO\/000002_1594362600.jpg"},"Qty":20,"isWarranty":0}]});}catch(e){if(window.console){console.log(e);}}'
#'try{jsonp_button([{"Seq":19197500,"Id":"DXAO4V-A9008LS5W-000","Price":{"M":0,"P":8990,"Prime":""},"Qty":20,"ButtonType":"ForSale","SaleStatus":1,"isPrimeOnly":0,"SpecialQty":0},{"Seq":20418680,"Id":"DXAO4V-A9008LS5W-004","Price":{"M":0,"P":8990,"Prime":""},"Qty":0,"ButtonType":"OrderRefill","SaleStatus":0,"isPrimeOnly":0,"SpecialQty":0},{"Seq":19197501,"Id":"DXAO4V-A9008LS5W-001","Price":{"M":0,"P":8990,"Prime":""},"Qty":20,"ButtonType":"ForSale","SaleStatus":1,"isPrimeOnly":0,"SpecialQty":0},{"Seq":19197502,"Id":"DXAO4V-A9008LS5W-002","Price":{"M":0,"P":8990,"Prime":""},"Qty":20,"ButtonType":"ForSale","SaleStatus":1,"isPrimeOnly":0,"SpecialQty":0}]);}catch(e){if(window.console){console.log(e);}}'


def parseJson(data):
    data = re.findall('\((?P<showid>.+?)\);}', data)[0]
    if data[0] == "[":
        data = json.loads(data)
    elif data[0] == "{":
        data = json.loads(data)
    else:
        logging.error("Parse error\n data")
        sys.exit()
    return data

"""
if type(data) == dict:
    print data.keys()
elif type(data) == list:
    for item in data:
        print item.keys()
"""





def cj_reqcj(s,cj):
    for item in cj:
        cookiesobject = requests.cookies.create_cookie(domain=item.domain, name=item.name, value=item.value)
        s.cookies.set_cookie(cookiesobject)


def reqcj_cj(s,cj):
    for s_cookie in s.cookies:
        cj.set_cookie(
            cookielib.Cookie(version=0, name=s_cookie.name, value=s_cookie.value, port='80', port_specified=False,
                             domain=s_cookie.domain, domain_specified=True, domain_initial_dot=False,
                             path="/", path_specified=True, secure=True,
                             expires="1569592763",  # s_cookie['expiry']
                             discard=False, comment=None, comment_url=None, rest=None,
                             rfc2109=False))


def dict2str(dic):
    string = "{"
    for i in dic:
        string += '"'+i+'":'
        if type(dic[i]) == str :
            string += '"'+dic[i]+'",'
        elif type(dic[i]) == int :
            string += str(dic[i])+','
        elif type(dic[i]) == list :
            if len(dic[i]) == 0:
                string += str(dic[i])+","
            elif type(dic[i][0]) == dict:
                for j in dic[i]:
                    string += dict2str(j)+","
            else:
                string += str(dic[i])+","
    string +="}}}}}forreplace"
    string = string.replace(",}}}}}forreplace","}")
    return string



def randomndigit(n):
    out = ""
    for i in range(n):
        out += str(random.randint(0,9))
    return int(out)




def base36encode(number):
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    alphabet, base36 = ['0123456789abcdefghijklmnopqrstuvwxyz', '']

    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]


def base36decode(number):
    return int(number, 36)





def pad(data):
    length = 16 - (len(data) % 16)
    return data + (chr(length)*length).encode()

def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

def bytes_to_key(data, salt, output=48):
    # extended from https://gist.github.com/gsakkis/4546068
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]

def encrypt_aes(message, passphrase):
    salt = Random.new().read(8)
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(message)))

def decrypt_aes(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))




if __name__ == '__main__':
    data = 'try{jsonp_addcart({"PRODTOTAL":0,"PRODCOUNT":0,"TYPE":"BIGCAR","PRODADD":"0","ISSALEOUT":0});}catch(e){if(window.console){console.log(e);}}'
    #'try{jsonp_button([{"Seq":21845293,"Id":"DRAD1R-A9009PTP3-000","Price":{"M":0,"P":8800,"Prime":""},"Qty":20,"ButtonType":"ForSale","SaleStatus":1,"isPrimeOnly":0,"SpecialQty":0}]);}catch(e){if(window.console){console.log(e);}}'
    #'try{jsonp_button([{"Seq":19197500,"Id":"DXAO4V-A9008LS5W-000","Price":{"M":0,"P":8990,"Prime":""},"Qty":20,"ButtonType":"ForSale","SaleStatus":1,"isPrimeOnly":0,"SpecialQty":0},{"Seq":20418680,"Id":"DXAO4V-A9008LS5W-004","Price":{"M":0,"P":8990,"Prime":""},"Qty":0,"ButtonType":"OrderRefill","SaleStatus":0,"isPrimeOnly":0,"SpecialQty":0},{"Seq":19197501,"Id":"DXAO4V-A9008LS5W-001","Price":{"M":0,"P":8990,"Prime":""},"Qty":20,"ButtonType":"ForSale","SaleStatus":1,"isPrimeOnly":0,"SpecialQty":0},{"Seq":19197502,"Id":"DXAO4V-A9008LS5W-002","Price":{"M":0,"P":8990,"Prime":""},"Qty":20,"ButtonType":"ForSale","SaleStatus":1,"isPrimeOnly":0,"SpecialQty":0}]);}catch(e){if(window.console){console.log(e);}}'
    data = parseJson(data)
    print data
    if type(data) == dict:
        print data.keys()
    elif type(data) == list:
        print len(data)
        for item in data:
            print item.keys()
    print type(data["ISSALEOUT"])


