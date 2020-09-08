# -*- coding: utf-8 -*-

from selenium import webdriver
import random
import cookielib


driver = webdriver.Chrome("chromedriver.exe")




driver.get("https://24h.pchome.com.tw/")
i = raw_input("after sign in enter something")


cookie = driver.get_cookies()

print cookie
cj = cookielib.MozillaCookieJar()
for s_cookie in cookie:
    cj.set_cookie(
        cookielib.Cookie(version=0, name=s_cookie['name'], value=s_cookie['value'], port='80', port_specified=False,
                         domain=s_cookie['domain'], domain_specified=True, domain_initial_dot=False,
                         path=s_cookie['path'], path_specified=True, secure=s_cookie['secure'],
                         expires="1569592763",#s_cookie['expiry']
                          discard=False, comment=None, comment_url=None, rest=None,
                         rfc2109=False))
cj.save("cookie" + ".txt", ignore_discard=True, ignore_expires=True)




