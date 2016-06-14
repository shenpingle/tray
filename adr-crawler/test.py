#-*- coding:utf-8 -*-
from utils import *
from utils_psur import *

def get_report():
    #
    from login2 import login
    logincounter = 10
    while logincounter:
        print logincounter
        if login():
            print "ok"
            break
        else:
            print "clear"
            cookieManager.clear()
            logincounter = logincounter -1

    report_url = "http://www.adrs.org.cn/ADR/page/adrpage/psur/viewPsurReport.jsp?fdObjectId=243014104899856270079204100000&type=2"
    somedata = send_url2(report_url)
    print  "test:",somedata
    n =11
    extrainfo = extradata3(somedata)
    dataout = [extrainfo[i:i+n] for i in range(0, len(extrainfo), n)]
    print "temp:", dataout
    erd = data2clean2(extrainfo)
    print erd

if __name__ == '__main__':
    print "test ..."
    print u"开始下载"
    get_report()