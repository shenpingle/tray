#-*- coding:utf-8 -*-
# coding=utf8

#*
#*  此文件包含登录相关功能实现
#*

import os,sys,urllib2
import cookielib,StringIO,gzip,time,random,re
import utils

#获取 authcode的URL
ADR_HOME_URL = "http://www.adrs.org.cn/sso/login?service=http%3A%2F%2Fwww.adrs.org.cn%2FPF%2FcasAuthUser"

#获取验证码图片的URL
AuthCodeURL = "http://www.adrs.org.cn/sso/authCode.jsp"


#抓取的authcode图片，保存到本地的临时文件名，若修改，要同时修改getcode.bat里面的名字
CUR_AUTH_FILE = "capacha.png"
    

def _getAuthCode(data):
    '''获取登录验证码'''
    fp = open(CUR_AUTH_FILE,"wb")
    fp.write(data)
    fp.flush()
    fp.close()

    ret = os.popen("getcode.bat", "r")
    results = ret.readlines()
    code = results[9].strip()
    return code
        
def login(cookieManager, username, password):
    '''登录'''
    
    #获取session_id
    utils.getUrlResponse(cookieManager, ADR_HOME_URL)    
    
    #获取authcode
    fp_auth = utils.getUrlResponse(cookieManager, AuthCodeURL) 
    authcode = _getAuthCode(fp_auth)
    print "authcode:",authcode
    
    #拼接登录信息
    login_data = "username=%s&password=%s&lt=e1s1&_eventId=submit&authCode=%s&ap=114.255.93.220" % (username, password, authcode)
    
    #登录
    utils.getUrlResponse(cookieManager, ADR_HOME_URL, data=login_data)
    
    opt = {
        "Referer" : 'http://www.adrs.org.cn/PF/page/frameWork.html'
        }
    utils.getUrlResponse(cookieManager, 'http://www.adrs.org.cn/ADR/scripts/lib/adr-common-lib.js', opt_headers=opt)
    
    utils.getUrlResponse(cookieManager, 'http://www.adrs.org.cn/MDR/scripts/lib/mdr-common-lib.js', opt_headers=opt)
    
    utils.getUrlResponse(cookieManager, 'http://www.adrs.org.cn/AEFI/scripts/lib/aefi-common-lib.js', opt_headers=opt)
    
    utils.getUrlResponse(cookieManager, 'http://www.adrs.org.cn/ADR/dwr/engine.js', opt_headers=opt)
    
    return len(cookieManager)>=5 #大于等于5，登录成功 
    