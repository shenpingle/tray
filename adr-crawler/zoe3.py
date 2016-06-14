#-*- coding:utf-8 -*-
###########################################################################################
#  author: luu
#  info:（自动下载）对比国家ADR和平台ADR数据库轮询检查数据，如有差额，进行当日下载
#  Revision: 1.0
"""
        说明：对比国家ADR和平台ADR数据库轮询检查数据，如有差额，进行当日下载
        算法概述：
              定义如下名词：
                 国家ADR数据库       A
                 平台ADR数据库       B

              首先获取A、B两者年份数据差额 ，当出现数据差；再次获取并对比两者月份差额 ，当出现数据差；开始查询本月逐天数据，当出现数据差，开始下载当天数据，并写下日志记录。
"""
#2014-10-14重新修改过
#1.下载逻辑判断
#2.药品本地查询字段改为StateReportDate，因为查询返回条数是依据StateReportDate查询的
###########################################################################################
import calendar
import mdrsql
from utils import *
import codecs

import main_adr
import time
import utils_adr
import login_new_adr
import login2

ThisYear = time.strftime('%Y-%m-%d', time.localtime(time.time()))[0:4]
ThisMonth = time.strftime('%Y-%m-%d', time.localtime(time.time()))[6:7]
Format = "%d-%d-%d:%d-%d-%d"

#返回某个月以每一周为元素的序列
def get_month_calendar(year, month):
    return calendar.monthcalendar(year, month)

#返回某个月当月所有天数，格式如下：2013-5-1
def daystomonth(year, month):
    Format = "%d-%d-%d"
    myday = get_month_calendar(year, month)
    mydays = []
    for x in myday:
        for y in x:
            if y == 0:
                pass
            else:
                const_time_all = Format % (year, month, y)
                mydays.append(const_time_all)
    return mydays

#获取A所有天数数据,yup
def harvestdaystomonthremote(sometime):
    #开始抓取指定日期报道条数
    itemid = []
    dayitemfilename = time.strftime("%Y-%m-%d") + '-remote_adr.txt'
    reportlog = codecs.open(dayitemfilename, 'a', 'utf-8')
    step = 10
    start_pos = 0
    batchId = 0

    for i in sometime:
        #
        print u"正在读取记录条数..."
        print u"i:", i

        end_time = datetime.datetime.strptime(i, "%Y-%m-%d")
        start_time = datetime.datetime.strptime(i, "%Y-%m-%d")
        start_time = start_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
        end_time = end_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
        filters = {
            "beginTime":    start_time,
            "endTime":      end_time
        }
        query_data = utils_adr.build_query(filters, start_pos, batchId, step)
        url = 'http://www.adrs.org.cn/ADR/dwr/call/plaincall/reportSearchService.dwrReportSearchCg.dwr'
        opt = {
        "c0-e1" : "number:" + str(start_pos),
        "c0-e2" : "number:" + str(step),
        "c0-e3" : "string:123_w_w_w_321_colon",
        "c0-e4": "string:123_w_w_w_321_comma",
        "c0-e5" : "string:",
        "c0-param0": "Object_Object:{start:reference:c0-e1, limit:reference:c0-e2, analyticsRuleColon:reference:c0-e3, analyticsRuleComma:reference:c0-e4, queryString:reference:c0-e5}"
        }
        out_data = login_new_adr.send_post3(url,query_data,opt_headers=opt)
        if out_data is None:
            #
            print u'返回空数据，重新操作本日数据'
            temp2 =0
        else:
            #print len(out_data)
            total = out_data.split(";")
            if len(total)!= 683:
                print u'返回数据长度不够，重新操作本日数据'
                temp2 = 0
            else:
                temp =total[681].split(",")[3].split(":")[1].strip(")")
                temp2 = temp.split("}")[0]
                print u"本日条数：",temp2
        itemid.append((i, str(temp2)))
        reportlog.write(i + '\t' + str(temp2) + '\n')
    reportlog.close()
    return itemid

#获取B所有天数数据,yup,现在可以使用
def harvestdaystomonthlocal(mydays):
    itemid = []

    dayitemfilename = time.strftime("%Y-%m-%d") + '-local_adr.txt'
    reportlog = codecs.open(dayitemfilename, 'a', 'utf-8')

    for i in mydays:
        #查询ADR数据库主表,business_gather,yup
        device_sql = (
            "SELECT count(*) FROM `business_gather` where StateReportDate='%s' " % (i)
        )
        rows_device = mdrsql.mdr_select(device_sql)
        localitem = rows_device[0][0]

        itemid.append((i, localitem))

        localitem_s = str(localitem)
        reportlog.write(i + '\t' + localitem_s + '\n')

    reportlog.close()
    return itemid

#获得所有日期参数列表,yup
def right2(year, month, m2):
    #
    year = int(year)
    month = int(month)
    m2 = int(m2)

    mydays = []
    for _m in range(month, m2+1):
        mop = daystomonth(year, _m)
        for i in mop:
            abc = i.split('-')
            Y = abc[0]
            if len(abc[1]) == 1:
                M = "0"+abc[1]
            else:
                M = abc[1]
            if len(abc[2]) == 1:
                D = "0"+abc[2]
            else:
                D = abc[2]
            Ddays = Y+'-'+M+'-'+D
            mydays.append(Ddays)

    return mydays

def main3(somed1, somed2, s3):
    #主逻辑部分
    print u"正在login..."
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login2.login()
        print u"login Tag(zoe3):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(main3)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return 
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)
    #
    print u"已经登录成功"
    #获得所有日期参数列表
    querydays = right2(int(somed1), int(somed2), int(s3))
    #读取B平台参数数据下记录报告总数
    days_local = harvestdaystomonthlocal(querydays)
    #辅助输出信息，供使用者阅读
    #{
    print u"本平台数据:",
    for il in days_local:
        print il
    print u"正在从国家站点读取数据........:",
    #}
    #读取A平台参数数据下记录报告总数
    days_remote = harvestdaystomonthremote(querydays)
    #辅助输出信息，供使用者阅读
    #{
    print u"国家站点数据:",
    for ir in days_remote:
        print ir
    #}
    #取得参数长度
    dl_len = len(days_local)

    for i in range(dl_len):
            #以A数据参数为基准参数
            someday = days_remote[i][0]
            date_remote = days_remote[i][1]
            date_local = days_local[i][1]
            date_check = int(date_remote)-int(date_local)

            if date_check ==0:
                print u"%s days Matched" % someday
            else:
                #
                print "Date_Check NOT MATCH:",date_check
                print u"%s days Not Match" % someday
                print u"匹配开始......."
                main_adr.crawler_today2(someday)
    print u"核对结束"


def myauto():
    username = "adr-hnadr06"
    password = "FE008700F25CB28940CA8ED91B23B354"
    some = right2(2014, 6, 9)
    harvestdaystomonthremote(username, password, some)

if __name__ == '__main__':
    #
    username = "adr-hnadr06"
    password = "FE008700F25CB28940CA8ED91B23B354"