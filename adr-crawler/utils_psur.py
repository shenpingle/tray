#-*- coding:utf-8 -*-
from utils import *
from login2 import login
from utils import *
import codecs
import mdrsql
from bs4 import BeautifulSoup

#################################################################################################
#下载文件，写入指定路径下
#20141011
#begining
#################################################################################################
def mkdir(path, id):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    mypath = path+"\\"+id
    isExists = os.path.exists(mypath)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print mypath + u' 创建成功'
        # 创建目录操作函数
        os.makedirs(mypath)
        return mypath
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print mypath + u' 目录已存在'
        return mypath

def gather_report_total(_timedict):
    t = _timedict
    t_start = t['beginTime']
    t_end = t['endTime']

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

    #首先获取记录条数总记录
    totalparamsx = {"funcID":"QUERY_DATA","userID":78919,"operations":[{"actionName":"query","operationDatas":[{"ENTRY_START_DATE_2401":t_start,"ENTRY_END_DATE_2401":t_end,"ACTIVE_CONSTITUENT_2430":"","TRADENAME_CN_2431":"","DRUGNAME_CN_FORM_2431":"","DOSEFORM_2431":"","DRUG_STATUS_2431":"","APPROVAL_NO_2431":"","REPORT_ID_2430":"","PICKER_UNIT_NAME_2430":"","START_APPLY_DATE_2430":"","END_APPLY_DATE_2430":"","listid":"2430_1","start":0,"limit":10}]}]}
    _idcdata = send_post_json(Psur_url, totalparamsx)
    #print _idcdata
    usa = 0
    try:
        _data = json.loads(_idcdata)
        usa = _data['ResponseMessage']['operations'][0]['pageTotal']
    #TypeError: expected string or buffer
    except (IndexError, KeyError, ValueError,TypeError), exception:
        print "gather_report_total:",exception
        print "IN json Data:", _idcdata

    total_usa = int(usa-1)
    total = (total_usa/100)+1
    reportlog = codecs.open('psurlog.txt', 'a', 'utf-8')
    reportlog.write('application start run time:'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n')
    reportlog.write('total:'+str(total_usa) + '\n')
    reportlog.write('page:'+str(total) + '\n')
    reportlog.close()
    return total

def readall(_tempdata):
    soup = BeautifulSoup(_tempdata)
    mydivs = soup.findAll("div", {"id": "psurReportBoby"})
    something = []
    temp_s = []
    if mydivs:
        tr = soup.findAll("td", {"class": "tdShow"})
        for trdata in tr:
            something.append(trdata.get_text().lstrip().rstrip())
        temp_s = something
    else:
        pass

    return temp_s

#药品产品信息
def psur_info(_tempdata):
    soup = BeautifulSoup(_tempdata)
    mydivs = soup.findAll("div", {"id": "psurReportBoby"})
    something = []
    temp_s = []
    if mydivs:
        #tr = soup.findAll("div", {"id": "DIV_PSUR_INFO"})[0].findAll("span")
        tr = soup.findAll("div", {"id": "DIV_PSUR_INFO"})[0].findAll("span")
        for trdata in tr:
            something.append(trdata.get_text().lstrip().rstrip())
        temp_s = something
    else:
        pass

    return temp_s
#评价信息
def psur_eval_info(_tempdata):
    soup = BeautifulSoup(_tempdata)
    mydivs = soup.findAll("div", {"id": "psurReportBoby"})
    something = []
    temp_s = []
    if mydivs:
        tr = soup.findAll("div", {"id": "evalInfoDiv"})[0].findAll("td")
        for trdata in tr:
            something.append(trdata.get_text().lstrip().rstrip())
        temp_s = something
    else:
        pass

    return temp_s[6:]

#修改日志
def psur_changelog_info(_tempdata):
    soup = BeautifulSoup(_tempdata)
    mydivs = soup.findAll("div", {"id": "psurReportBoby"})
    something = []
    temp_s = []
    if mydivs:
        tr = soup.findAll("div", {"id": "modifyLogInfo"})[0].findAll("td")
        for trdata in tr:
            something.append(trdata.get_text().lstrip().rstrip())
        temp_s = something
    else:
        pass

    return temp_s[6:]

#DWF
def psur_DWF_info(_tempdata):
    soup = BeautifulSoup(_tempdata)
    mydivs = soup.findAll("div", {"id": "psurReportBoby"})
    something = []
    temp_s = []
    if mydivs:
        tr = soup.findAll("div", {"id": "DIV_PSUR_ATTACHMENT_INFO"})[0].findAll("td")
        for trdata in tr:
            something.append(trdata.get_text().lstrip().rstrip())
        temp_s = something
    else:
        pass

    return temp_s[6:]

#无来源数据解析
def ghostdata(ly):
    a = []
    i = 0
    tag2 = u'报告期(数据起止日期)'

    sunny2 = tag2
    while (i < len(ly)):
        pdata2 = ly[i].find(sunny2)

        #报告期(数据起止日期)
        if pdata2 != -1:
            a.append(ly[i+1].lstrip().rstrip().strip())
        i += 1

    return a

def extradata(_tempdata):
    #
    alldata = readall(_tempdata)
    edata = psur_info(_tempdata)
    gdata = ghostdata(alldata)
    temp = edata+gdata
    return temp

def extradata2(_tempdata):
    #
    alldata = readall(_tempdata)
    gdata = ghostdata(alldata)
    return gdata

def extradata3(_tempdata):
    #
    edata = psur_info(_tempdata)
    return edata

def data2clean(temp):
    print len(temp)
    d0 = temp[0]

    d1 = temp[1]
    d2 = temp[2]
    if d1:
        pass
    else:
        d1 = "0000-00-00"
    if d2:
        pass
    else:
        d2 = "0000-00-00"

    d3 = temp[3]
    d4 = temp[4]
    d5 = temp[5]
    d6 = temp[6]
    d7 = temp[7]
    d8 = temp[8]
    d9= temp[9]
    d10 = temp[0]
    d11 = temp[11]

    return [d0,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11]

def data2clean2(temp):
    print len(temp)
    d0 = temp[0]
    d1 = temp[1]
    d2 = temp[2]
    if d1:
        pass
    else:
        d1 = "0000-00-00"
    if d2:
        pass
    else:
        d2 = "0000-00-00"
    d3 = temp[3]
    d4 = temp[4]
    d5 = temp[5]
    d6 = temp[6]
    d7 = temp[7]
    d8 = temp[8]
    d9= temp[9]
    d10 = temp[0]
    d11 = temp[11]
    return [d0,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11]

def write_Eval(sometest, showid, id):
    evalinfo = psur_eval_info(sometest)
    einfoid = len(evalinfo)

    if einfoid == 1:
        #eidata = evalinfo[0]
        #BackUp1
        eidata = [id, evalinfo[0], showid]
        pusr_eval_info = (
                "insert into pusr_eval_info (ReportID,BackUp1,BackUp2) "
                "value(%s,%s,%s)"
        )
        mdrsql.mdr_insert_alone(pusr_eval_info, eidata)
    else:
        n = 6
        dataout = [evalinfo[i:i+n] for i in range(0, len(evalinfo), n)]
        pusr_eval_info = (
                "insert into pusr_eval_info (ReportID,EvalUity,EvalValue,EvalInfo,EvalDate,Evalpeople,FileName,BackUp2) "
                "value(%s,%s,%s,%s,%s,%s,%s,%s)"
        )
        for dodata in dataout:
            eidata = [id, dodata[0], dodata[1],dodata[2],dodata[3],dodata[4],dodata[5],showid]
            mdrsql.mdr_insert_alone(pusr_eval_info, eidata)

def write_ChangeInfo(sometest, showid, id):
    evalinfo = psur_changelog_info(sometest)
    einfoid = len(evalinfo)

    if einfoid == 1:
        #eidata = evalinfo[0]
        #BackUp1
        eidata = [id, evalinfo[0], showid]
        pusr_eval_info = (
                "insert into pusr_changelog_info (ReportID,BackUp1,BackUp2) "
                "value(%s,%s,%s)"
        )
        mdrsql.mdr_insert_alone(pusr_eval_info, eidata)
    else:
        n = 6
        dataout = [evalinfo[i:i+n] for i in range(0, len(evalinfo), n)]
        pusr_eval_info = (
                "insert into pusr_changelog_info (ReportID,IteratorID,ChangePeopleName,ChangeType,ChangeDate,ChangeValue,ChangeOperator,BackUp2) "
                "value(%s,%s,%s,%s,%s,%s,%s,%s)"
        )
        for dodata in dataout:
            eidata = [id, dodata[0], dodata[1],dodata[2],dodata[3],dodata[4],dodata[5],showid]
            mdrsql.mdr_insert_alone(pusr_eval_info, eidata)

def write_DWF(sometest, showid, id):
    #dwf = bussness.psur_DWF_info(sometest)
    evalinfo = psur_DWF_info(sometest)
    einfoid = len(evalinfo)

    if einfoid == 1:
        #eidata = evalinfo[0]
        #BackUp1
        eidata = [id, evalinfo[0], showid]
        pusr_eval_info = (
                "insert into pusr_dwf_info (ReportID,BackUp1,BackUp2) "
                "value(%s,%s,%s)"
        )
        mdrsql.mdr_insert_alone(pusr_eval_info, eidata)
    else:
        n = 6
        dataout = [evalinfo[i:i+n] for i in range(0, len(evalinfo), n)]
        pusr_eval_info = (
                "insert into pusr_dwf_info (ReportID,IteratorID,FileName,FileType,FileInfo,UpLoadDate,UploadDepartmentName,BackUp2) "
                "value(%s,%s,%s,%s,%s,%s,%s,%s)"
        )
        for dodata in dataout:
            eidata = [id, dodata[0], dodata[1],dodata[2],dodata[3],dodata[4],dodata[5],showid]
            mdrsql.mdr_insert_alone(pusr_eval_info, eidata)


def get_report(id):
    #
    report_url = "http://www.adrs.org.cn/ADR/page/adrpage/psur/viewPsurReport.jsp?fdObjectId=%s&type=2" % id
    somedata = send_url2(report_url)
    return somedata