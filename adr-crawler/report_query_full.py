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
import gather
from utils import *
from config import *
import codecs
import time
import os
from deletedance import dodelete
import mdrsql
import simplejson as json

def crawler_mdr_record_ids(_timedict):
    '''抓取mdr数据的所有ID'''
    
    #获取循环次数
    pageCount = gather.mdr_get_page_count_by_day(_timedict)
    MDR_query = []

    print u'有效数据页数：', pageCount

    for idx in range(0, pageCount):

        startPos = idx*100

        jim = {"funcID":"QUERY_DATA", "userID":78919, "operations":[{"actionName":"query", "operationDatas":[{"PROD_NAME_1540":"", "REG_NO_1540":"", "DEVICE_CLASS_ID_1540":"", "DEVICE_CLASS_NAME_1540":"", "REPORT_DATE_START":_timedict, "REPORT_DATE_END":_timedict, "REPORT_NUMBER_1540":"", "CREATE_DATE_START":"", "CREATE_DATE_END":"", "SUPERVISE_ORG_ID_1540":"","SUPERVISE_ORG_NAME_1540":"","MAN_NAME_1540":"","REPORT_UNIT_NAME_1540":"","PATIENT_NAME_1540":"","EVALUATE_DATE_START":"","EVALUATE_DATE_END":"","MANAGE_CATEGORY_1540":"","listid":"1540","start":startPos,"limit":100}]}]}

        #查询结果列表
        _searchdata = send_post_json_me(totalHome, jim)
        #
        _data = json.loads(_searchdata)
        
        #当前页记录数
        currentPageRecordCount = _data['ResponseMessage']['operations'][0]['count']
        print u'第 %s 页共有记录数: %s' % (idx+1,currentPageRecordCount)

        for idx in range(0, currentPageRecordCount):
            #病人姓名
            _p_name = _data['ResponseMessage']['operations'][0]['operationDatas'][idx]['es'][26]['v']
            p_name = data_check_type(_p_name)
            #报告id
            _report_id = _data['ResponseMessage']['operations'][0]['operationDatas'][idx]['es'][4]['v']
            report_id = data_check_type(_report_id)

            #报告单位名称
            _r_u_name = _data['ResponseMessage']['operations'][0]['operationDatas'][idx]['es'][27]['v']
            r_u_name = data_check_type(_r_u_name)
            #事件后果
            _event_name = _data['ResponseMessage']['operations'][0]['operationDatas'][idx]['es'][12]['v']
            event_name = data_check_type(_event_name)
            #产品名称
            _pro_name = _data['ResponseMessage']['operations'][0]['operationDatas'][idx]['es'][20]['v']
            pro_name = data_check_type(_pro_name)
            #报告日期
            _sned_date = _data['ResponseMessage']['operations'][0]['operationDatas'][idx]['es'][2]['v']
            sned_date = data_check_type(_sned_date)
            #接受日期
            _create_date = _data['ResponseMessage']['operations'][0]['operationDatas'][idx]['es'][6]['v']
            create_date = data_check_type(_create_date)
            #评价状态
            _info = _data['ResponseMessage']['operations'][0]['operationDatas'][idx]['es'][16]['v']
            info = data_check_type(_info)
            #厂家名称
            _factory_name = _data['ResponseMessage']['operations'][0]['operationDatas'][idx]['es'][7]['v']
            factory_name = data_check_type(_factory_name)
            #view对象
            _fd_obj = _data['ResponseMessage']['operations'][0]['operationDatas'][idx]['es'][14]['v']
            fd_obj = data_check_type(_fd_obj)
            #退回状态
            _bs = _data['ResponseMessage']['operations'][0]['operationDatas'][idx]['es'][21]['v']
            _bs_ = data_check_type(_bs)
            #补充材料
            _bccl = _data['ResponseMessage']['operations'][0]['operationDatas'][idx]['es'][24]['v']
            bccl = data_check_type(_bccl)

            obj_id = unicode_to_str(fd_obj)
            obj_name = unicode_to_str(r_u_name)
            filters = [obj_id, obj_name,  info, _bs_, create_date, bccl, report_id, sned_date]

            insert_sql = (
                "insert into mdr_fullidlist (ViewID,ReportUnitName,ValueState,BackState,ReceiveDate,AddSource,ReportID,SendDate) "
                "value(%s,%s,%s,%s,%s,%s,%s,%s)"
            )
            mdrsql.mdr_insert_alone(insert_sql, filters)

        time.sleep(0.001)

    return True