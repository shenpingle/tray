#-*- coding:utf-8 -*-
###########################################################################################
#  author: luu
#  info:ADR24小时值守程序
#  Revision: 1.0
"""
    功能说明：   MDR24小时值守程序
    逻辑：       读取设定时间，然后等待至设定时间，执行当日报告下载
    输入参数：   自动填入当天日期，如2014-09-09
"""
###########################################################################################
import myschedule
import datepicker

from mdrtime import *
import deletedance
import report_query
from login2 import login
from utils import *

def crawler_today():
    #抓取今天
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login()
        print u"login Tag(auto today):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(auto today)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)

    deletedance.dodelete(toady_cal())
    report_query.MDR_Report_Query(toady_cal())

ABC = 0

def doWork():
    #do work here
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print "I'm working...", t
    crawler_today()
    global ABC
    ABC = 2

def myrun():
    #
    some = datepicker.readini_minute()[0:5]
    print some

    okcount = some
    while 1:
        print u"设定时间:         ", okcount
        myschedule.clear()
        myschedule.every().day.at(okcount).do(doWork)
        Tag = myschedule.jobs
        print u"当前操作信息日志:                 ", Tag
        global ABC
        if ABC == 2:
            #
            ABC = 0
            print "abc:", ABC
        else:
            pass
        while 1:
            if ABC == 0:
                t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                some = t.split(":")
                p1 = int(some[1])
                p2 = int(some[2])
                if p2 %10 ==0 and p1 %10 ==0:
                    #
                    print u"当前时间:           %s" % t
                myschedule.run_pending()
                time.sleep(1)
            else:
                okcount = datepicker.readini_minute()[0:5]
                print u"设定时间或者新的设定时间 :                  ", okcount
                print "......."
                break

if __name__ == "__main__":
    myrun()