#-*- coding:utf-8 -*-
###########################################################################################
#  author:touchluu2010@gmail.com
#  说明:常量数据
#  Revision: 1.0
###########################################################################################
import urllib2
import cookielib
import time
from mdrtime import *
import os

cookieManager = cookielib.CookieJar()
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

#import url
MDR_HOME_URL = "http://www.adrs.org.cn/sso/login?service=http://www.adrs.org.cn/PF/casAuthUser"
AuthCodeURL = "http://www.adrs.org.cn/sso/authCode.jsp?t=" +  str(time.time())
LOGIN_URL = "http://www.adrs.org.cn/sso/login?service=http://www.adrs.org.cn/PF/casAuthUser?"+str(time.time())

CUR_AUTH_FILE = os.getcwd() + "\\capacha.png"

#common lib url
MDR_JS_ADR = 'http://www.adrs.org.cn/ADR/scripts/lib/adr-common-lib.js'
MDR_JS_MDR = 'http://www.adrs.org.cn/MDR/scripts/lib/mdr-common-lib.js'
MDR_JS_AEFI = 'http://www.adrs.org.cn/AEFI/scripts/lib/aefi-common-lib.js'
MDR_JS_ENGINE = 'http://www.adrs.org.cn/ADR/dwr/engine.js'
MDR_JS_FIND = 'http://www.adrs.org.cn/MDR/scripts/mdr/smdr/findReport.js'
MDR_JS_SEB = 'http://www.adrs.org.cn/MDR/scripts/mdr/smdr/smdrEvaluateBrowse.js'
MDR_JS_ASM = 'http://www.adrs.org.cn/MDR/scripts/mdr/smdr/advanceSearchManager.js'
MDR_JS_BM = 'http://www.adrs.org.cn/MDR/scripts/mdr/bulletin/BulletinManager.js'
MDR_JS_AEM = 'http://www.adrs.org.cn/MDR/scripts/mdr/am/AmEveManage.js'
MDR_JS_GRM = 'http://www.adrs.org.cn/MDR/scripts/mdr/gmdr/GMDRReportManager.js'
MDR_JS_GEM = 'http://www.adrs.org.cn/MDR/scripts/mdr/gmdr/GMDRReportExamineManager.js'
MDR_JS_PI = 'http://www.adrs.org.cn/MDR/scripts/mdr/personal/PersonalInfo.js'
MDR_JS_PM = 'http://www.adrs.org.cn/MDR/scripts/mdr/rm/RemindManager.js'
MDR_JS_COM = 'http://www.adrs.org.cn/MDR/scripts/mdr/common/common.js'
MDR_JS_TB = 'http://www.adrs.org.cn/MDR/scripts/mdr/personal/TemporaryBox.js'

#mdr home page
secondHome = 'http://www.adrs.org.cn/MDR/scripts/mdr/index.jsp'
MDR_1 = 'http://www.adrs.org.cn/MDR/dwr/interface/smdrHisReportService.js'
MDR_2 = 'http://www.adrs.org.cn/MDR/dwr/interface/smdReportEvalService.js'
MDR_3 = 'http://www.adrs.org.cn/MDR/dwr/interface/findListSmdReportService.js'
MDR_4 = 'http://www.adrs.org.cn/MDR/dwr/interface/eventService.js'

#mdr query page
thirdHome = 'http://www.adrs.org.cn/MDR/scripts/mdr/smdr/queryCondition.jsp'

my_today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
#report total
#http://www.adrs.org.cn/MDR/ep/smdrFindList/FindListSmdReportService/query/
totalHome = 'http://www.adrs.org.cn/MDR/ep/smdrFindList/FindListSmdReportService/query/'
#my_today
totalparams = {"funcID":"QUERY_DATA","userID":78919,"operations":[{"actionName":"query","operationDatas":[{"PROD_NAME_1540":"","REG_NO_1540":"","DEVICE_CLASS_ID_1540":"","DEVICE_CLASS_NAME_1540":"","REPORT_DATE_START":"2001-01-01","REPORT_DATE_END":my_today,"REPORT_NUMBER_1540":"","CREATE_DATE_START":"","CREATE_DATE_END":"","SUPERVISE_ORG_ID_1540":"","SUPERVISE_ORG_NAME_1540":"","MAN_NAME_1540":"","REPORT_UNIT_NAME_1540":"","PATIENT_NAME_1540":"","EVALUATE_DATE_START":"","EVALUATE_DATE_END":"","MANAGE_CATEGORY_1540":"","listid":"1540","start":0,"limit":100}]}]}
#totalparams ={"funcID":"0000000","userID":608575,"operations":[{"actionName":"query","operationDatas":[{"PROD_NAME_1540":"","REG_NO_1540":"","DEVICE_CLASS_ID_1540":"","DEVICE_CLASS_NAME_1540":"","REPORT_DATE_START":"","REPORT_DATE_END":"","REPORT_NUMBER_1540":"","CREATE_DATE_START":"2015-06-10","CREATE_DATE_END":"2015-07-10","SUPERVISE_ORG_ID_1540":"","SUPERVISE_ORG_NAME_1540":"","MAN_NAME_1540":"","REPORT_UNIT_NAME_1540":"","PATIENT_NAME_1540":"","EVALUATE_DATE_START":"","EVALUATE_DATE_END":"","MANAGE_CATEGORY_1540":"","listid":"1540","start":0,"limit":10}]}]}}
#pusr
Psur_url = u"http://www.adrs.org.cn/ADR/ep/PSURService/PSURService/queryPSURForSearch/"
File_url = u"http://www.adrs.org.cn/ADR/ep/PSURService/PSURService/queryFileInfoForJSP"

