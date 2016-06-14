#-*- coding:utf-8 -*-
import datetime
import mdrsql
import report_query_full
import utils
import login2
import time
import mdr_parse
import urllib

import sys
sys.setdefaultencoding('utf-8')

def mdr_update_appraise(date):
    '''
    更新指定日期的再评价数据
    '''
    print u'开始更新%s的不良事件评价数据！' % date
    
    #删除指定日期的id列表
    delete_sql = "delete from mdr_fullidlist where SendDate='%s'" % date
    mdrsql.mdr_delete_alone(delete_sql)

    #抓取当天所有有效记录的ID
    report_query_full.crawler_mdr_record_ids(date)

    #查询需要下载的记录
    query_sql = "select * from mdr_fullidlist where sendDate='%s' and BackState<>'%s' " % (date,u'已退回')
    download_rows = mdrsql.mdr_dict_query(query_sql)

    for qrow in download_rows:    
            
        viewId          = qrow["ViewID"]
        ReportUnitName  = qrow["ReportUnitName"]
        backState       = qrow["BackState"]
        AddSource       = qrow["AddSource"]
        ReportDate      = qrow["SendDate"]
        ReportID        = qrow["ReportID"]
        ValueState      = qrow["ValueState"]

        if not ValueState:
            print u'%s 未评价！' % ReportID
            continue

        mdr_Home_1 = 'http://www.adrs.org.cn/MDR/scripts/mdr/smdr/smdReportView.jsp'
        querydata_1 = {
                "action"        :   "update",
                "FD_OBJECTID"   :   viewId,
                "UNIT_NAME"     :   ReportUnitName,
                "start"         :   1,
                "limit"         :   10
            }
        smdrReportViewHtml = utils.send_post(mdr_Home_1, urllib.urlencode( querydata_1))
        if not backState and  smdrReportViewHtml:
            #获取关联性评价信息
            utils.mdr_get_smd_appraise(smdrReportViewHtml, ReportID, viewId, ReportUnitName,ReportDate)
            mdr_data = mdr_parse.mdr_get_report_data(viewId,ReportID,ReportDate)    
            if mdr_data and "reporter" in mdr_data:
                utils.get_smd_report(smdrReportViewHtml, ReportID, viewId,ReportUnitName,mdr_data["reporter"],mdr_data["reporter_class"],ReportDate)

    print u"%s的不良事件评价更新完成！" % (date)

def crawler_appraise(year,beginMonth, endMonth):
    
    logincounter = 0
    loginOk = False
    while logincounter < 6 and not loginOk :
        loginOk = login2.login()
        logincounter = logincounter + 1
        time.sleep(8)

    beginDay = datetime.date(int(year),int(beginMonth),1)
    while beginDay.month <= int(endMonth) and beginDay.year == int(year) :
        mdr_update_appraise(beginDay.strftime("%Y-%m-%d"))
        beginDay = beginDay + datetime.timedelta(days=1)

if __name__ == "__main__":
    logincounter = 0
    loginOk = False
    while logincounter < 6 and not loginOk :
        loginOk = login2.login()
        logincounter = logincounter + 1
        time.sleep(8)

    mdr_update_appraise('2016-01-14')