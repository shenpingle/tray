#-*- coding:utf-8 -*-
###########################################################################################
#  author: luu
#  info:（自动下载）对比国家MDR和平台MDR数据库轮询检查数据，如有差额，进行当日下载
#  Revision: 1.0
"""
        说明：对比国家MDR和平台MDR数据库轮询检查数据，如有差额，进行当日下载
        算法概述：
              定义如下名词：
                 国家MDR数据库       A
                 平台MDR数据库       B

              首先获取A、B两者年份数据差额 ，当出现数据差；再次获取并对比两者月份差额 ，当出现数据差；开始查询本月逐天数据，当出现数据差，开始下载当天数据，并写下日志记录。
"""
#2014-10-14重新修改过
#1.下载逻辑判断
###########################################################################################

import calendar
import mdrsql
import acdownload
from login2 import login
from utils import *
import codecs
import datetime

import time
ThisYear = time.strftime('%Y-%m-%d', time.localtime(time.time()))[0:4]
ThisMonth = time.strftime('%Y-%m-%d', time.localtime(time.time()))[6:7]
Format = "%d-%d-%d:%d-%d-%d"

def RegulateMdrData(year, beginMonth, endMonth):
    '''
    校正mdr数据
    @year : 指定校正的年份
    @beginMonth : 指定开始校正的月分
    @endMonth : 指定结束校正的月份
    '''

    print u"正在login..."
    logincounter = 0
    loginOk = False
    while logincounter < 6 and not loginOk :
        loginOk = login()
        logincounter = logincounter + 1
        time.sleep(8)
    
    beginDay = datetime.date(int(year),int(beginMonth),1)
    while beginDay.month <= int(endMonth) and beginDay.year == int(year) :
        acdownload.mdr_data_regulate(beginDay.strftime("%Y-%m-%d"))
        beginDay = beginDay + datetime.timedelta(days=1)

    print u"核对结束"

if __name__ == '__main__':
    some = right2(2014, 6, 9)
    print some