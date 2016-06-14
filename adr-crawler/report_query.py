#-*- coding:utf-8 -*-

###########################################################################################
#  author: luu
#  info: 获取查询信息，除icd、伤害、故障和评价信息
#  Revision: 1.0
###########################################################################################
"""
    功能说明：   获取查询信息，包含以下数据：
                    #患者姓名
                    #报告编码
                    #报告单位
                    #时间后果
                    #产品名称
                    #报告日期
                    #系统接受日期
                    #评价状态
                    #补充材料
                    #退回状态
                    用于主循环函数中
    逻辑：       首先，取得所提供查询时间段字典参数的值，调用gather_report_total获得查询页数，进入循环遍历整个查询页面
                 向http://www.adrs.org.cn/MDR/scripts/mdr/smdr/queryCondition.jsp发送post请求，获得站点请求后，返回输出
    输入参数：   所提供查询时间段字典参数
    输出参数：        返回一个list对象，包含如下结构的字典：
                        filters = {
                                    "obj_id":    obj_id,
                                    "r_u_name":      obj_name,
                                    "info":     info,
                                    "bs":       _bs_,
                                    "create_date":      create_date,
                                    "bccl":     bccl,
                                    "report_id":     report_id,
                                    "sned_date": sned_date
                                }，
                        view对象、报告单位名称、评价状态、退回状态、接受日期 、补充材料、报告编码、报告日期
"""
from gather import mdr_get_page_count
from utils import *
from config import *
import codecs
import time
import os
from deletedance import dodelete
import simplejson as json
import mdr_parse
import login2

def MDR_Report_Query(_timedict):
    #
    t = _timedict
    t_start = t['beginTime']
    t_end = t['endTime']

    #获取总页数
    pageTotal = mdr_get_page_count(_timedict)

    print u'数据总页数：', pageTotal

    for pageIdx in range(0, pageTotal):
        print u'抓取第%s页数据！' % pageIdx
        records = mdr_get_records_by_page_index(pageIdx, t_start, t_end)
        for rec in records:
             mdr_parse.mdr_import_report(rec)

    print u'本次抓取任务完成！'

def mdr_get_records_by_page_index(pageIdx, t_start, t_end ):
    '''获取指定页的记录信息'''

    startPos = pageIdx*100 #i是页数， startPos为本面首记录
            
    jim = {"funcID":"QUERY_DATA", "userID":78919, "operations":[{"actionName":"query", "operationDatas":[{"PROD_NAME_1540":"", "REG_NO_1540":"", "DEVICE_CLASS_ID_1540":"", "DEVICE_CLASS_NAME_1540":"", "REPORT_DATE_START":t_start, "REPORT_DATE_END":t_end, "REPORT_NUMBER_1540":"", "CREATE_DATE_START":"", "CREATE_DATE_END":"", "SUPERVISE_ORG_ID_1540":"","SUPERVISE_ORG_NAME_1540":"","MAN_NAME_1540":"","REPORT_UNIT_NAME_1540":"","PATIENT_NAME_1540":"","EVALUATE_DATE_START":"","EVALUATE_DATE_END":"","MANAGE_CATEGORY_1540":"","listid":"1540","start":startPos,"limit":100}]}]}

    #查询当前页记录数
    _searchdata = send_post_json_me(totalHome, jim)
            
    _data = json.loads(_searchdata)

    #本次查询结果记录数
    searchdataid = _data['ResponseMessage']['operations'][0]['count']
    records = [] 
    for i in range(0, searchdataid):
        #报告id
        _report_id = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][4]['v']

        #报告单位名称
        _r_u_name = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][27]['v']

        #报告日期
        _sned_date = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][2]['v']

        #接受日期
        _create_date = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][6]['v']

        #评价状态
        _info = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][16]['v']

        #view对象
        _fd_obj = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][14]['v']

        #退回状态
        _bs = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][21]['v']

        #补充材料
        _bccl = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][24]['v']

        filters = {
            "ViewID":       unicode_to_str(data_check_type(_fd_obj)),
            "ReportUnitName":     unicode_to_str( data_check_type(_r_u_name)),
            "ValueState":         data_check_type(_info),
            "BackState":           data_check_type(_bs),
            "ReceiveDate":  data_check_type(_create_date),
            "AddSource":         data_check_type(_bccl),
            "ReportID":    data_check_type(_report_id),
            "SendDate":    data_check_type(_sned_date),
            "CreateDate":    data_check_type(_create_date)
        }
        yield filters