#-*- coding:utf-8 -*-
###########################################################################################
#  author: luu
#  info:主要业务逻辑操作，获得报告数据，匹配、查重等处理后，写入相应业务数据库
#  Revision: 1.0
"""
    功能说明：  主要业务逻辑操作，获得报告数据，匹配、查重等处理后，写入相应业务数据库

"""
###########################################################################################

import utils
import datetime

import sys
import login2 
import report_query
import mdr_parse

reload(sys)
sys.setdefaultencoding('utf-8')


def mdr_report_full(_MDR_query_temp):

    for qrow in _MDR_query_temp:
        pass

    print u"本次下载任务已经结束"
    
def July_cal():
    
    start_time = datetime.datetime(2011,12,1).strftime('%Y-%m-%d')
    end_time = datetime.datetime(2011,12,31).strftime('%Y-%m-%d')
    
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    return filters

def mdr_profile():
    isLogin = False
    while not isLogin:
        isLogin = login2.login()   

    for qrow in utils.MDR_Report_Query(July_cal()):
        mdr_parse.mdr_import_report(qrow)