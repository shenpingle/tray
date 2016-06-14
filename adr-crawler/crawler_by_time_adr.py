#-*- coding:utf8 -*-
#1.2014-10-14,修改登录函数的调用
#2.2014-10-14,修改下载函数的调用
#3.2014-10-14,import common

import logging
import database_adr
import adr_adr
import login2
import login_new_adr
from common import *

LOG_FILENAME = "error_" + datetime.datetime.today().strftime("%Y_%m_%d") + ".log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def delete_by_bianma(bianma):
    try:
        conn = database_adr.getConnection()
        cur = conn.cursor()
        cur.execute("delete from business_gather where bianma='%s'" % (bianma))
        cur.execute("delete from attachments where bianma='%s'" % (bianma))
        cur.execute("delete from olapclinic where bianma='%s'" % (bianma))
        cur.execute("delete from olapleechdom where bianma='%s'" % (bianma))
        cur.execute("delete from olappass where bianma='%s'" % (bianma))
        
        cur.close()
        conn.commit()
        conn.close()
    except Exception as err :
        logging.info("delete data by bianma(:%s) failture!" % bianma)
        return False
        
    return True
        


def crawler_by_time(username, password,start_date,end_date):
    #开始抓取指定日期区间数据
    logging.info("开始抓取指定日期区间数据！")
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
    
    page_idx = 1
    step = 100

    end_time = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    start_time = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    
    start_time = start_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    end_time =  end_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    logging.info("start time:%s \t end time:%s" % (start_time, end_time))
    start_pos = 0
    for res_page  in login_new_adr.get_page_list(filters,start_pos, step):
        print "page: ",page_idx
        page_idx += 1
        
        business_idx = 1
        for qrow in res_page:  # 一次一个案例
            print "business idx: %s of %s " % (business_idx , step)
            business_idx += 1
            
            try:
                delete_by_bianma(qrow["report_id2"])   		#删除成功则添加
                adr_adr.import_from_html(qrow)
            except Exception as err :
                print err
                
   
if __name__ == "__main__":
    #username="adr-liuxinyi"
    #password="96E79218965EB72C92A549DD5A330112"
    username = "adr-hnadr06"
    password = "FE008700F25CB28940CA8ED91B23B354"
