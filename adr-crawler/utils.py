#-*- coding:utf-8 -*-
###########################################################################################
#  author:luu
#  说明:常用功能函数
#
#  Revision: 1.0
###########################################################################################
import os
import json
from common import *
import time
from bs4 import BeautifulSoup
import urllib
import socket
import re
from config import *
import mdrsql

response = None
json_data = None
reportdata = None

#获取表格
re_table = re.compile(r'''<table[^>]+>(.*?)</table>''',re.M|re.S)
re_td = re.compile(r'''<td[^>]*>((\s|\S)+?)</td>''',re.M|re.U)

#获取省、市、县评论信息
re_eval = re.compile(r'<div id="smdr_eval_info">\s+<div class="div_title_table">(.*?)</div>',re.M|re.S)

#获取关联性评价信息
re_evalute = re.compile(r'<div id="rel_evaluate_info">\s+<div class="div_title_table">(.*?)</table>',re.M|re.S)

re_td_val = re.compile(r'<label[^>]+>√</label>(.+?)\&nbsp;',re.M|re.S)

re_EvalId_val = re.compile(r"viewRelEvalWindow\('([a-z0-9-]+)'\);",re.U)

def getcode_new():
    #部分不服务器不支持这个版本 刘欣毅
    #获取登录验证码
    curdir = os.getcwd()
    code_filename = curdir + '\code2.txt'
    ocr_file = curdir + "\\ocr.bat"
    
    if os.path.isfile(code_filename):
        os.remove(code_filename)
    
    if os.path.exists(ocr_file):
        #os.system(ocr_file)
        os.popen(ocr_file,"r")
        #os.spawnl(os.P_NOWAIT,ocr_file)
    else :
        print u"ocr.bat文件不存在！"

    file_object = open(curdir + '\\code2.txt', 'r')
    capacha = file_object.readline(4)
    file_object.close()

    return capacha

def getcode():
    #
    #获取登录验证码
    code_filename = './code2.txt'
    here = os.path.isfile(code_filename)
    if here:
        os.remove(code_filename)

    here2 = False
    while not here2:
        os.popen("ocr.bat", "r")
        here2 = os.path.exists(code_filename)
    file_object = open('code2.txt', 'r')
    capacha = file_object.readline(4)
    file_object.close()

    return capacha

#通用请求
def send_url(url):
    #
    global response
    try:
        common_url = urllib2.Request(url)
        response = urllib2.urlopen(common_url, timeout=120)
    except (urllib2.HTTPError, urllib2.URLError, socket.error), exception:
        pass

    return response
#psur report get request
def send_url2(url):
    #
    global reportdata

    try:
        common_url = urllib2.Request(url)
        response = urllib2.urlopen(common_url, timeout=10)
        reportdata = response.read().decode('utf-8')
    except (urllib2.HTTPError, urllib2.URLError, socket.error), exception:
        print u'额外数据解析,即返回整个文本,psur:', exception
        print "reportdata:",reportdata
        pass

    return reportdata

#post请求
def send_post(url, postdata):
    
    response_data = None

    #网络不稳定，加个循环
    while not response_data:
        try:
            common_url = urllib2.Request(url)
            response = urllib2.urlopen(common_url, data=postdata, timeout=150)
            response_data = response.read().decode('utf-8')            
            break #成功就中断循环
        except (urllib2.HTTPError, urllib2.URLError, socket.error), exception:
            print 'send_post:', exception
            continue

    return response_data

#post请求之json
def send_post_json(url, postdata):
    #
    global json_data
    try:
        common_url = urllib2.Request(url)
        common_url.add_header('Content-Type', 'application/json')
        json_response = urllib2.urlopen(common_url, json.dumps(postdata), timeout=100)
        json_data = json_response.read().decode('utf-8')
        #print 'send_post_json result:',json_data
        #json_response.close()
    except (urllib2.HTTPError, urllib2.URLError, socket.error), exception:
        print 'send_post_json:', exception
        print 'send_post_json data:', json_data

    return json_data

def send_post_json_me(url, postdata):
    #
    global json_data
    try:
        common_url = urllib2.Request(url)
        common_url.add_header('Content-Type', 'application/json')
        #json_response = urllib2.urlopen(common_url, json.dumps(postdata), timeout=400)
        #print 'postdata 100:', postdata
        #json_response = urllib2.urlopen(common_url, json.dumps(postdata), timeout=2)
        json_response = urllib2.urlopen(common_url, json.dumps(postdata), timeout=400)
        json_data = json_response.read().decode('utf-8')
        #json_response.close()
    except (urllib2.HTTPError, urllib2.URLError, socket.error), exception:
        print 'send_post_json_me:', exception
        pass

    return json_data

def send_post_json2(url, postdata, type, commonid, commondate):
    #
    global json_data
    try:
        common_url = urllib2.Request(url)
        common_url.add_header('Content-Type', 'application/json')
        #print 'postdata:', postdata
        #json_response = urllib2.urlopen(common_url, json.dumps(postdata), timeout=3)
        #json_response = urllib2.urlopen(common_url, json.dumps(postdata), timeout=400)
        json_response = urllib2.urlopen(common_url, json.dumps(postdata), timeout=400)
        json_data = json_response.read().decode('utf-8')
        #json_response.close()
    except (urllib2.HTTPError, urllib2.URLError, socket.error), exception:
        if type == 1:
            #write log
            myconn = myconnect()
            mycu = myconn.cursor()
            mycu.execute(
                "insert into mdr_errorlist(Date,ReportID,TypeTag,ClassTag)"
                "values(%s,%s,%s,%s)", (commondate, commonid, "E", "D"))
            myconn.commit()
        else:
            #print 'send_post_json2:', exception
            pass

    return json_data

def mdr_send_post(url, postdata, type, commonid, commondate):
    json_data = None

    #网络不稳定，加个循环
    while not json_data:
        try:
            common_url = urllib2.Request(url)
            common_url.add_header('Content-Type', 'application/json')
            json_response = urllib2.urlopen(common_url, postdata, timeout=400)
            json_data = json_response.read().decode('utf-8')
            break # 成功就退出循环
        except (urllib2.HTTPError, urllib2.URLError, socket.error), exception:
            print 'mdr_send_post error:',exception
            continue

    return json_data

def send_post3(url, postdata):
    #
    global response_data
    try:
        #header = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)", "Content-type": "text/plain"}
        header = {
            'Accept': 'text/html',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN',
            'Connection':  'keep-alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Referer':"http://www.adrs.org.cn/sso/login?service=http%3A%2F%2Fwww.adrs.org.cn%2FPF%2FcasAuthUser"
        }
        common_url = urllib2.Request(url, headers=header)
        #response = urllib2.urlopen(common_url, data=postdata, timeout=400)
        response = urllib2.urlopen(common_url, data=postdata, timeout=10)
        response_data = response.read().decode('utf-8')
    except (urllib2.HTTPError, urllib2.URLError, socket.error), exception:
        print 'send_post:', exception
        pass

    return response_data

def send_post2(url, _data):
    #
    global response
    try:
        common_url = urllib2.Request(url)
        if isinstance(_data, dict):
            #
            common_url.add_header('Content-Type', 'application/json')
            _data = json.dumps(_data)
        else:
            pass
            #response = urllib2.urlopen(common_url, data=_data, timeout=500)
        response = urllib2.urlopen(common_url, data=_data, timeout=10)
        response_data = response.read().decode('utf-8')
        #
    except(urllib2.HTTPError, urllib2.URLError, socket.error), exception:
        print exception
    else:
        pass

    return response_data

def unicode_to_str(text, encoding=None, errors='strict'):
    """Return the str representation of text in the given encoding. Unlike
    .encode(encoding) this function can be applied directly to a str
    object without the risk of double-decoding problems (which can happen if
    you don't use the default 'ascii' encoding)
    """

    if encoding is None:
        encoding = 'utf-8'
    if isinstance(text, unicode):
        return text.encode(encoding, errors)
    elif isinstance(text, str):
        return text
    else:
        raise TypeError('unicode_to_str must receive a unicode or str object, got %s' % type(text).__name__)

def str_to_unicode(text, encoding=None, errors='strict'):
    """Return the unicode representation of text in the given encoding. Unlike
    .encode(encoding) this function can be applied directly to a unicode
    object without the risk of double-decoding problems (which can happen if
    you don't use the default 'ascii' encoding)
    """

    if encoding is None:
        encoding = 'utf-8'
    if isinstance(text, str):
        return text.decode(encoding, errors)
    elif isinstance(text, unicode):
        return text
    else:
        raise TypeError('str_to_unicode must receive a str or unicode object, got %s' % type(text).__name__)

def data_check_type(somedata):
    backdata = ''
    if isinstance(somedata, long):
        backdata = str(somedata)
    elif isinstance(somedata, int):
        backdata = str(somedata)
    elif isinstance(somedata, unicode):
        backdata = somedata
    else:
        backdata = str(somedata)

    return backdata

def icd_check(_data):
    tag = '；'
    tagx = ';'
    _tempx = []
    _tag = str_to_unicode(tag)
    _tagx = str_to_unicode(tagx)
    _data =_data.replace(_tagx, _tag)
    _data_ = str_to_unicode(_data.lstrip().rstrip())
    _temp = _data_.split(_tag)

    for i in _temp:
        if not i:
            pass
        else:
            _tempx.append(i)


    return _tempx


def readdata(_tempdata):
    soup = BeautifulSoup(_tempdata)
    mydivs = soup.findAll("div", {"id": "smdr_eval_info"})
    something = []
    temp_s = []
    if mydivs:
        tr = soup.findAll("div", {"id": "smdr_eval_info"})[0].findAll("td")
        for trdata in tr:
            something.append(trdata.get_text().lstrip().rstrip())
        temp_s = something
    else:
        pass

    return temp_s

def _single_select(_data):
    tag_1 = '○'
    tag_2 = '√'
    _tag_1_data = str_to_unicode(tag_1)
    _tag_2_data = str_to_unicode(tag_2)
    _temp = _data.split(_tag_1_data)
    _tempdata = ''

    for _abc in _temp:
        if _abc.find(_tag_2_data) != -1:
            _tempdata =_abc.split(_tag_2_data)[1]
        else:
            pass

    return _tempdata

def event_info(ly):
    a = []
    i = 0
    _tag = '关联性评价结论'
    tag2 = '是否符合报告要求'
    tag3 = '事件初步原因分析'
    tag4 = '备　　注'
    tag5 = '评价单位'
    tag6 = '评价人'
    tag7 = '评价时间'
    tag8 = '附件'
    _sunny = str_to_unicode(_tag)
    sunny2 = str_to_unicode(tag2)
    sunny3 = str_to_unicode(tag3)
    sunny4 = str_to_unicode(tag4)
    sunny5 = str_to_unicode(tag5)
    sunny6 = str_to_unicode(tag6)
    sunny7 = str_to_unicode(tag7)
    sunny8 = str_to_unicode(tag8)
    while (i < len(ly)):
        _pdata = ly[i].find(_sunny)
        pdata2 = ly[i].find(sunny2)
        pdata3 = ly[i].find(sunny3)
        pdata4 = ly[i].find(sunny4)
        pdata5 = ly[i].find(sunny5)
        pdata6 = ly[i].find(sunny6)
        pdata7 = ly[i].find(sunny7)
        pdata8 = ly[i].find(sunny8)
        #结论
        if _pdata != -1:
            #print 'test:',i
            a.append(_single_select(ly[i+1]).lstrip().rstrip().strip())
            #合规
        if pdata2 != -1:
            #print 'test 2:',i
            a.append(ly[i+1].lstrip().rstrip().strip())
            #初步分析
        if pdata3 != -1:
            #print 'test 3:',i
            a.append(ly[i+1].lstrip().rstrip().strip())
            #备注
        if pdata4 != -1:
            #print 'test 4:',pdata4
            a.append(ly[i+1].lstrip().rstrip().strip())
            #单位
        if pdata5 != -1:
            #print 'test 5:',i
            a.append(ly[i+1].lstrip().rstrip().strip())
            #评价人
        if pdata6 != -1:
            #print 'test 6:',i
            a.append(ly[i+1].lstrip().rstrip().strip())
            #时间
        if pdata7 != -1:
            #print 'test 7:',i
            a.append(ly[i+1].lstrip().rstrip().strip())
            #附件
        if pdata8 != -1:
            #print 'test 8:',i
            a.append(ly[i+1].lstrip().rstrip().strip())

        i += 1
    return a

def ndyp_province(somedata):
    a = []
    i = 0
    tag = '省食品药品评价中心评价意见'
    sun = str_to_unicode(tag)
    tom = ''
    somedata.append(tom)
    somedata.append(tom)
    somedata.append(tom)
    while (i < len(somedata)):
        #测试环境下可以使用下面两条数据
        pdata=somedata[i].find(sun)
        while (pdata != -1):
            #
            for itor in range(i,i+17):
                if not somedata[itor]:
                    somedata[itor] = ''
                else:
                    pass
                a.append(somedata[itor])
                if itor == 17:
                    break
            break
            #break

        i += 1

    return a

def smdr_province_info(_data):
    lyy = ndyp_province(readdata(_data))
    cdata = event_info(lyy)
    n = 8
    dataout = [cdata[i:i+n] for i in range(0, len(cdata), n)]
    return dataout

def ndyp_district(somedata):
    a = []
    i = 0
    tag = '药品不良反应监测中心'
    sun = str_to_unicode(tag)
    tom = ''
    somedata.append(tom)
    somedata.append(tom)
    somedata.append(tom)
    while (i < len(somedata)):
        pdata = somedata[i].find(sun)
        if pdata!=-1:
            for itor in range(i, i+17):
                if not somedata[itor]:
                    somedata[itor] = ''
                else:
                    pass
                a.append(somedata[itor])
                if itor == 17:
                    break
            break

        i += 1

    return a

def smdr_district_info(_data):
    lyy = ndyp_district(readdata(_data))
    cdata = event_info(lyy)
    n = 8
    dataout = [cdata[i:i+n] for i in range(0, len(cdata), n)]
    return dataout

def ndyp_county(somedata):
    a = []
    i = 0
    #食品药品监督管理局
    #食品药品监督管理局ADR中心
    #河南省南阳市社旗县ADR中心
    #河南省商丘市食品药品稽查一队
    tag = '食品药品'
    sun = str_to_unicode(tag)
    tag_1 = 'ADR中心'
    sun_1 = str_to_unicode(tag_1)
    tag_2 = '市药品不良反应监测中心'
    sun_2 = str_to_unicode(tag_2)

    tom = ''
    somedata.append(tom)
    somedata.append(tom)
    somedata.append(tom)

    while (i < len(somedata)):
        #测试环境下可以使用下面两条数据
        pdata = somedata[i].find(sun)
        pdata_1 = somedata[i].find(sun_1)
        pdata_2 = somedata[i].find(sun_2)
        while (pdata != -1 or pdata_1!=-1 or pdata_2 !=-1):
            #for itor in range(i, i+17):非退回数据，正常
            for itor in range(i, i+17):
                if not somedata[itor]:
                    somedata[itor] = ''
                else:
                    pass
                a.append(somedata[itor])
                if itor == 17:
                    break
            break
        break

        i += 1

    return a

def smdr_county_info(_data):
    lyy = ndyp_county(readdata(_data))
    cdata = event_info(lyy)
    n = 8
    dataout = [cdata[i:i+n] for i in range(0, len(cdata), n)]
    return dataout


def event_info_evaluate(ly):
    a = []
    i = 0
    _tag = '1'
    tag2 = '1'
    tag3 = '3'
    tag4 = '关联性评价结果'

    _sunny = str_to_unicode(_tag)
    sunny2 = str_to_unicode(tag2)
    sunny3 = str_to_unicode(tag3)
    sunny4 = str_to_unicode(tag4)

    while (i < len(ly)):
        _pdata = ly[i].find(_sunny)
        pdata2 = ly[i].find(sunny2)
        pdata3 = ly[i].find(sunny3)
        pdata4 = ly[i].find(sunny4)

        #1
        if _pdata != -1:
            #print 'test:',i
            a.append(_single_select(ly[i+1]))
            #2
        if pdata2 != -1:
            #print 'test 2:',i
            a.append(_single_select(ly[i+1]))
            #3
        if pdata3 != -1:
            #print 'test 3:',i
            a.append(_single_select(ly[i+1]))
            #关联性评价结果
        if pdata4 != -1:
            #print 'test 4:',pdata4
            a.append(_single_select(ly[i+1]))

        i +=1
    return a



def readdata_evaluate(_temp):
    soup = BeautifulSoup (_temp)
    mydivs = soup.findAll("div", {"id": "rel_evaluate_info"})
    something = []
    temp_s = []
    if mydivs:
        tr = soup.findAll("div", {"id": "rel_evaluate_info"})[0].findAll("td")
        for trdata in tr:
            something.append(trdata.get_text().lstrip().rstrip())
        temp_s = something
    else:
        pass

    return temp_s


def evaluate_info(_tempdata):
    _temp = readdata_evaluate(_tempdata)
    _temp_2 = event_info_evaluate(_temp)
    return _temp_2


def seeinfo(data):
    data = open(data, 'r').read()
    re_attach = re.compile(r'''(.*?);" value="查看" />''', re.M|re.U)
    result = re_attach.findall(data)
    tom = []
    c = ''.join(result).strip().split('\t')
    for i in c:
        if i:
            if i.find("(") != -1:
                ii = i.split("')")
                if ii:
                    #
                    for ia in ii:
                        if ia.find("(") != -1:
                            iii = ia.split("(")
                            if len(iii) == 2:
                                if len(iii[1].strip("'")) == 36:
                                    tom.append(iii[1].strip("'"))
            else:
                if i.find(")") != -1:
                    ii = i.split("')")
                    if len(ii[0]) == 36:
                        tom.append(ii[0])

    return tom

def readsee(_tempdata):
    soup = BeautifulSoup(_tempdata)
    mydivs = soup.findAll("div", {"class": "div_title_table"})
    something = []
    temp_s = []
    if mydivs:
        tr = soup.findAll("div", {"class": "div_title_table"})[0].findAll("td")
        for trdata in tr:
            something.append(trdata.get_text().lstrip().rstrip())
        temp_s = something
    else:
        pass

    return temp_s


def see_info(_tempdata):
    _temp = readsee(_tempdata)
    _temp_2 = event_info_evaluate(_temp)
    return _temp_2

def sex(_int):
    a = ''
    if _int == 1:
        a = '男'
    else:
        a = '女'
    return a

def bgly(_int):
    a = ''
    if _int == 1:
        a = '生产企业'
    elif _int == 2:
        a = '经营企业'
    elif _int == 3:
        a = '使用单位'
    elif _int == 4:
        a = '个人'
    else:
        pass

    return a

def event(_int):
    a = ''
    if _int == 1:
        a = '死亡'
    elif _int == 2:
        a = '危及生命'
    elif _int == 3:
        a = '机体功能结构永久性损伤'
    elif _int == 4:
        a = '可能导致机体功能结构永久性损伤'
    elif _int == 5:
        a = '需要内、外科治疗避免上述永久损伤'
    elif _int == 6:
        a = '其它'
    else:
        pass

    return a

def type_report(_int):
    a = ''
    if _int == 1:
        a = '医师'
    elif _int == 2:
        a = '技师'
    elif _int == 3:
        a = '护士'
    elif _int == 4:
        a = '工程师'
    elif _int == 5:
        a = '其他'
    else:
        pass

    return a

def type_op(_int):
    a = ''
    if _int == 1:
        a = '专业人员'
    elif _int == 2:
        a = '非专业人员'
    elif _int == 3:
        a = '患者'
    elif _int == 4:
        a = '其他'
    else:
        pass

    return a

def use(_int):
    a = ''
    if _int == 1:
        a = '医疗机构'
    elif _int == 2:
        a = '家庭'
    elif _int == 3:
        a = '其他'
    else:
        pass

    return a

def told(_int_list):
    #1,2,3,4:已通知使用单位,已通知生产企业,已通知经营企业,已通知药监部门
    ted = []
    for i in range(0, len(_int_list)):
        #if _int_list[i] == kf[i]:
        if _int_list[i] == 1:
            ted.append('已通知使用单位')
        if _int_list[i] == 2:
            ted.append('已通知生产企业')
        if _int_list[i] == 3:
            ted.append('已通知经营企业')
        if _int_list[i] == 4:
            ted.append('已通知药监部门')

    ted = ','.join(ted)

    return ted


def obj_id_slice(_data):
    len_data = len(_data)
    _temp = ''
    if len_data > 36:
        _temp = _data[2:]
    else:
        _temp = _data

    return _temp

def age_check(_data_):
    _data_back = ''
    if _data_:
        _data = int(_data_)
        if _data >= 0 and _data <= 2:
            _data_back = '婴儿'
        elif _data >= 3 and _data <= 5:
            _data_back = '幼儿'
        elif _data >= 6 and _data <= 12:
            _data_back = '儿童'
        elif _data >= 13 and _data <= 18:
            _data_back = '少年'
        elif _data >= 19 and _data <= 40:
            _data_back = '青年'
        elif _data >= 41 and _data <= 59:
            _data_back = '中年'
        elif _data >= 60 and _data <= 200:
            _data_back = '老年'
        else:
            _data_back = '未知'
    else:
    #_data_back = str(0)
        _data_back = '未知'

    return _data_back
"""
from config import *
def delete_by_time(t1, t2):
    try:
        mycu.execute("delete from mdr_business_gather where ReportDate>='%s' and ReportDate<='%s'" % (t1,t2))
        myconn.commit()
        mycu.execute("delete from mdr_adrbusiness where ReportDate>='%s' and ReportDate<='%s'" % (t1,t2))
        myconn.commit()
        mycu.execute("delete from mdr_faultbusiness where ReportDate>='%s' and ReportDate<='%s'" % (t1,t2))
        myconn.commit()
        mycu.execute("delete from mdr_icdbusiness where ReportDate>='%s' and ReportDate<='%s'" % (t1,t2))
        myconn.commit()
        mycu.execute("delete from mdr_devicebusiness where ReportDate>='%s' and ReportDate<='%s'" % (t1,t2))
        myconn.commit()

        mycu.close()
        myconn.close()
    except Exception as err:
        print err
        return False

    return True
"""

my_today = time.strftime('%Y-%m-%d',time.localtime(time.time()))

def mdr_slice(somedata):
    if isinstance(somedata,int) :
        somedata = str(somedata)
    else :
        somedata = str_to_unicode(somedata)
        
    tag = [",",".","?",":",";","'","，","。","？","：","；","‘","、"," "]
    new_tag = str_to_unicode(';')
    #replace
    some = None
    some_data = None
    some_temp = None
    for item in tag:
        pag = somedata.find(str_to_unicode(item))
        if pag != -1:
            some_temp = somedata.strip(str_to_unicode(item)).replace(str_to_unicode(item), str_to_unicode(new_tag))
            some = some_temp
            somedata = some
        else:
            some = somedata

    some_temp = some.split(str_to_unicode(new_tag))
    return some_temp

def data_set(data_list):
    ok = None
    some = []
    #a=['立即','[非标准:导尿]','急性化脓性阑尾炎','[非标准:缓解排尿状况]','感冒']
    for i in data_list:
        temp = ''.join(i)+','
        some.append(temp)
    some = ''.join(some).strip(str_to_unicode(','))
    #print some
    return some
"""
def routine():
    #测试数据库可连接及重新连接
    routine_tag = myconn.is_connected()
    if routine_tag:
        pass
    else:
        #
        myconn.reconnect(attempts=10, delay=10)
"""
"""
#注意：在过一段时间，进行任意时间段重新下载时，要删除这个时间段的所有mdr_reports、mdr_appraise表时段段内数据，所有加入DateTag字段
#mdr_reports:单位评价人评价信息
#mdr_appraise:监测机构评价（县、市、省）
#相对应在deletedance.py更改业务：
    1）mycu.execute("delete from mdr_appraise where DateTag>='%s' and DateTag<='%s'" % (t1, t2))
    2）mycu.execute("delete from mdr_reports where DateTag>='%s' and DateTag<='%s'" % (t1, t2))
#author:liuxinyi
#Date:2015-09-01
"""
def mdr_get_smd_appraise(smdrReportViewHtml, BianMa, obj_id,obj_name,DateTag):
    '''获取不良事件评价'''
    global re_eval,re_table,re_td,re_EvalId_val
    AppraiseLevel = ""
    report_sql = '''
    replace into mdr_appraise( 
                `BianMa` ,  `Obj_id`,  `AppraiseConclusion`,  `ReportRequirement` ,  `ReportPreliminaryAnalysisOfEvents`,  
                `AppraiseMemo` ,  `AppraiseUnitName`,  `AppraiseMan` ,  `AppraiseDate`,  `DateTag`,`ADRDateAnalyse`,`ADRTypeAnalyse`,`OtherRelatedAnalyse`,`Appraise`,`AppraiseLevel`
            ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
    
    match = re_eval.search(smdrReportViewHtml)
    if not match :
        print u'还没有评价信息',BianMa
        return

    try:
        body = match.group(1)
        reports = []
        for table in re_table.finditer(body):
            if not table :
                print 'BianMa:',BianMa, '解析评价信息失败！body:', body
                continue
            values = []
            
            for td in re_td.finditer(table.group(1)):
                if not td :
                    print 'BianMa:',BianMa, '解析评价信息失败！table:',table.group(0)
                values.append(td.group(1).strip())

            AppraiseConclusion = getTdVal(values[2])
            ReportRequirement = getTdVal(values[4])
            ReportPreliminaryAnalysisOfEvents = getTdVal(values[6])
            AppraiseMemo = getTdVal(values[8])
            AppraiseUnitName = getTdVal(values[10])
            AppraiseMan = getTdVal(values[12])
            AppraiseDate = getTdVal(values[14])

            
            evalIdMatch =  re_EvalId_val.search(values[2])
            evalId = None
            evalHtml = None

            ADRDateAnalyse = ""
            ADRTypeAnalyse = ""
            OtherRelatedAnalyse = ""
            Appraise = ""
            AppraiseLevel = get_AppraiseLevel(AppraiseUnitName)

            if evalIdMatch:
                evalId = evalIdMatch.group(1)
            if evalId :
                (ADRDateAnalyse,ADRTypeAnalyse,OtherRelatedAnalyse,Appraise) =  getEvalInfo(evalId)            

            report_value = (BianMa, obj_id, AppraiseConclusion,ReportRequirement,ReportPreliminaryAnalysisOfEvents,AppraiseMemo,
                            AppraiseUnitName,AppraiseMan,AppraiseDate,DateTag,ADRDateAnalyse,ADRTypeAnalyse,OtherRelatedAnalyse,Appraise,AppraiseLevel)
            mdrsql.mdr_insert_alone(report_sql,  report_value)
    except Exception, err:
        print BianMa,u'不良事件评论获取失败！', err
        
        #监管机构评价信息默认为空
        AppraiseConclusion = ""
        ReportRequirement =  ""
        ReportPreliminaryAnalysisOfEvents =  ""
        AppraiseMemo =  "Appraise error"
        AppraiseUnitName =  ""
        AppraiseMan =  ""
        AppraiseDate =  ""
        ADRDateAnalyse = ""
        ADRTypeAnalyse = ""
        OtherRelatedAnalyse = ""
        Appraise = ""
        AppraiseLevel=""

        report_value = (BianMa, obj_id, AppraiseConclusion,ReportRequirement,ReportPreliminaryAnalysisOfEvents,AppraiseMemo,
                        AppraiseUnitName,AppraiseMan,AppraiseDate,DateTag,ADRDateAnalyse,ADRTypeAnalyse,OtherRelatedAnalyse,Appraise,AppraiseLevel)
        mdrsql.mdr_insert_alone(report_sql,  report_value)

def getEvalInfo(evalId):    
    
    mdr_View_RelEval_url = 'http://www.adrs.org.cn/MDR/scripts/mdr/smdr/viewRelEval.jsp' # http://www.adrs.org.cn/MDR/scripts/mdr/smdr/viewRelEval.jsp
    post_data = 'smdrEvalID=%s' % evalId
    evalHtml = send_post(mdr_View_RelEval_url, post_data)    

    ADRDateAnalyse = ""
    ADRTypeAnalyse = ""
    OtherRelatedAnalyse = ""
    Appraise=""

    if evalHtml :
        tds =  re_td.findall(evalHtml)
        ADRDateAnalyse = getTdVal(tds[1][0])
        ADRTypeAnalyse = getTdVal(tds[3][0])
        OtherRelatedAnalyse = getTdVal(tds[5][0])
        Appraise = getTdVal(tds[7][0])
    return (ADRDateAnalyse,ADRTypeAnalyse,OtherRelatedAnalyse,Appraise)

def getTdVal(value):
    ''''获取单元格内的值 '''
    re_td_val = re.compile(u'<label[^>]+>√</label>(.+?)&nbsp;',re.M|re.U)
    re_Label_val = re.compile(u'<label[^>]+>○</label>', re.U);
    result = ""
    
    match = re_td_val.search(value)
    
    if match :
        result = match.group(1)
    else:
        hasLabel = re_Label_val.search(value)
        if hasLabel :
            result = ""
        else :
            result = value
    result = result.replace("&nbsp;","")
    result = re.sub(r'\s','',result)
    #liuxinyi151102，设置32太小，如编码：153530209201100311：继续监测;考虑为患者机体与节育环的排异反应或是节育环类型、型号的选择不当有关。
    #153530000201100006：继续监测;主要考虑为可能是所使用药物的不良反应，或是患者自身病情发展所致，但也不能排除与使用该输液器有关。
    #153530000201100050：继续监测;考虑为患者可能对贴的药物成份过敏，或是对贴布的粘性成份过敏所致，但该产品的注册证号在国家局网站中无法查询到，请继续监测该产品使用情况。
    if len(result) > 100 :
        result = result[:100]

    return result

def get_AppraiseLevel(unitName):

    mdr_query = "select distinct role from mhisuser where unitname='%s'" % unitName

    mdr_row = mdrsql.mdr_select(mdr_query) # 返回结果是多行
    if len(mdr_row) > 0 :
        mdr_row = mdr_row[0]
    else :
        return ""

    if len(mdr_row) > 0 :
        return mdr_row[0]
    return ""


def get_smd_report(smdrReportViewHtml, report_id,obj_id, obj_name,ReportUnitLinkman,ReportUnitWork,DateTag):
    #D.关联性评价
    global re_evalute,re_td
    
    report_sql = (
                '''replace into mdr_reports(
                BianMa,
                ReportUnitnName,               
                ReportAppraiseDate,
                
                ReportUnitADRDateAnalyse,
                ReportUnitADRTypeAnalyse,
                ReportUnitOtherRelatedAnalyse,                
                ReportUnitAppraise, 
                
                ReportUnitLinkman,
                ReportUnitWork,
                DateTag,
                ReportUnitComments)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            )
    mdr_sql = "SELECT BianMa,ReportUnitName,StateReportDate FROM `mdr_business_gather` where BianMa='%s'" % (report_id)
    mdr_row = mdrsql.mdr_select(mdr_sql) # 返回结果是多行
    if len(mdr_row) > 0 :
        mdr_row = mdr_row[0]
    
    if len(mdr_row) != 3 :
        return
        
    BianMa = mdr_row[0]
    ReportUnitName = mdr_row[1]
    ReportAppraiseDate = mdr_row[2]

    eval_match = re_evalute.search(smdrReportViewHtml)
    if not eval_match:
        print u'暂时还没有关联性评价信息!'
        return 
    
    ReportUnitADRDateAnalyse = ""
    ReportUnitADRTypeAnalyse = ""
    ReportUnitOtherRelatedAnalyse = ""
    ReportUnitAppraise = ""
    ReportUnitComments=""   #单位评价备注，如果能正常抓取信息，备注默认为空，否则=Unit appraise error

    try:
        ping_jia_infos = re_td.findall(eval_match.group(1))
        if len(ping_jia_infos) > 0:
            ReportUnitADRDateAnalyse = getTdVal(ping_jia_infos[2][0])
            ReportUnitADRTypeAnalyse = getTdVal(ping_jia_infos[4][0])
            ReportUnitOtherRelatedAnalyse = getTdVal(ping_jia_infos[6][0])
            ReportUnitAppraise = getTdVal(ping_jia_infos[8][0])
        
        report_values = (BianMa,ReportUnitName,ReportAppraiseDate,ReportUnitADRDateAnalyse,ReportUnitADRTypeAnalyse,ReportUnitOtherRelatedAnalyse,ReportUnitAppraise,ReportUnitLinkman,ReportUnitWork,DateTag,ReportUnitAppraise)
        mdrsql.mdr_insert_alone(report_sql,  report_values)
    except Exception, err:
        print BianMa,u'关联性评价获取失败',err

        #评价信息默认为空
        ReportUnitADRDateAnalyse = ""
        ReportUnitADRTypeAnalyse = ""
        ReportUnitOtherRelatedAnalyse = ""
        ReportUnitAppraise =  ""
        ReportUnitComments=""
        report_values = (BianMa,ReportUnitName,ReportAppraiseDate,ReportUnitADRDateAnalyse,ReportUnitADRTypeAnalyse,ReportUnitOtherRelatedAnalyse,ReportUnitAppraise,ReportUnitLinkman,ReportUnitWork,DateTag,ReportUnitAppraise)
        mdrsql.mdr_insert_alone(report_sql,  report_values)

def getReportStatus(report_id, obj_id, sned_date):
    #事件报告状态
    mdr_Url_1_SmdReportStatus = 'http://www.adrs.org.cn/MDR/ep/smdrFindList/FindListSmdReportService/getSmdReportStatus'
    querydata_1_SmdReportStatus = 'params={"funcID":"MDR_SMDR_BROWSE_01","userID":78919,"operations":[{"actionName":"query","count":1,"operationDatas":[{"FD_OBJECTID":%s,"action":"update"}]}]}' % obj_id
    
    #网络不稳定，加个循环
    while True:
        data_SmdReportStatus = mdr_send_post(mdr_Url_1_SmdReportStatus, querydata_1_SmdReportStatus, 2, report_id, sned_date)
        if not data_SmdReportStatus :
            continue

        try:
            _report_SmdReportStatus = json.loads(data_SmdReportStatus)
        except  Exception,err:
            print err,'getSmdReportStatus抓取失败，body:',data_SmdReportStatus
            continue
        break

    len_rs = _report_SmdReportStatus['ResponseMessage']['operations'][0]['count']
    tom = []
    if len_rs > 0:
        for i in range(0, len_rs):
            status_val = ""
            sam = _report_SmdReportStatus['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][2]['v']
            if sam == 1 :
                status_val =  u"已通知使用单位"
            if sam == 2:
                status_val =u"已通知生产企业"
            if sam == 3:
                status_val = u"已通知经营企业"
            if sam == 4 :
                status_val =  u"已通知药监部门"
            tom.append(status_val)
    return tom

def getReportUnitDistrictInfo(ReportUnitName):
    report_unit_sql = (  """SELECT ProvinceName,DistrictTypeID,County  FROM `unit` where Name="%s" limit 1""" % (ReportUnitName) )
    rows_unit = None
    rows_unit = mdrsql.mdr_select(report_unit_sql)
    #行政区域匹配
    if rows_unit:
        for unit_info in rows_unit:
            ProvinceName = unit_info[0]
            District = unit_info[1]
            County = unit_info[2]
    else:
        County = ""
        District = ""
        ProvinceName = ""
    return (County,District,ProvinceName)

def getDeviceInstrumentInfo(production_name):
    #获取器械的基础数据

    deviceInfo = {}
    un_device_info = None
    Is_m_device = None
    _un_tag_device_1 = str_to_unicode(u"[非标准:")
    _un_tag_device_2 = str_to_unicode(u"]")

    rows_device_sql = (
                "SELECT SuperClassName, subname, Name, classcode, manageclass FROM `mdr_deviceinstrument` where Name='%s' limit 1" % (production_name)
            )
    rows_device = mdrsql.mdr_select(rows_device_sql)

    if rows_device:
        Is_m_device = u'是'
        for rows_device_info in rows_device:
            SuperClassName = rows_device_info[0]
            subname = rows_device_info[1]
            Name = rows_device_info[2]
            classcode = rows_device_info[3]
            d_5 = rows_device_info[4]
            manageclass = rows_device_info[4]
        _un_device_info = Name
        un_device_info = Name

    else:
        Is_m_device = u'否'
        un_device_info = _un_tag_device_1+production_name+_un_tag_device_2
        un_device_info = str_to_unicode(un_device_info)
        SuperClassName = ""
        subname = ""
        Name = ""
        classcode = ""
        manageclass = ""

    deviceInfo["SuperClassName"] = SuperClassName
    deviceInfo["subname"] = subname
    deviceInfo["Name"] = Name
    deviceInfo["classcode"] = classcode
    deviceInfo["manageclass"] = manageclass

    return (un_device_info,Is_m_device,deviceInfo)

def getSmdrWhoArt(BianMa,sned_date,obj_id):
    #获取smdrWhoArt
    sh_info = None 

    mdr_Home_1_report_sh = 'http://www.adrs.org.cn/MDR/ep/smdrFindList/FindListSmdReportService/getSmdrWhoArt'
    querydata_1_report_sh = 'params={"funcID":"MDR_SMDR_BROWSE_01","userID":78919,"operations":[{"actionName":"query","count":1,"operationDatas":[{"FD_OBJECTID":%s, "action":"update"}]}]}' % (obj_id)
    report_data_full_sh = mdr_send_post(mdr_Home_1_report_sh, querydata_1_report_sh,4, BianMa, sned_date)
    try:
        _report_sh = json.loads(report_data_full_sh)
    except Exception,err:
        print err,'getSmdrWhoArt抓取失败！body:',report_data_full_sh
        return

    total_sh = _report_sh['ResponseMessage']['operations'][0]['count']
    if total_sh != 0:
        _sh_info = _report_sh['ResponseMessage']['operations'][0]['operationDatas'][0]['es'][3]['v']
        sh_info = mdr_slice(_sh_info)

    return sh_info


# 2016.06.07年修改
def getsmdrfda(obj_id, bianma, sned_date):

    mdr_home_1_report_qg = 'http://www.adrs.org.cn/MDR/ep/smdrFindList/FindListSmdReportService/getSmdrFDA'
    querydata_1_report_qg = 'params={"funcID": "MDR_SMDR_BROWSE_01", "userID": 78919, "operations": [{"actionName": ' \
                            '"query","count": 1, "operationDatas": [{"FD_OBJECTID": %s, "action": "update"}]}]}' \
                            % obj_id
    report_data_full_qg = mdr_send_post(mdr_home_1_report_qg, querydata_1_report_qg, 3, bianma, sned_date)

    try:
        _report_qg = json.loads(report_data_full_qg)
    except Exception, err:
        print err, 'getSmdrFDA抓取失败，body:', report_data_full_qg
        return

    total_qg = _report_qg['ResponseMessage']['operations'][0]['count']

    if total_qg != 0:
        _qg_info = _report_qg['ResponseMessage']['operations'][0]['operationDatas'][0]['es'][3]['v']
        qg_info = mdr_slice(_qg_info)
        return qg_info
