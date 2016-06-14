#-*- coding:utf-8 -*-
###########################################################################################
#  author: luu
#  info:封装传入某个具体日期下载报告函数,自动核查部分，接受单一时间参数下载报告数据（某一天）
#  Revision: 2013-12-10-1.0
"""
    功能说明：   封装传入某个具体日期下载报告函数,自动核查部分，接受单一时间参数下载报告数据（某一天）
    逻辑：       首先，查询mdr_fullidlist中ViewID,ReportUnitName,ValueState,BackState,ReceiveDate,
                AddSource,ReportID,SendDate几个字段，然后获得obj_id对象，依次发送post请求，完成报告下载
    输入参数：   某个具体日期，如2014-09-09
"""
###########################################################################################

from utils import *
import mdrsql
import report_query_full
import deletedance
import mdr_parse

def mdr_data_regulate(date):
    '''
    校正指定一天的mdr数据
    '''
    print u'开始校正%s的数据！' % date
    
    #删除指定日期的id列表
    delete_sql = "delete from mdr_fullidlist where SendDate='%s'" % date
    mdrsql.mdr_delete_alone(delete_sql)

    #抓取当天所有有效记录的ID
    report_query_full.crawler_mdr_record_ids(date)

    #清除当天已经失效的记录
    # 以下2016.05.25注释
    # 详情查看文档DX-1000001
    # deletedance.clear_invalid_data(date)


    #查询需要下载的记录
    # 以下2016.05.25注释
    # 详情查看文档DX-1000001
    # query_sql = "select * from mdr_fullidlist where sendDate='%s' and BackState<>'%s' and ReportID not in(select bianma from mdr_business_gather where ReportDate='%s')" % (date,u'已退回',date)

    query_sql = "select * from mdr_fullidlist where sendDate='%s' and " \
                "ReportID not in(select bianma from mdr_business_gather where ReportDate='%s')" % (date, date)
    download_rows = mdrsql.mdr_dict_query(query_sql)

    for qrow in download_rows:
        mdr_parse.mdr_import_report(qrow)

    # 以下2016.05.26新增
    # 详情查看文档DX-1000001
    # 功能说明：在临时表中查看已退回字段的编码，在主表中匹配编码标记为已退回
    # deletedance.check_back_data(date)

    # 以下2016.05.26新增
    # 详情查看文档DX-1000002
    # 功能说明：对比一天的临时表跟主表的数量，如果有主表多，就写入mdr_business_gather_disappear表里面
    deletedance.check_disappear_data(date)

    print u"%s的数据校正完成！新增数据%s条" % (date, len(download_rows))