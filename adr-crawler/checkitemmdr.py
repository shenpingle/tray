#-*- coding:utf-8 -*-
###########################################################################################
#  author: luu
#  info:获取单月智能报表总数（MDR）
#  Revision: 1.0
"""
    功能说明：   获取单月智能报表总数（MDR）
    逻辑：       获得指定参数，取得相应报告条数
    输入参数：   依次选择输入年份、开始月份、结束月份
    输出参数：   报告条数
"""
###########################################################################################

import calendar as cal
import time
ThisYear = time.strftime('%Y-%m-%d', time.localtime(time.time()))[0:4]
#ThisMonth = time.strftime('%Y-%m-%d', time.localtime(time.time()))[5:7]
ThisMonth = time.strftime('%Y-%m-%d', time.localtime(time.time()))[6:7]
Format = "%d-%d-%d:%d-%d-%d"

from login2 import login
from utils import *
import codecs
from config import *

def timetomonth3(y, m1, m2):
    #
    print u"计算时间"
    month_a = []
    month_b = []
    for m in range(m1, m2+1):
        d = cal.monthrange(y, m)
        const_time_all = Format % (y, m, 1, y, m, d[1])
        const_time_temp = const_time_all.split(":")
        const_time_a = const_time_temp[0]
        const_time_b = const_time_temp[1]
        month_a.append(const_time_a)
        month_b.append(const_time_b)
        #print "month:", const_time_temp
    return [month_a, month_b]

def harvest(sometime):
    #
    print u"正在login..."
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login()
        print u"login Tag (MDR list):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            print u"6次login失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)

    #
    send_url(secondHome)
    print u"已经登录成功"

    #mdr
    send_url(thirdHome)
    #获取记录条数总记录
    stack = sometime
    _stack = stack[0]
    stack_l = len(_stack)
    reportlog = codecs.open('item.txt', 'a', 'utf-8')
    myconn = myconnect()
    mycu = myconn.cursor()

    for i in range(stack_l):
        #
        print u"正在读取记录条数..."
        out = _stack.pop()
        out1 = stack[1].pop()
        const_time_o = out1.split("-")
        const_time_o_ = out.split("-")
        yaer = const_time_o_[0]
        month = const_time_o_[1]
        #print yaer, month
        mycu.execute("delete from mdr_checklist where CheckTag='Q' and Year=%s and Month=%s" % (yaer, month))
        myconn.commit()
        totalparamsx = {"funcID":"QUERY_DATA","userID":78919,"operations":[{"actionName":"query","operationDatas":[{"PROD_NAME_1540":"","REG_NO_1540":"","DEVICE_CLASS_ID_1540":"","DEVICE_CLASS_NAME_1540":"","REPORT_DATE_START":out,"REPORT_DATE_END":out1,"REPORT_NUMBER_1540":"","CREATE_DATE_START":"","CREATE_DATE_END":"","SUPERVISE_ORG_ID_1540":"","SUPERVISE_ORG_NAME_1540":"","MAN_NAME_1540":"","REPORT_UNIT_NAME_1540":"","PATIENT_NAME_1540":"","EVALUATE_DATE_START":"","EVALUATE_DATE_END":"","MANAGE_CATEGORY_1540":"","listid":"1540","start":0,"limit":100}]}]}
        _idcdata = send_post_json(totalHome, totalparamsx)
        #print totalparamsx
        _data = json.loads(_idcdata)
        usa = _data['ResponseMessage']['operations'][0]['pageTotal']
        total_usa = int(usa)
        print out, out1
        print u"报告条数:",str(total_usa)
        if int(const_time_o[1])-int(const_time_o_[1])> 10:
            mycu.execute(
            "insert into mdr_checklist (BeginDate,EndDate,Item,Tag) "
            "value(%s,%s,%s,%s)", (out, out1, str(total_usa), "Y"))
            myconn.commit()
        else:
            mycu.execute(
                "insert into mdr_checklist (BeginDate,EndDate,Item,Tag,CheckTag,Year,Month) "
                "value(%s,%s,%s,%s,%s,%s,%s)", (out, out1, str(total_usa), "M", "Q", yaer, month))
            myconn.commit()
    reportlog.close()

    print u"本次任务已经结束"

def myauto(t1, t2, t3):
    t1 = int(t1)
    t2 = int(t2)
    t3 = int(t3)
    some = timetomonth3(t1, t2, t3)
    harvest(some)
if __name__ == '__main__':
    #some = timetomonth3(2014, 3, 5)
    #print some
    t1 = int("2014")
    t2 = int("2")
    t3 = int("5")
    myauto(t1, t2, t3)