#-*- coding:utf-8 -*-
#1,2014-10-14,删除多余的import
import logging
import adr_adr
import login_new_adr
import login2
from common import *

LOG_FILENAME = "error_" + datetime.datetime.today().strftime("%Y_%m_%d") + ".log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

def crawler_last_year(username, password):
    #抓取上一年度的

    logging.info(u"开始抓取上一年度数据！")
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login2.login()
        print u"login Tag(last_year):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(last_year)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)
    
    page_idx = 1
    step = 100
    
    year = datetime.datetime.today().year - 1
    last_year_start = datetime.date(year,1,1)
    last_year_end = datetime.date(year,12,31)
    start_time = last_year_start.strftime("%a %b %d %Y 00:00:00 GMT+0800 ")
    end_time =  last_year_end.strftime("%a %b %d %Y 00:00:00 GMT+0800 ")
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    logging.info(u"start time:%s \t end time:%s" % (start_time, end_time))
    start_pos = 0
    for res_page  in login_new_adr.get_page_list(filters,start_pos, step):# 一次一页，一页10条
        print "page: ",page_idx
        page_idx += 1
        
        business_idx = 1
        for qrow in res_page:  # 一次一个案例
            print u"business idx: %s of %s " % (business_idx , step)
            business_idx += 1
            
            adr_adr.import_from_html(qrow)
            
def crawler_first_half_year(username, password):
    #抓取上半年度的

    logging.info(u"开始抓取上半年度数据！")
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login2.login()
        print u"login Tag(first_half_year):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(first_half_year)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)
    
    page_idx = 1
    step = 100
    
    year = datetime.datetime.today().year 
    last_year_start = datetime.date(year,1,1)
    last_year_end = datetime.date(year,6,30)
    start_time = last_year_start.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    end_time =  last_year_end.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    logging.info(u"start time:%s \t end time:%s" % (start_time, end_time))
    start_pos = 0
    for res_page  in login_new_adr.get_page_list(filters,start_pos, step):
        print u"page: ",page_idx
        page_idx += 1
        
        business_idx = 1
        for qrow in res_page:
            print u"business idx: %s of %s " % (business_idx , step)
            business_idx += 1
            
            adr_adr.import_from_html(qrow)
            
def crawler_second_half_year(username, password):
    #抓取下半年度的

    logging.info(u"开始抓取下半年度数据！")
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login2.login()
        print u"login Tag(second_half_year):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(second_half_year)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)
    
    page_idx = 1
    step = 100
    
    year = datetime.datetime.today().year 
    start_time = datetime.date(year,7,1)
    end_time = datetime.date(year,12,31)
    start_time = start_time.strftime("%a %b %d %Y 00:00:00 GMT+0800" )
    end_time =  end_time.strftime("%a %b %d %Y 00:00:00 GMT+0800" )
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    logging.info(u"start time:%s \t end time:%s" % (start_time, end_time))
    start_pos = 0
    for res_page  in login_new_adr.get_page_list(filters,start_pos, step):# 一次一页，一页10条
        print u"page: ",page_idx
        page_idx += 1
        
        business_idx = 1
        for qrow in res_page:  # 一次一个案例
            print u"business idx: %s of %s " % (business_idx , step)
            business_idx += 1
            
            adr_adr.import_from_html(qrow)
            
def crawler_current_week(username, password):
    #抓取本周的

    logging.info(u"开始抓取本周数据！")
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login2.login()
        print u"login Tag(current_week):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(current_week)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)
    
    page_idx = 1
    step = 100
    
    end_time = datetime.datetime.today()
    delta = datetime.timedelta(days=end_time.weekday())
    start_time = end_time - delta 
    
    start_time = start_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    end_time =  end_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    logging.info(u"start time:%s \t end time:%s" % (start_time, end_time))
    start_pos = 0
    for res_page  in login_new_adr.get_page_list(filters,start_pos, step):# 一次一页，一页10条
        print u"page: ",page_idx
        page_idx += 1
        
        business_idx = 1
        for qrow in res_page:  # 一次一个案例
            print u"business idx: %s of %s " % (business_idx , step)
            business_idx += 1
            
            adr_adr.import_from_html(qrow)
            
def crawler_last_week(username, password):
    #抓取上周的

    logging.info(u"开始抓取上周数据！")
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login2.login()
        print u"login Tag(last_week):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(last_week)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)
    
    page_idx = 1
    step = 100
    
    end_time = datetime.datetime.today()
    delta_day = end_time.weekday() + 7
    delta = datetime.timedelta(days= delta_day )
    start_time = end_time - delta
    end_time = start_time + datetime.timedelta(days=6)
    
    start_time = start_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    end_time =  end_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    logging.info(u"start time:%s \t end time:%s" % (start_time, end_time))
    start_pos = 0
    for res_page in login_new_adr.get_page_list(filters,start_pos, step):# 一次一页，一页10条
        print u"page: ",page_idx
        page_idx += 1
        
        business_idx = 1
        for qrow in res_page:  # 一次一个案例
            print u"business idx: %s of %s " % (business_idx , step)
            business_idx += 1
            
            adr_adr.import_from_html(qrow)
            
def crawler_last_month(username, password):
    #抓取上月的
    logging.info(u"开始抓取上月数据！")
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login2.login()
        print u"login Tag(last_month):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(last_month)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)
    
    page_idx = 1
    step = 100
    
    cur_time = datetime.datetime.today()
    year = cur_time.year
    month = cur_time.month - 1
    if month == 0 :
       month = 12
       year -= 1

    start_time = datetime.datetime(year, month, 1)
    end_time = datetime.datetime( cur_time.year, cur_time.month, 1 ) - datetime.timedelta(days=1)

    
    start_time = start_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    end_time =  end_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    logging.info(u"start time:%s \t end time:%s" % (start_time, end_time))
    start_pos = 0
    for res_page  in login_new_adr.get_page_list(filters,start_pos, step):# 一次一页，一页10条
        print u"page: ",page_idx
        page_idx += 1
        
        business_idx = 1
        for qrow in res_page:  # 一次一个案例
            print u"business idx: %s of %s " % (business_idx , step)
            business_idx += 1
            
            adr_adr.import_from_html(qrow)


def crawler_today():
    #
    logging.info(u"开始抓取今天数据！")
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login2.login()
        print u"login Tag(ADR Today):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            #
            print u"6次login(auto today)失败，重新尝试此操作"
            print u"本次任务已经结束"
            return
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)

    page_idx = 1
    step = 100
    start_time = datetime.datetime.today()
    end_time = start_time + datetime.timedelta(days=1)
    start_time = start_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    end_time =  end_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    logging.info(u"start time:%s \t end time:%s" % (start_time, end_time))
    start_pos = 0
    for res_page  in login_new_adr.get_page_list(filters,start_pos, step):
        page_idx += 1

        business_idx = 1
        for qrow in res_page:
            print "business idx: %s of %s " % (business_idx , step)
            business_idx += 1
            adr_adr.import_from_html(qrow)

def crawler_today2(sometime):
    #
    page_idx = 1
    step = 100
    end_time = datetime.datetime.strptime(sometime, "%Y-%m-%d")
    start_time = datetime.datetime.strptime(sometime, "%Y-%m-%d")
    start_time = start_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
    end_time =  end_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")

    print u"start_time,end_time:", start_time, end_time
    filters = {
        "beginTime":    start_time,
        "endTime":      end_time
    }
    logging.info(u"start time:%s \t end time:%s" % (start_time, end_time))
    start_pos = 0

    for res_page  in login_new_adr.get_page_list(filters,start_pos, step):
        page_idx += 1
        business_idx = 1
        print u'res_page:',res_page
        for qrow in res_page:
            print "business idx: %s of %s " % (business_idx , step)
            business_idx += 1
            adr_adr.import_from_html(qrow)

if __name__ == "__main__":
    username = "adr-hnadr06"
    password = "FE008700F25CB28940CA8ED91B23B354"