#-*- coding:utf-8 -*-
###########################################################################################
#  author:luu
#  说明:MDR主函数，封装各个功能函数
#  Revision: 1.0
#1.2014-10-14,修改login import
#2.2014-10-14,删除多余import
###########################################################################################
from mdrtime import *
import deletedance
import report_query 
from login2 import login
from utils import *
import mdr_parse

def crawler_last_year():
    #抓取上一年度
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login()
        print u"login Tag(last_year):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(last_year)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)

    deletedance.dodelete(last_year_cal())
    report_query.MDR_Report_Query(last_year_cal())

def crawler_first_half_year():
    #抓取上半年度
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login()
        print u"login Tag(first_half_year):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(first_half_year)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)
    deletedance.dodelete(halfyear_before_cal())
    report_query.MDR_Report_Query(halfyear_before_cal())

def crawler_second_half_year():
    #抓取下半年度
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login()
        print u"login Tag(second_half_year):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(second_half_year)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)

    deletedance.dodelete(halfyear_after_cal())
    report_query.MDR_Report_Query(halfyear_after_cal())

def crawler_current_week():
    #抓取本周
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login()
        print u"login Tag(current_week):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(current_week)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)

    deletedance.dodelete(current_week_cal())
    report_query.MDR_Report_Query(current_week_cal())

def crawler_last_week():
    #抓取上周
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login()
        print u"login Tag(last_week):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(last_week)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)

    deletedance.dodelete(last_week_cal())
    report_query.MDR_Report_Query(last_week_cal())

def crawler_last_month():
    #抓取上月
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login()
        print u"login Tag(last_month):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(last_month)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)

    deletedance.dodelete(last_month_cal())
    report_query.MDR_Report_Query(last_month_cal())

def crawler_today():
    #抓取今天
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login()
        print u"login Tag(today):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(today)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)

    deletedance.dodelete(toady_cal())
    report_query.MDR_Report_Query(toady_cal())


def crawler_anytime():
    #
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login()
        print u"login Tag(anytime):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(anytime)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)

    deletedance.dodelete(anytime())
    report_query.MDR_Report_Query(anytime())

    print '抓取完成'

def crawler_anytime2(start, end):
    #
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login()
        print u"login Tag(anytime2):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(anytime2)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(1)

    deletedance.dodelete(anytime2(start, end))
    report_query.MDR_Report_Query(anytime2(start, end))