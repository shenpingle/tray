#-*- coding:utf-8 -*-
from utils import *
import mdrsql
from utils_psur import *
from mdrtime import *
#################################################################################################
#抽取报告数据
#20141011
#begining
#################################################################################################
#move on utils_psur.py
#################################################################################################
#抽取报告数据
#20141011
#ending
#################################################################################################

#################################################################################################
#向http://www.adrs.org.cn/ADR/ep/PSURService/PSURService/queryFileInfoForJSP发post请求，获取下载文件详细信息
#20141011
#begining
#################################################################################################
def download_fileinfo3(id,reportid):
    #写完临时数据，然后写到pusr_dwf_info，并返回下载文件所需要的参数
    url = u"http://www.adrs.org.cn/ADR/ep/PSURService/PSURService/queryFileInfoForJSP"
    jim = {"funcID":"123","userID":"admin","operations":[{"actionName":"query","count":1,"operationDatas":[{"objectID":id,"classid":"2401"}]}]}
    _searchdata = send_post_json_me(url, jim)
    _data = json.loads(_searchdata)

    DWF_id = _data['ResponseMessage']['operations'][0]['count']

    for i in range(0, DWF_id):
        #
        p0 = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][0]['v']
        p1 = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][1]['v']
        p2 = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][2]['v']
        p7 = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][7]['v']
        p8 = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][8]['v']
        p11 = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][11]['v']
        p12 = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][12]['v']
        p13 = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][13]['v']
        p16 = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][16]['v']

        data_pusr_dwf_info = [p0, p1, p2, p7, p8, p11, p12, p13, p16,reportid]
        pusr_dwf_info_sql = (
                "insert into pusr_dwfinfo_down (FileType,UploadDepartmentName,AttachmentFileType,FileName,UpLoadDate,FilePath,FileSize,FileID,ShowFileName,ReportID) "
                "value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        )
        mdrsql.mdr_insert_alone(pusr_dwf_info_sql, data_pusr_dwf_info)
#################################################################################################
#向http://www.adrs.org.cn/ADR/ep/PSURService/PSURService/queryFileInfoForJSP发post请求，获取下载文件详细信息
#20141011
#ending
#################################################################################################
def downallfiles3(id, psurobjid, filename, reportid):
    #
    url ="http://www.adrs.org.cn/ADR/cdrAttachment/attachmentDiskManager/"
    #id = "109913972074597010463482100000"
    #psurobjid = "243013972078880790070655100000"
    import random
    some = random.randrange(1000000000000000, 9999999999999999)
    boundary = '-----------------------------' + str(some)
    parts = []

    parts.append('--' + boundary)
    parts.append('Content-Disposition: form-data; name="action"')
    parts.append('')
    parts.append(str("download"))

    parts.append('--' + boundary)
    parts.append('Content-Disposition: form-data; name="id"')
    parts.append('')
    parts.append(id)

    parts.append('--' + boundary + '--')
    parts.append('')

    body = '\r\n'.join(parts)

    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'Host: www.adrs.org.cn',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection':  'keep-alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
        'Content-Type': 'multipart/form-data; boundary=%(boundary)s' % {"boundary": boundary},
        'Referer':'http://www.adrs.org.cn/ADR/page/adrpage/psur/viewPsurReport.jsp?fdObjectId=%(objid)s&type=2' % {"objid": psurobjid}
    }

    try:
        common_url = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(common_url, data=body, timeout=120)
        #print "response.info():",response.info()
        from cStringIO import StringIO
        from gzip import GzipFile
        data2 = GzipFile('', 'r', 0, StringIO(response.read())).read()
        response_data = data2
        # 定义要创建的目录
        import pathDlg
        mkpath = "c:\\mykill\\web\\"
        #mkpath = pathDlg.readini_path()
        path = mkdir(mkpath, psurobjid)
        name = path + "\\"+filename

        print name

        local_file = open(name, "wb")
        local_file.write(response_data)
        local_file.close()
    except (urllib2.HTTPError, urllib2.URLError, socket.error), exception:
        print u"下载出现错误，打印文件信息:",id, psurobjid, filename,reportid
        tempdata = (reportid, psurobjid, filename,id)
        insert_sql = (
                    "insert into pusr_dwfinfo_down_error(ReportID, FileID,ShowFileName BackUp1) "
                    "value(%s,%s,%s,%s,%s)"
                )
        mdrsql.mdr_insert_alone(insert_sql, tempdata)
        pass

def myautodown(id,reportid):
    #has_sql = "select ReportID from pusr_business where ReportID='%s'" % (REPORT_ID)
    down_sql = "SELECT FileID,ShowFileName FROM pusr_dwfinfo_down where ReportID='%s'" % (reportid)
    objlistid = mdrsql.mdr_select(down_sql)
    for objid in objlistid:
        downallfiles3(objid[0], id, objid[1],reportid)

def myautodown2():
    #has_sql = "select ReportID from pusr_business where ReportID='%s'" % (REPORT_ID)
    down_sql = "SELECT FileID,ShowFileName,BackUp,ReportID FROM pusr_dwfinfo_down_error"
    objlistid = mdrsql.mdr_select(down_sql)
    for objid in objlistid:
        downallfiles3(objid[0], objid[2], objid[1],objid[3])


#################################################################################################
#下载文件，写入指定路径下
#20141011
#ending
#################################################################################################
def PSUR_Report(_timedict):
    #
    t = _timedict
    t_start = t['beginTime']
    t_end = t['endTime']
    RF_list = gather_report_total(_timedict)
    for i in range(0, RF_list):
        meid = i*100
        print "meid:", meid
        jim = {"funcID":"QUERY_DATA","userID":78919,"operations":[{"actionName":"query","operationDatas":[{"ENTRY_START_DATE_2401":t_start,"ENTRY_END_DATE_2401":t_end,"ACTIVE_CONSTITUENT_2430":"","TRADENAME_CN_2431":"","DRUGNAME_CN_FORM_2431":"","DOSEFORM_2431":"","DRUG_STATUS_2431":"","APPROVAL_NO_2431":"","REPORT_ID_2430":"","PICKER_UNIT_NAME_2430":"","START_APPLY_DATE_2430":"","END_APPLY_DATE_2430":"","listid":"2430_1","start":meid,"limit":100}]}]}
        #查询结果列表
        try:
            _searchdata = send_post_json_me(Psur_url, jim)
            _data = json.loads(_searchdata)
            #print 'json:', _data
            searchdataid = _data['ResponseMessage']['operations'][0]['count']
            for i in range(0, searchdataid):

                PICKER_UNIT_ADDR = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][0]['v']
                REPORT_DATE = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][2]['v']
                PICKER_UNIT_FAX = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][3]['v']
                PICKER_UNIT_TEL = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][6]['v']
                DRUG_TYPE_NAME = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][7]['v']

                ACTIVE_CONSTITUENT = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][10]['v']
                OBJ_ID = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][13]['v']
                INTERNATION_BEGIN_DATE = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][15]['v']
                PSUR_CONCLUSION = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][17]['v']
                PROD_SOURCE_2430_SHOW = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][18]['v']
                ENTRY_DATE = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][19]['v']


                PROD_DESC = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][21]['v']
                INDICATIONS = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][25]['v']
                PICKER_UNIT_LINKMAN = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][26]['v']
                PICKER_UNIT_NAME = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][28]['v']
                PICKER_UNIT_EMAIL = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][29]['v']
                PICKER_UNIT_DEPT = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][31]['v']
                PICKER_SIGN = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][32]['v']

                PICKER_UNIT_POST = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][34]['v']
                DATA_END_DATE = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][35]['v']
                REPORT_ID = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][36]['v']
                DRUGNAME_CN_FORM = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][38]['v']
                DATA_START_DATE = _data['ResponseMessage']['operations'][0]['operationDatas'][i]['es'][40]['v']

                tempdata = (
                    REPORT_ID,
                    #36,报告编码
                    DRUG_TYPE_NAME,
                    #7,药品分类
                    ACTIVE_CONSTITUENT,
                    #10,活性成分
                    PROD_SOURCE_2430_SHOW,
                    #18,国产/进口
                    DRUGNAME_CN_FORM,
                    #38,通用名称
                    DATA_START_DATE,
                    #41,数据起日期
                    DATA_END_DATE,
                    #35,数据止日期
                    PICKER_UNIT_NAME,
                    #28,报告单位名称
                    ENTRY_DATE,
                    #19,国家中心接收时间
                    OBJ_ID
                    #13
                )
                #新添加：
                #1.判断已存在，则不再添加
                #2.为了解决下载error中的数据，添加标识
                has_sql = "select ReportID from pusr_business where ReportID='%s'" % (REPORT_ID)
                hasset = mdrsql.mdr_select(has_sql)
                if hasset:
                    #print hasset
                    print u"已存在此报告编码：",REPORT_ID
                    continue
                else:
                    #ReportID, DrugType, CFZC, Classify, TYMC, Start_Date, End_Date, FactoryName, StateReportDate, BackUp1
                    #查询数据写入
                    print "ENTRY_DATE:",ENTRY_DATE
                    insert_sql = (
                        "insert into pusr_query (ReportID, DrugType, CFZC, Classify, TYMC, Start_Date, End_Date, FactoryName, StateReportDate, BackUp1) "
                        "value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    )
                    mdrsql.mdr_insert_alone(insert_sql, tempdata)

                    #{
                    ylname = None
                    code = None
                    myname = None
                    ylycn = None
                    ymcn_sql = "select distinct ylname,code,myname,ylycn from ym where ymcn='%s'" % (DRUGNAME_CN_FORM)
                    ymcndataset = mdrsql.mdr_select(ymcn_sql)
                    if ymcndataset:
                        for ymcndata in ymcndataset:
                            ylname = ymcndata[0]
                            code = ymcndata[1]
                            myname = ymcndata[2]
                            ylycn = ymcndata[3]
                    else:
                            ylname = ""
                            code = ""
                            myname = ""
                            ylycn = ""
                    #}
                    pname =None
                    dtypeID = None

                    localdata_sql = "select distinct ProvinceName,DistrictTypeID from unit where Name='%s'" % (PICKER_UNIT_NAME)

                    localdataset = mdrsql.mdr_select(localdata_sql)
                    if localdataset:
                        for localdata in localdataset:
                            pname = localdata[0]
                            dtypeID = localdata[1]

                    else:
                            pname = ""
                            dtypeID = ""
                    yao_data = [ylname, code, myname, ylycn]
                    boss_add_data = [pname, dtypeID]
                    #主表信息写入
                    reportdata =[
                        #
                        #报告表编码 	36
                        REPORT_ID,
                        #国际诞生日   15
                        INTERNATION_BEGIN_DATE,
                        #活性成分(处方组成) 10
                        ACTIVE_CONSTITUENT,
                        #药品分类	7
                        DRUG_TYPE_NAME,
                        #国产/进口 18
                        PROD_SOURCE_2430_SHOW,
                        #适应症(功能主治) 25
                        INDICATIONS,
                        #产品情况说明 21
                        PROD_DESC,
                        #本期报告结论 17
                        PSUR_CONCLUSION,
                        #报告人 32
                        PICKER_SIGN,
                        #报告日期 2
                        REPORT_DATE,
                        #报告单位名称 28
                        PICKER_UNIT_NAME,
                        #传真 3
                        PICKER_UNIT_FAX,
                        #报告单位地址 0
                        PICKER_UNIT_ADDR,
                        #邮政编码 34
                        PICKER_UNIT_POST,
                        #负责部门 31
                        PICKER_UNIT_DEPT,
                        #联系电话 6
                        PICKER_UNIT_TEL,
                        #联系人26
                        PICKER_UNIT_LINKMAN,
                        #电子邮件 29
                        PICKER_UNIT_EMAIL,
                        #国家中心接收时间 19
                        ENTRY_DATE
                    ]
                    #主表信息更新
                    somedata = get_report(OBJ_ID)
                    #print u"额外数据解析,即返回整个文本",somedata
                    #extrareportdata = data2clean(extradata(somedata))
                    extrareportdata = extradata2(somedata)

                    dataall = reportdata + extrareportdata + boss_add_data

                    #报告表编码 	36
                    #REPORT_ID,INTERNATION_BEGIN_DATE,ACTIVE_CONSTITUENT,DRUG_TYPE_NAME,PROD_SOURCE_2430_SHOW,INDICATIONS,PROD_DESC,PSUR_CONCLUSION,PICKER_SIGN,REPORT_DATE,PICKER_UNIT_NAME,PICKER_UNIT_FAX,PICKER_UNIT_ADDR, PICKER_UNIT_POST,PICKER_UNIT_DEPT,PICKER_UNIT_TEL,PICKER_UNIT_LINKMAN,PICKER_UNIT_EMAIL,ENTRY_DATE
                    insert_report = (
                        "insert into pusr_business (REPORTID,INTERNATION_BEGIN_DATE,ACTIVE_CONSTITUEN,DRUG_TYPE_NAME,PROD_SOURCE,INDICATIONS,PROD_DESC,PSUR_CONCLUSION,PICKER_SIGN,REPORT_DATE,PICKER_UNIT_NAME,PICKER_UNIT_FAX,PICKER_UNIT_ADDR, PICKER_UNIT_POST,PICKER_UNIT_DEPT,PICKER_UNIT_TEL,PICKER_UNIT_LINKMAN,PICKER_UNIT_EMAIL,ENTRY_DATE,BGQ,ProvinceName,District) "
                        "value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    )
                    mdrsql.mdr_insert_alone(insert_report, dataall)
                    print REPORT_ID
                    #psur业务主表批准文号部分11字段1-N数据表
                    extrainfo = extradata3(somedata)
                    n=11
                    dataout = [extrainfo[i:i+n] for i in range(0, len(extrainfo), n)]
                    for temp in dataout:
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
                        d10 = temp[10]
                        extraalldata = [REPORT_ID,d0,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10]
                        exdata = extraalldata + yao_data
                        insert_report_extra = (
                            "insert into pusr_business_extradata (REPORTID,RegisterID,RegisterTime,FirstRegisterTime,TYMC,SPMC,DrugMState,GG,JX,BQSC,BQXL,CountUser,ylname,code,myname,ylycn) "
                            "value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        )
                        mdrsql.mdr_insert_alone(insert_report_extra, exdata)
                    #评价信息读取
                    write_Eval(somedata, OBJ_ID, REPORT_ID)

                    #修改信息读取
                    write_ChangeInfo(somedata, OBJ_ID, REPORT_ID)

                    #显示附件信息读取
                    write_DWF(somedata, OBJ_ID, REPORT_ID)

                    #下载文件信息写入
                    download_fileinfo3(OBJ_ID,REPORT_ID)

                    #附件下载
                    """
                    if Tag:
                        myautodown(OBJ_ID,REPORT_ID)
                    else:
                        pass
                    """
                    myautodown(OBJ_ID,REPORT_ID)

            time.sleep(0.001)
        except (IndexError, KeyError, ValueError), exception:
            print "Main:",exception
            print "main:",_searchdata
        #pass

    print u"本次下载任务已经结束"

def autopsur(start,end):
    #def PSUR_Report(_timedict):
    PSUR_Report(anytime2(start, end))

if __name__ == '__main__':
    print "test ..."

    print u"开始下载"
    import mdrtime
    PSUR_Report(mdrtime.anytime())