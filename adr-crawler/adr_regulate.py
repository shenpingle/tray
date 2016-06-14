#-*- coding:utf-8 -*-

import datetime
import mdrsql
import deletedance
import login2
import time
import login_new_adr
import config
import adr_adr
import utils
import urllib
import simplejson as json

def crawler_adr_fullidlist(sometime):
    #
    page_idx = 1
    step = 100
    end_time = datetime.datetime.strptime(sometime, "%Y-%m-%d")
    start_time = datetime.datetime.strptime(sometime, "%Y-%m-%d")
    start_time = start_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    end_time =  end_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")

    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    start_pos = 0

    for res_page  in login_new_adr.get_page_list(filters,start_pos, step):
        page_idx += 1
        business_idx = 1
        for qrow in res_page:
            business_idx += 1

            show_id = qrow["report_id"]
            bianma = qrow["report_id2"]                         #编码
            fungible_name = qrow["personal_his"]                #代报单位
            report_unit_name = qrow["report_unit_name"]         #报告单位
            medic_list = qrow["general_name"]                   #通用名称，用药集合
            adr_list = qrow["adr_name"]                         #不良反应名称
            data_source = qrow["data_source"]                   #个例来源
            report_type = qrow["new_flag"]                      #报告类型
            StateReportDate = qrow["report_date"]               #国家中心接收时间

            insert_sql = u'insert into adr_full_id_list(report_id,report_id2,personal_his,report_unit_name,general_name,adr_name,data_source,new_flag,report_date)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mdrsql.mdr_insert_alone(insert_sql,[show_id,bianma,fungible_name,report_unit_name,medic_list,adr_list,data_source,report_type,StateReportDate]) 

def clear_invalid_data(strDate):
    '''
    清除某天无效的记录
    '''
    beginDate = datetime.datetime.strptime(strDate,"%Y-%m-%d")
    endDate = beginDate + datetime.timedelta(days=180)
    pageSize = 100
    pageStart = 0
    processCnt = 0
    isComplete = False
    deleted_data_query_url = 'http://www.adrs.org.cn/ADR/ep/alreadyReport/AlreadyReportService/queryDeleteReport/'
    while not isComplete: 
        query_data = '{"funcID":"0000000","userID":608575,"operations":[{"actionName":"query","operationDatas":[{"ENTRY_START_DATE_2200":"%s","ENTRY_END_DATE_2200":"%s","DELETE_START_DATE_2226":"%s","DELETE_END_DATE_2226":"%s","REPORT_ID_2200":"","GENERAL_NAME_2200":"","ADR_RESULT_2660":"","PATIENT_NAME_2200":"","FACTORY_NAME_2200":"","REPORTDELETE_2200":"1","REPORTRepeat_2200":"1","listid":"2433","start":%s,"limit":%s}]}]}' % (strDate,strDate,strDate, endDate.strftime("%Y-%m-%d"),pageStart, pageSize)
        #query_data = {
	       # "funcID": "0000000",
	       # "userID": 608575,
	       # "operations": [{
		      #  "actionName": "query",
		      #  "operationDatas": [{
			     #   "ENTRY_START_DATE_2200":strDate,
			     #   "ENTRY_END_DATE_2200": endDate.strftime("%Y-%m-%d"),
			     #   "DELETE_START_DATE_2226": strDate,
			     #   "DELETE_END_DATE_2226": endDate.strftime("%Y-%m-%d"),
			     #   "REPORT_ID_2200": "",
			     #   "GENERAL_NAME_2200": "",
			     #   "ADR_RESULT_2660": "",
			     #   "PATIENT_NAME_2200": "",
			     #   "FACTORY_NAME_2200": "",
			     #   "REPORTDELETE_2200": "1",
			     #   "REPORTRepeat_2200": "1",
			     #   "listid": "2433",
			     #   "start": pageStart,
			     #   "limit": pageSize
		      #  }]
	       # }]
        #}
        strResponse = utils.mdr_send_post(deleted_data_query_url, query_data,None,None,None)
        jsonData = None
        try:
            jsonData = json.loads(strResponse)
        except Exception,err:
            print u'获取%s的删除数据失败！' % strDate
            return

        pageTotal = jsonData["ResponseMessage"]["operations"][0]["pageTotal"]
        currTotal = jsonData["ResponseMessage"]["operations"][0]["count"]
        if pageTotal <= 0:
            print u'date: %s 没有删除的数据' % strDate
            return

        if currTotal < pageSize :
            isComplete = True #如果当前返回结果小于pageSize ， 证明是最后一页

        datas = jsonData["ResponseMessage"]["operations"][0]["operationDatas"]
        for rowData in datas:
            showid = rowData["es"][3]["v"]
            bianma = rowData["es"][12]["v"]
            reason = rowData["es"][8]["v"]
            report_date = rowData["es"][1]["v"]
            deleted_date= rowData["es"][2]["v"]
            row = [showid,bianma,reason,report_date,deleted_date]
            mdrsql.mdr_insert_alone("replace into adr_deleted_gather(show_id,bianma,reason,report_date,deleted_date)values(%s,%s,%s,%s,%s)",row)

    recordCnt = 0
    myconn = config.myconnect()
    mycu = myconn.cursor()
    #在主表中删除标记为己退回的报告
    mycu.execute(u"delete from business_gather where bianma in(select bianma from adr_deleted_gather where report_date like '%s%s')" % (strDate, '%'))
    recordCnt = mycu.rowcount 
    myconn.commit()

    print u'%s 无效记录清除完成！共清除%s条记录！' % (strDate, recordCnt)


# 以下2016.05.31新增
# 详情查看文档DX-1000003
# 功能说明：对比一天的临时表跟主表的数量，如果有主表多，就写入adr_business_gather_disappear表里面
def check_disappear_data(date):

    today = datetime.date.today()
    # 先查询到主表多于的数量
    sql = "select bianma from business_gather where StateReportDate='%s' and " \
          "bianma not in(select report_id2 from adr_full_id_list where report_date like '%s%s')" % (date, date, '%')
    bianma_list = mdrsql.mdr_select(sql)
    all_data = []
    delete_data = []
    move_data = []
    for i in bianma_list:
        all_data.append(i[0])
    # 把多于的报表分为两种，一种是已退回列表查询到的需要删除的报表，还有一种是已经消失的需要移动的报表
    for i in all_data:
        sql = "select bianma from adr_deleted_gather where bianma='%s'" % i
        bianma_list = mdrsql.mdr_select(sql)
        if len(bianma_list) > 0:
            delete_data.append(bianma_list[0])
        else:
            move_data.append(i)

    # 把两种报表写到两个列表以后，进行数据库处理
    myconn = config.myconnect()
    mycu = myconn.cursor()
    num = 0
    for i in delete_data:
        mycu.execute("delete from business_gather where bianma='%s'" % i)
        myconn.commit()
    print u'%s 退回报表删除完成！共删除%s条报表！' % (date, num)
    num = 0
    for i in move_data:
        sql = "select bianma,reportunitname,reportdate,StateReportDate " \
              "from business_gather where bianma='%s'" % i
        diff_a = mdrsql.mdr_select(sql)
        sql = "INSERT into adr_business_gather_disappear(bianma,reportunitname,reportdate,StateReportDate," \
              "FoundTime) values('%s','%s','%s','%s','%s')" \
              % (diff_a[0][0], diff_a[0][1], diff_a[0][2], diff_a[0][3], today)
        mycu.execute(sql)
        myconn.commit()
        mycu.execute("delete from business_gather where bianma='%s'" % i)
        myconn.commit()
        num += 1
    print u'%s 消失报表移动完成！共移动%s条记录！' %(date, num)


def adr_regulate_by_day(date):
    '''
    校正指定一天的adr数据
    '''
    print u'开始校正%s的数据！' % date
    
    #删除指定日期的id列表
    delete_sql = "delete from adr_full_id_list where date_format( report_date,'%Y-%m-%d')='" + date + "'"
    mdrsql.mdr_delete_alone(delete_sql)

    #抓取当天所有有效记录的ID
    crawler_adr_fullidlist(date)

    #查询需要下载的记录
    query_sql = "select * from adr_full_id_list where date_format( report_date,'%Y-%m-%d')='" + date + "' and report_id2 not in(select bianma from business_gather where StateReportDate='" + date + "')"
    download_rows = mdrsql.mdr_dict_query(query_sql)

    for qrow in download_rows:
        qrow["report_date"] = qrow["report_date"].strftime("%Y-%m-%d %H:%M:%S")
        adr_adr.import_from_html(qrow)

    #清除当天已经失效的记录
    clear_invalid_data(date)

    # 以下2016.05.31新增
    # 详情查看文档DX-1000003
    # 功能说明：对比一天的临时表跟主表的数量，如果有主表多，就写入adr_business_gather_disappear表里面
    check_disappear_data(date)

    print u"%s 的数据校正完成！新增数据%s条" % (date, len(download_rows))
    
def adr_regulate(year, beginMonth, endMonth):
    '''
    校正adr数据
    @year : 指定校正的年份
    @beginMonth : 指定开始校正的月分
    @endMonth : 指定结束校正的月份
    '''

    print u"正在login..."
    logincounter = 0
    loginOk = False
    while logincounter < 6 and not loginOk :
        loginOk = login2.login()
        logincounter = logincounter + 1
        time.sleep(8)
    
    beginDay = datetime.date(int(year),int(beginMonth),1)
    while beginDay.month <= int(endMonth) and beginDay.year == int(year) :
        adr_regulate_by_day(beginDay.strftime("%Y-%m-%d"))
        beginDay = beginDay + datetime.timedelta(days=1)

if __name__ == "__main__":
    #print login()
    adr_regulate(2015,1,1)