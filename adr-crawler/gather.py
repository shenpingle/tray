#-*- coding:utf-8 -*-
###########################################################################################
#  author: luu
#  info:获取报告总数
#  Revision: 1.0
"""
    功能说明：   获取在所提供查询时间段参数内的报告条数，用于主循环函数中
    逻辑：       首先，调用登录函数，当登录成功后，取得所提供查询时间段字典参数的值，
                 向http://www.adrs.org.cn/MDR/scripts/mdr/smdr/queryCondition.jsp发送post请求，获得站点请求后，返回输出
    输入参数：   所提供查询时间段字典参数
    输出参数：   报告条数
"""
###########################################################################################
from utils import *
import codecs
from mdrtime import *
import datetime

def mdr_get_page_count(_timedict):

    '''查询符合指定条件的总记录页数'''

    t = _timedict
    t_start = t['beginTime']
    t_end = t['endTime']

    #首先获取记录条数总记录
    form_query_data = 'params={"funcID":"0000000","userID":608575,"operations":[{"actionName":"query","operationDatas":[{"PROD_NAME_1540":"","REG_NO_1540":"","DEVICE_CLASS_ID_1540":"","DEVICE_CLASS_NAME_1540":"","REPORT_DATE_START":"%s","REPORT_DATE_END":"%s","REPORT_NUMBER_1540":"","CREATE_DATE_START":"","CREATE_DATE_END":"","SUPERVISE_ORG_ID_1540":"","SUPERVISE_ORG_NAME_1540":"","MAN_NAME_1540":"","REPORT_UNIT_NAME_1540":"","PATIENT_NAME_1540":"","EVALUATE_DATE_START":"","EVALUATE_DATE_END":"","MANAGE_CATEGORY_1540":"","listid":"1540","start":0,"limit":100}]}]}' % (t_start,t_end)
    _idcdata = send_post(totalHome,form_query_data)
    usa = 0
    try:
        _data = json.loads(_idcdata)
        usa = _data['ResponseMessage']['operations'][0]['pageTotal']
    except (IndexError, KeyError, ValueError), exception:
        print exception
    
    total_usa = int(usa-1)
    total = (total_usa/100)+1

    return total

def mdr_get_page_count_by_day(_timedict):
    '''
    获取@_timedict当天的数据记录页数 
    
    '''

    endTime = datetime.datetime.strptime(_timedict,"%Y-%m-%d") + datetime.timedelta(days=1)

    queryt_params = {
            "beginTime" : _timedict,
            "endTime"   : endTime.strftime("%Y-%m-%d")
        }
    return mdr_get_page_count(queryt_params)