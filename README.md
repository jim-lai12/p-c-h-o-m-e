# p-c-h-o-m-e
 
用於自動化搶購商品，已經寫成模組化方便使用多線程實現多帳號搶購

以下為example.py內容

s = requests.session()
config = getconfig.Config(s)    用於取得設定
config.data_fill_check()    初步檢查設定


step1 = checkinfo.Checkbeforebuy(config,s)
step1.checkall()    檢查登入狀況，加購相關資訊


step2 = add.Add2car(config,s)
step2.setTimer()    等待設定時間
step2.snapup()    加入購物車


全自動化call api付款(貨到付款，信用卡)相關流程已經完成,歡迎來信商業合作

剩下流程也可以使用我的cookieway模組來把cookie丟給selenium完成手續流程

