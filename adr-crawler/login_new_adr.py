#-*- coding:utf-8 -*-
#
#  author:luu
#  说明:login函数
#  Revision: 1.0
#
from common import *
from utils import *

import calendar as cal
import time
Format = "%d-%d-%d:%d-%d-%d"
import random
import StringIO
import gzip
import logging
from HTMLParser import HTMLParser
import database_adr

import login2

def build_query(filter, startpos, batchid, step = 10):
    #北京：scriptSessionId：C528E9A53161B512369476338A1
    #河南：scriptSessionId：C528E9A53161B512369476338A1
    query_string = {}
    query_string["callCount"] =  "1"
    query_string["page" ] =    "/PF/page/frameWork.html"
    query_string["httpSessionId"] =    ""
    query_string["scriptSessionId"] =   "C528E9A53161B512369476338A1" + str(random.randint(10000000,1000000000))
    query_string["c0-scriptName"] =    "reportSearchService"
    query_string["c0-methodName"] =    "dwrReportSearchCg"
    query_string["c0-id"] =    "0"
    query_string["c0-e1"] =    "number:" + str(startpos)
    query_string["c0-e2"] =    "number:" + str(step)
    query_string["c0-e3"] =    "string:123_w_w_w_321_colon"
    query_string["c0-e4"] =    "string:123_w_w_w_321_comma"
    query_string["c0-e5" ] =    "string:"
    query_string["c0-param0"] =    "Object_Object:{start:reference:c0-e1, limit:reference:c0-e2, analyticsRuleColon:reference:c0-e3, analyticsRuleComma:reference:c0-e4, queryString:reference:c0-e5}"
    query_string["batchId"] =    str(batchid)
    
    if "beginTime" not in filter:
        filter["beginTime"] = "Sat Jan 01 00:00:00 GMT+0800 2011"
    if "endTime" not in filter:
        filter["endTime"] = "Sat Dec 31 00:00:00 GMT+0800 2011"
    
    map = {
        "dateType"      :   "5",
        "leechdomType"  :   "0,1"
    }
    map.update(filter)
    str_where = ""
    for k,v in map.iteritems():
        str_where += "123_w_w_w_321_comma" + k + "123_w_w_w_321_colon" + v
        
    str_filter = urllib.quote(str_where)
    
    query_string["c0-e5"] = query_string["c0-e5"]  + str_filter
    
    ret = []
    keys = ["callCount","page","httpSessionId","scriptSessionId","c0-scriptName","c0-methodName","c0-id","c0-e1","c0-e2","c0-e3","c0-e4","c0-e5","c0-param0","batchId"]
    for k in keys :
        v = query_string[k]
        ret.append(k + "=" + v)
        
    return "\n".join(ret)

def send_post3(url, postdata,opt_headers={}):
    #
    response_data = None
    try:
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection':  'keep-alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Referer':"http://www.adrs.org.cn/sso/login?service=http%3A%2F%2Fwww.adrs.org.cn%2FPF%2FcasAuthUser",
            'Host':'www.adrs.org.cn',
            'Content-Type':'text/plain; charset=UTF-8'
        }
        if opt_headers :
            #
            header.update(opt_headers)
            
        common_url = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(common_url, data=postdata, timeout=360)
        response_data = response.read()
        compressedstream = StringIO.StringIO(response_data)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        data = gzipper.read()
        gzipper.close()
        response_data = data
    except (urllib2.HTTPError, urllib2.URLError, socket.error), exception:
        pass

    return response_data

def send_adr_url(url):
    #
    response_data = None
    try:
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection':  'keep-alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Referer':"http://www.adrs.org.cn/PF/page/frameWork.html",
            'Host':'www.adrs.org.cn'
        }
            
        common_url = urllib2.Request(url)
        response = urllib2.urlopen(common_url, timeout=36)
        response_data = response.read()
    except (urllib2.HTTPError, urllib2.URLError, socket.error), exception:
        pass

    return response_data

def get_page_list(filter=None, startpos=0, step = 10):
    #分布获取数据
    batchId = 0
    
    opt = {
        "Referer" : 'http://www.adrs.org.cn/PF/page/frameWork.html',
        'Content-Type' : 'text/plain'
        }
        
    re_match = re.compile(r"\['([^']+)'\]=\"?([^;]*?)\"?;",re.U)
    
    p = HTMLParser()
    
    #上一年度
    last_year_query = {
        "beginTime" :    "Sat Jan 01 2011 00:00:00 GMT+0800",
        "endTime"   :    "Sat Dec 31 2011 00:00:00 GMT+0800"
    }
    if not filter :
        filter = last_year_query

    re_total = re.compile(r'totalSize:(\d+)',re.M|re.U)
    while True:
        query_data = build_query(filter,startpos,batchId, step)
        
        try:
            ret_body = send_post3('http://www.adrs.org.cn/ADR/dwr/call/plaincall/reportSearchService.dwrReportSearchCg.dwr', query_data)
            if ret_body is None:
                print u"ID查询数据返回空"
                return
            else:
                ret_body = ret_body.decode("unicode-escape")
                
                ret_body = p.unescape(ret_body).encode("utf8")
                lines = ret_body.split("\n")
                ret = []
                
                total_match = re_total.search(ret_body)
                total = 0
                if total_match :
                    total = total_match.group(1)
                logging.info("total: %s, batch:%s, step:%s" % (total, batchId, step))
                for line in lines:
                    matches = {}
                    for m in re_match.finditer(line) :
                        matches[m.group(1)] = m.group(2)
                        
                    if len(matches) > 0:
                        ret.append(matches)
                        
                if len(ret) > 0 :
                    yield ret 
                else :
                    print "done!!!"
                    return
                
        except Exception,err:
            print err
            
        startpos += step
        batchId += 1

def timetomonth3(y, m1, m2):
    print u"计算时间"
    month_a = []
    month_b = []
    for m in range(m1, m2+1):
        d = cal.monthrange(y, m)
        const_time_all = Format % (y, m, 1, y, m, d[1])
        const_time_temp = const_time_all.split(":")
        const_time_a = const_time_temp[0]
        const_time_b = const_time_temp[1]
        month_a.append(const_time_a)
        month_b.append(const_time_b)
    return [month_a, month_b]

def checklistauto(t1, t2, t3):
    #
    logincounter = 6
    while logincounter:
        print logincounter
        loginTag = login2.login()
        print u"login Tag (checklist):",loginTag
        if loginTag:
            break
        elif logincounter == 1:
            print u"6次login失败，重新尝试此操作"
            print u"本次任务已经结束"
            return 
        else:
            cookieManager.clear()
        logincounter = logincounter -1
        time.sleep(8)

    some = timetomonth3(int(t1), int(t2), int(t3))
    stack = some
    _stack = stack[0]
    stack_l = len(_stack)
    conn = database_adr.getConnection()
    cur = conn.cursor()
    for i in range(stack_l):
        #
        print u"正在读取记录条数..."
        out = _stack.pop()
        out1 = stack[1].pop()
        print out, out1
        const_time_o = out1.split("-")
        const_time_o_ = out.split("-")
        yaer = const_time_o_[0]
        month = const_time_o_[1]

        cur.execute("delete from mdr_checklist where CheckTag='Y' and Year=%s and Month=%s" % (yaer, month))
        conn.commit()

        end_time = datetime.datetime.strptime(out1, "%Y-%m-%d")
        start_time = datetime.datetime.strptime(out, "%Y-%m-%d")

        start_time = start_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
        end_time = end_time.strftime("%a %b %d %Y 00:00:00 GMT+0800")
        filters = {
                "beginTime":    start_time,
                "endTime":      end_time
        }
        step = 10
        start_pos = 0
        batchId = 0
        
        query_data = build_query(filters, start_pos, batchId, step)
        #print query_data
        adr_url = 'http://www.adrs.org.cn/ADR/dwr/call/plaincall/reportSearchService.dwrReportSearchCg.dwr'
       
        opt = {
        "c0-e1" : "number:" + str(start_pos),
        "c0-e2" : "number:" + str(step),
        "c0-e3" : "string:123_w_w_w_321_colon",
        "c0-e4": "string:123_w_w_w_321_comma",
        "c0-e5" : "string:",
        "c0-param0": "Object_Object:{start:reference:c0-e1, limit:reference:c0-e2, analyticsRuleColon:reference:c0-e3, analyticsRuleComma:reference:c0-e4, queryString:reference:c0-e5}"
        }
        out_data = send_post3(adr_url,query_data,opt_headers=opt)
        if out_data is None:
            #
            print u'返回空数据，重新操作本月份数据'
        else:
            #print len(out_data)
            total = out_data.split(";")
            if len(total)!= 683:
                print u'返回数据长度不够，重新操作本月份数据'
            else:
                total_no = total.pop()
                temp =total[681].split(",")[3].split(":")[1].strip(")")
                temp2 = temp.split("}")[0]
                print u"本月条数：",temp2

                cur.execute(
                    "insert into mdr_checklist (BeginDate,EndDate,Item,Tag,CheckTag,Year,Month) "
                    "value(%s,%s,%s,%s,%s,%s,%s)", (out, out1, str(temp2), "M", "Y", yaer, month)
                )
                conn.commit()
    print u"本次任务已经结束"

if __name__ == "__main__":
    #checklistauto()
    pass