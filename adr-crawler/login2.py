#-*- coding:utf-8 -*-
###########################################################################################
#  author:luu
#  说明:login函数
#  Revision: 1.0
#1.2014-10-14,修改逻辑
###########################################################################################
from common import *
from utils import *
from readyaml import readlogininfo

def login():
    #
    send_url(MDR_HOME_URL)
    #获取验证图片
    #send_url(AuthCodeURL)
    #获取验证码数据
    output = open(CUR_AUTH_FILE, 'wb')
    output.write(send_url(AuthCodeURL).read())
    output.close()

    somedata = readlogininfo()
    name = somedata[0]
    password = somedata[1]
    #print name,password

    code = getcode()
    print u"验证码，如若看到不是4位数字，请重新使用此操作......:", code
    #www.adrs.org.cn:114.255.93.220
    login_postdata = u"username=%s&password=%s&lt=e1s1&_eventId=submit&authCode=%s&ap=114.255.93.220" % (name, password,code)
    login_data = send_post(LOGIN_URL, login_postdata)
    
    Login_Check = login_data.find('<body onload="init();" id="cas">')
    if Login_Check == -1:
        is_login = True
    else:
        #此句表明已经跳转至login页面
        print u"login 失败",Login_Check
        return False

    send_url(MDR_JS_ADR)
    send_url(MDR_JS_MDR)
    send_url(MDR_JS_AEFI)
    send_url(MDR_JS_ENGINE)

    s2 = send_url(secondHome)
    s3 = send_url(thirdHome)


    return is_login

#main
if __name__ == "__main__":
    print login()