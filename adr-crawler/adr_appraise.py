#-*- coding:utf-8 -*-
import datetime
import mdrsql
import urllib
import adr_regulate
import adr_adr
import login_new_adr
import config
import re
import logging
import sys


def adr_update_appraise(date):
    '''
    更新指定日期的再评价数据
    '''
    print u'开始更新%s的不良事件评价数据！' % date
    
   #删除指定日期的id列表
    delete_sql = "delete from adr_full_id_list where date_format( report_date,'%Y-%m-%d')='" + date + "'"
    mdrsql.mdr_delete_alone(delete_sql)

    #抓取当天所有有效记录的ID
    adr_regulate.crawler_adr_fullidlist(date)

    #查询需要下载的记录
    query_sql = "select * from adr_full_id_list where date_format( report_date,'%Y-%m-%d')='" + date + "'"
    download_rows = mdrsql.mdr_dict_query(query_sql)

    for qrow in download_rows:

        qrow["report_date"] = qrow["report_date"].strftime("%Y-%m-%d %H:%M:%S")
        show_id = qrow["report_id"]

        show_url = adr_adr.REPORT_SHOW_URL % (show_id)

        body = login_new_adr.send_adr_url(show_url)

        appraise_data = adr_adr.get_appraises(show_id, body)
        sql = "update business_gather set "
        update_to_table('business_gather',appraise_data,"show_id='%s'" % show_id)

def _check_date_value(row):
    re_date = re.compile(r'\d{4}-\d{2}-\d{2}', re.U)
    keys = ["happendate", "reportdate", "acceptdate", "statereportdate", "provincereportdate", 
        "trackdate", "birthday", "deathdate", "personappraisedate", "unitappraisedate",
        "basicappraisedate", "municipalappraisedate", "provinceappraisedate", "stateappraisedate" ]
    for key in keys:
        if key in row :
            match = re_date.match(row[key])
            if match :
                row[key] = match.group(0)
            else :
                del row[key]
    
    return row

  
def update_to_table(tabName,data,where):
    '''根据dict修改数据库记录'''
    
    conn = config.myconnect()
    
    data = _check_date_value(data)
    
    del_keys = data.keys()
    for k in del_keys:
        if k.startswith("_"): #下划线打头的字段，不入库
            del data[k]
    
    sql = ""
    try:
        cur = conn.cursor()        
        keys = data.keys()        
        update_sets = []

        for k in keys:
            if isinstance(data[k],str) :
                data[k] = data[k].decode("utf8")

            update_sets.append(u"%s='%s'" %(k, data[k].replace(u"'",u"\’").strip()) )
        
        
        sql = u"update %s set %s where %s " % (tabName, u','.join(update_sets), where) 

        cur.execute(sql)
        cur.close()
    except Exception as err :
        print err
        
    conn.commit()
    conn.close()    
    
    

def crawler_appraise(year,beginMonth, endMonth):
    
    import login2

    logincounter = 0
    loginOk = False
    while logincounter < 6 and not loginOk :
        loginOk = login2.login()
        logincounter = logincounter + 1

    beginDay = datetime.date(int(year),int(beginMonth),1)
    while beginDay.month <= int(endMonth) and beginDay.year == int(year) :
        adr_update_appraise(beginDay.strftime("%Y-%m-%d"))
        beginDay = beginDay + datetime.timedelta(days=1)

if __name__ == "__main__":
    logincounter = 0
    loginOk = False
    import login2
    while logincounter < 6 and not loginOk :
        loginOk = login2.login()
        logincounter = logincounter + 1

    adr_update_appraise('2016-01-14')