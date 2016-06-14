#-*- coding:utf-8 -*-
###########################################################################################
#  author: luu
#  info:ADR24小时值守程序
#  Revision: 1.0
"""
    功能说明：   ADR24小时值守程序
    逻辑：       读取设定时间，然后等待至设定时间，执行当日报告下载
    输入参数：   自动填入当天日期，如2014-09-09
"""
###########################################################################################

import myschedule
import datepicker
from mdrtime import *
import main_adr

ABC = 0

def doWork():
    #do work here
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print "I'm working...", t
    main_adr.crawler_today()
    global ABC
    ABC = 2

def myrun():
    #
    some = datepicker.readini_minute_adr()[0:5]
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
                #print u"当前时间:           %s" % t
                some = t.split(":")
                p1 = int(some[1])
                p2 = int(some[2])
                if p2 %10 ==0 and p1 %10 ==0:
                    #
                    print u"当前时间:           %s" % t
                myschedule.run_pending()
                time.sleep(1)
            else:
                okcount = datepicker.readini_minute_adr()[0:5]
                print u"设定时间或者新的设定时间 :                  ", okcount
                print "......."
                break

if __name__ == "__main__":
    myrun()