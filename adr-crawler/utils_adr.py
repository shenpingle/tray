#-*- coding:utf-8 -*-
###########################################################################################
#
#  此文件提供一些封装的实用函数
#
###########################################################################################

import urllib2,StringIO,gzip,urllib,re
from HTMLParser import HTMLParser
import sys
import random
import logging


def getUrlResponse(cookieManager, url, data=None, opt_headers={}):
    '''带Cookie的请求'''
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieManager))
    urllib2.install_opener(opener)

    header = {
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN',
        'Connection':  'keep-alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
        'Referer':"http://www.adrs.org.cn/sso/login?service=http%3A%2F%2Fwww.adrs.org.cn%2FPF%2FcasAuthUser"
        }
    if opt_headers :
        header.update(opt_headers)
        
    req = urllib2.Request(url = url,headers = header)
    
    if data:
        req.add_data(data)
        
    try:
        fp=opener.open(req)
    except:
        return False

    if "Content-Encoding" in fp.headers and "gzip" in fp.headers.get("Content-Encoding"):
        compresseddata = fp.read()
        compressedstream = StringIO.StringIO(compresseddata)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        fp_read = gzipper.read()
        gzipper.close()
        return fp_read
        
    return fp.read()
    

def get_page_list(cj, filter=None, startpos=0, step = 10):
    '''分布获取数据'''
    batchId = 0
    
    opt = {
        "Referer" : 'http://www.adrs.org.cn/PF/page/frameWork.html',
        'Content-Type' : 'text/plain'
        }
        
    re_match = re.compile(r"\['([^']+)'\]=\"?([^;]*?)\"?;",re.U)
    
    p = HTMLParser()
    
    #上一年度
    #time.strftime("%a %b %d %Y 00:00:00 GMT+0800 ")
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
            print "start query of batch: %s" % (batchId)
            ret_body = getUrlResponse(cj, 'http://www.adrs.org.cn/ADR/dwr/call/plaincall/reportSearchService.dwrReportSearchCg.dwr', data=query_data, opt_headers=opt)
            print "end query of batch: %s" % (batchId)
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
            
def build_query(filter, startpos, batchid, step = 10):
    '''
    @filter = {
        "beginTime" :    "Sat Jan 01 2011 00:00:00 GMT+0800"
        "endTime"   :    "Sat Dec 31 2011 00:00:00 GMT+0800"
    }
    '''
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