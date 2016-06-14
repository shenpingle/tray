#-*- coding:utf-8 -*-

import utils
from config import *
import codecs
import time
import os
from deletedance import dodelete
import mdrsql
import simplejson as json
import urllib

def mdr_import_report(qrow):
    '''
    抓取指定的记录
    '''
    smdrReportViewHtml = None
    is_icd = None
    icd_setdata = None

    viewId          = qrow['ViewID']
    ValueState      = qrow['ValueState']        #评价状态
    backState       = qrow['BackState']         #退回状态
    StateReportDate = qrow['ReceiveDate']       #接收日期
    AddSource       = qrow['AddSource']         #补充材料
    ReportID        = qrow['ReportID'].strip()  #报告id
    ReportUnitName  = qrow['ReportUnitName']    #报告单位名称
    SendDate        = qrow['SendDate']          #上报日期

    ReportID          = utils.unicode_to_str(ReportID.strip())
    ReportUnitName    = utils.str_to_unicode(ReportUnitName)

    print u"报告编码(MDR):", ReportID

    appraise_status = 0  #评价状态       
    if ValueState:
        appraise_status = 1
    #退回状态
    elif backState:
        appraise_status = 2

    mdr_data = mdr_get_report_data(viewId, ReportID, SendDate)
    
    qg_info = utils.getsmdrfda(viewId, ReportID, SendDate)

    sh_info = utils.getSmdrWhoArt(ReportID, SendDate, viewId)

    # 获取报告单位所在行政区信息
    (County,District,ProvinceName) = utils.getReportUnitDistrictInfo(ReportUnitName)
    mdr_data["County"] = County
    mdr_data["District"] = District
    mdr_data["ProvinceName"] = ProvinceName

    mdr_data["ReportUnitName"] = ReportUnitName
    mdr_data["BianMa"] = ReportID
    mdr_data["StateReportDate"] = StateReportDate
    
    #获取报告状态
    report_status = utils.getReportStatus(ReportID, viewId, SendDate)
    IsNotifyGov_value =     u'已通知药监部门' if u'已通知药监部门' in report_status else ''
    IsNotifyFactory_value = u'已通知生产企业' if u'已通知生产企业' in report_status else ''
    IsNotifyUnit_value =    u'已通知使用单位' if u'已通知使用单位' in report_status else ''
    IsNotifyShop_value =    u'已通知经营企业' if u'已通知经营企业' in report_status else ''
    State = u','.join(report_status)
    mdr_data["State"] = State

    icd_ok = mdr_data["icd_ok"]
    if len(icd_ok) != 0:
        (is_icd, UnMatchAffect,icd_setdata) = get_icd_info(mdr_data, icd_ok)


    # #获取器械基础信息
    # (UnMatchDevice,IsMatchingDevice,deviceInfo) =  utils.getDeviceInstrumentInfo(mdr_data["DeviceStandard"])
    # mdr_data["UnMatchDevice"] = UnMatchDevice
    # mdr_data["IsMatchingDevice"] = IsMatchingDevice


    IsMatchingFault = None
    IsADRorAccident_tag = None
    qg_setdata = None
    if qg_info:
        (IsMatchingFault, IsADRorAccident_tag, qg_setdata, sanlei) = mdr_falt_business(qg_info, mdr_data["DeviceStandard"])
    else:
        IsMatchingFault = '否'

    is_adr = None
    adr_data_list = None
    if sh_info:
        (is_adr, adr_data_list, IsADRorAccident_tag) = get_sh_info(sh_info,mdr_data)
    else:
        is_adr = u'否'

    if qg_info and sh_info:
        IsADRorAccident_tag = "3"
    else:
        IsADRorAccident_tag = "4"

    mdr_Home_1 = 'http://www.adrs.org.cn/MDR/scripts/mdr/smdr/smdReportView.jsp'

    querydata_1 = {
                "action"        :   "update",
                "FD_OBJECTID"   :   viewId,
                "UNIT_NAME"     :   utils.unicode_to_str(ReportUnitName),
                "start"         :   "1",
                "limit"         :   "10"
            }
    smdrReportViewHtml = utils.send_post(mdr_Home_1, urllib.urlencode( querydata_1))

    if not backState and smdrReportViewHtml:
        #获取关联性评价信息
        utils.mdr_get_smd_appraise(smdrReportViewHtml, ReportID, viewId, ReportUnitName,mdr_data["ReportDate"])

    #获取器械基础信息
    (UnMatchDevice,IsMatchingDevice,deviceInfo) =  utils.getDeviceInstrumentInfo(mdr_data["DeviceStandard"])
    mdr_data["UnMatchDevice"] = UnMatchDevice
    mdr_data["IsMatchingDevice"] = IsMatchingDevice
    
    
    if mdr_data["company_name"] :
        #存在，先去查询GMP
        (IsMatchingFactory,UnMatchFactory) = import_GMP_Info(mdr_data,mdr_data["company_name"] ,deviceInfo)
        mdr_data["IsMatchingFactory"] = IsMatchingFactory
        mdr_data["UnMatchFactory"] = UnMatchFactory

    d_tag = ""
    main_data = [
        mdr_data["BianMa"], mdr_data["ProvinceName"], mdr_data["District"], mdr_data["County"],
        mdr_data["ReportUnitName"], mdr_data["ReportUnitAddress"], mdr_data["ReportUnitTel"], mdr_data["Postalcode"], 
        mdr_data["UnitType"], mdr_data["HappenDate"], mdr_data["KnowDate"], mdr_data["ReportDate"], 
        mdr_data["ReportDate"], mdr_data["StateReportDate"], mdr_data["State"], mdr_data["patient_name"], 
        mdr_data["patient_gender"], mdr_data["patient_birthday"], mdr_data["patient_age"], mdr_data["age_class"], 
        mdr_data["patient_telephone"], mdr_data["event_memo"], mdr_data["event_consequence"], mdr_data["death_time"], 
        appraise_status, d_tag, IsNotifyGov_value, IsNotifyFactory_value, 
        IsNotifyUnit_value, IsNotifyShop_value, IsMatchingDevice, UnMatchDevice, 
        is_icd, icd_setdata, IsMatchingFault, qg_setdata, 
        None, is_adr, adr_data_list
    ]

    #信息插入
    main_sql = (
        u"""replace into mdr_business_gather(
        BianMa,ProvinceName,District,County, ReportUnitName, ReportUnitAddress,ReportUnitTel,Postalcode,UnitType,HappenDate,KnowDate,ReportDate,AcceptDate,StateReportDate,State,SuffererName,Sex,Birthday,Age,SuffererType,TelePhone,DepictDispose,Events,DeathDate,ReportInfo,DumplicateData, IsnotifyGov, IsnotifyFactory, IsnotifyUnit, IsnotifyShop,IsDeviceMatch,DeviceList,IsICDMatch,ICDList,IsFaultMatch,FaultList,IsADRorAccident,IsADRMatch,ADRList)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    )
    
    mdrsql.mdr_insert_alone(main_sql, main_data)
    
    #D.关联性评价 ,一定要在insert主表之后执行
    if smdrReportViewHtml :
        utils.get_smd_report(smdrReportViewHtml, ReportID, viewId,ReportUnitName,mdr_data["reporter"],mdr_data["reporter_class"],mdr_data["ReportDate"])

    #print u"本次下载任务已经结束"

    if qg_setdata:
        if len(sanlei) > 2:
            qg_data = (
                mdr_data["BianMa"], mdr_data["ProvinceName"], mdr_data["District"], mdr_data["County"],
                mdr_data["ReportUnitName"], mdr_data["ReportUnitAddress"], mdr_data["ReportUnitTel"], mdr_data["Postalcode"],
                mdr_data["UnitType"], mdr_data["HappenDate"], mdr_data["KnowDate"], mdr_data["ReportDate"],
                mdr_data["ReportDate"], mdr_data["StateReportDate"], mdr_data["State"], IsMatchingFault,
                qg_setdata, sanlei[2], sanlei[1], sanlei[0], None)

            qg_sql = (
                    "replace into mdr_faultbusiness(BianMa,ProvinceName,District,County,ReportUnitName,ReportUnitAddress,"
                    "ReportUnitTel,Postalcode,UnitType,HappenDate,KnowDate,ReportDate,AcceptDate,StateReportDate,State,"
                    "IsMatchingFault,StandardFaultName,Name,SubName,SuperClassName,NonName)"
                    "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            )
            mdrsql.mdr_insert_alone(qg_sql, qg_data)

        else:
            qg_data = (
                mdr_data["BianMa"], mdr_data["ProvinceName"], mdr_data["District"], mdr_data["County"],
                mdr_data["ReportUnitName"], mdr_data["ReportUnitAddress"], mdr_data["ReportUnitTel"], mdr_data["Postalcode"],
                mdr_data["UnitType"], mdr_data["HappenDate"], mdr_data["KnowDate"], mdr_data["ReportDate"],
                mdr_data["ReportDate"], mdr_data["StateReportDate"], mdr_data["State"], IsMatchingFault,
                qg_setdata, None, None, None, sanlei[0])

            qg_sql = (
                    "replace into mdr_faultbusiness(BianMa,ProvinceName,District,County,ReportUnitName,ReportUnitAddress,"
                    "ReportUnitTel,Postalcode,UnitType,HappenDate,KnowDate,ReportDate,AcceptDate,StateReportDate,State,"
                    "IsMatchingFault,StandardFaultName,Name,SubName,SuperClassName,NonName)"
                    "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            )
            mdrsql.mdr_insert_alone(qg_sql, qg_data)


def import_GMP_Info(data,company_name,deviceInfo):

    device_sql = "SELECT manufacturer_name_cn,province,city,district FROM `mdr_gmp` where manufacturer_name_cn='%s'  limit 1" % ( company_name )
    
    rows_device = mdrsql.mdr_select(device_sql)
    if rows_device:
        IsMatchingFactory = u'是'
        UnMatchFactory = ""
        rows_device_gmp = rows_device[0]
        
        StandardFactory = rows_device_gmp[0]
        manufacturerProvinceName = rows_device_gmp[1]
        manufacturerCity = rows_device_gmp[2]
        manufacturerCounty = rows_device_gmp[3]
    else:
        IsMatchingFactory = u'否'
        UnMatchFactory = company_name
        
        StandardFactory = ""
        manufacturerProvinceName = ""
        manufacturerCity = ""
        manufacturerCounty = ""

    device_sql = (
		    """
            replace into mdr_devicebusiness(
                BianMa, ProvinceName, District, County, ReportUnitName, 
                ReportUnitAddress,ReportUnitTel,Postalcode,UnitType,
                HappenDate,KnowDate,ReportDate,AcceptDate,StateReportDate,
                State,CertificateNumber,TradeName,classification,firstreason,
                firstdone,useplace,specifications,Productnumber,Batchnumber,
                operator,ImplantationDate,StopDate,EffectiveDate,
                manufacturer_address,manufacturer_tel,IsMatchingDevice,DeviceStandard,
                PName,SubName,Name,manageclass,classcode,
                UnMatchDevice, IsMatchingFactory, StandardFactory,manufacturerProvinceName,
                manufacturerCity, manufacturerCounty,UnMatchFactory) 
                
                values
                
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	    )

    device_data = [
                data["BianMa"], data["ProvinceName"], data["District"], data["County"],
                data["ReportUnitName"], data["ReportUnitAddress"], data["ReportUnitTel"], data["Postalcode"], 
                data["UnitType"], data["HappenDate"], data["KnowDate"], data["ReportDate"], 
                data["ReportDate"], data["StateReportDate"], data["State"], data["CertificateNumber"], 
                data["TradeName"], data["classification"], data["firstreason"], data["firstdone"], 
                data["useplace"], data["specifications"], data["Productnumber"], data["Batchnumber"], 
                data["operator"], data["ImplantationDate"], data["StopDate"], data["EffectiveDate"], 
                data["manufacturer_address"], data["manufacturer_tel"], data["IsMatchingDevice"], data["DeviceStandard"], 
                deviceInfo["SuperClassName"], deviceInfo["subname"], data["DeviceStandard"], deviceInfo["manageclass"], 
                deviceInfo["classcode"], data["UnMatchDevice"], IsMatchingFactory, StandardFactory, 
                manufacturerProvinceName, manufacturerCity, manufacturerCounty, UnMatchFactory]
    mdrsql.mdr_insert_alone(device_sql, device_data)

    return (IsMatchingFactory,UnMatchFactory)
    
def get_icd_info(data,icd_ok):
    icd_standname = ""
    icd_set = []
    IsMatchingAffect = None
    UnMatchAffect = None
    icd_setdata = None
    _un_tag_icd_1 = utils.str_to_unicode("[非标准:")
    _un_tag_icd_2 = utils.str_to_unicode("]")
    for item in icd_ok:
        #_item = item.strip(_trim_tag).strip()
        icd_sql = (
            "SELECT StandardIcdName,icd_a_name,icd_b_name,icd_c_name,PathName FROM `mdr_icd` where StandardIcdName='%s'  limit 1" %(item)
        )

        rows_icd = mdrsql.mdr_select(icd_sql)
        if rows_icd:
            IsMatchingAffect = u'是'
            UnMatchAffect = ""
            for icd_ok_info in rows_icd:
                icd_a_name = icd_ok_info[0]
                icd_b_name = icd_ok_info[1]
                AffectStandardName = icd_ok_info[2]
                PathName = icd_ok_info[3]

            icd_set.append(item)
            icd_setdata = item
            icd_standname = AffectStandardName
        else:
            IsMatchingAffect = u'否'
            un_icd_info = _un_tag_icd_1+item+_un_tag_icd_2
            _un_icd_info = utils.str_to_unicode(un_icd_info)
            UnMatchAffect = _un_icd_info
            icd_a_name = ""
            icd_b_name = ""
            AffectStandardName = ""
            PathName = ""
            icd_standname = AffectStandardName

            icd_set.append(UnMatchAffect)
            icd_setdata = utils.data_set(icd_set)
    
    icd_sql = (
        "replace into mdr_icdbusiness(BianMa,ProvinceName,District,County,ReportUnitName,ReportUnitAddress,ReportUnitTel,Postalcode,UnitType ,HappenDate,KnowDate,ReportDate,AcceptDate,StateReportDate,State,IsMatchingAffect,AffectStandardName,icd_a_name,icd_b_name,icd_c_name,PathName,UnMatchAffect)"
        "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    
    icd_data = [
        data["BianMa"], data["ProvinceName"], data["District"], data["County"],
        data["ReportUnitName"], data["ReportUnitAddress"], data["ReportUnitTel"], data["Postalcode"], 
        data["UnitType"], data["HappenDate"], data["KnowDate"], data["ReportDate"], 
        data["ReportDate"], data["StateReportDate"], data["State"],IsMatchingAffect, 
        AffectStandardName, icd_a_name, icd_b_name, AffectStandardName, 
        PathName, UnMatchAffect]
    mdrsql.mdr_insert_alone(icd_sql, icd_data)
    
    return (IsMatchingAffect, UnMatchAffect,icd_setdata)


def mdr_falt_business(qg_info, name):
    qg_set = []
    sanlei = []
    IsMatchingFault = None
    IsADRorAccident_tag = None
    for SuperFaultName in qg_info:
        qg_sql = (
            "SELECT SuperClassName,subname FROM `mdr_deviceinstrument` where Name='%s'  limit 1" % name
        )
        rows_qg = mdrsql.mdr_select(qg_sql)
        if rows_qg:
            IsMatchingFault = u'是'
            for row_qg_data in rows_qg:
                s_name_1 = row_qg_data[0]
                s_name_2 = row_qg_data[1]
                compose_data = s_name_1+':'+s_name_2+':'+name
            accident_sql = (
                "replace into mdr_fault(SuperClassName,SubName,Name,NonStandardName,IsDeviceMatching,RealFaultName) "
                "values(%s,%s,%s,%s,%s,%s)"
            )
            accident_data = (s_name_1, s_name_2, name, None, u'是', SuperFaultName)
            mdrsql.mdr_insert_alone(accident_sql, accident_data)
            
            qg_set.append(SuperFaultName)
            qg_setdata = utils.data_set(qg_set)
            UnMatchFault = ""
            IsADRorAccident_tag = "2"
            sanlei.append(s_name_1)
            sanlei.append(s_name_2)
            sanlei.append(name)
            
        else:
            accident_sql = (
                "replace into mdr_fault(SuperClassName,SubName,Name,NonStandardName,IsDeviceMatching,RealFaultName) "
                "values(%s,%s,%s,%s,%s,%s)"
            )
            accident_data = (None, None, None, name, u'否', SuperFaultName)
            mdrsql.mdr_insert_alone(accident_sql, accident_data)
            IsMatchingFault = u'是'
            UnMatchFault = utils.str_to_unicode(SuperFaultName)
            qg_set.append(UnMatchFault)
            qg_setdata = utils.data_set(qg_set)
            sanlei.append(name)
            
        # qg_data = (
        #     data["BianMa"], data["ProvinceName"], data["District"], data["County"],
        #     data["ReportUnitName"], data["ReportUnitAddress"], data["ReportUnitTel"], data["Postalcode"],
        #     data["UnitType"], data["HappenDate"], data["KnowDate"], data["ReportDate"],
        #     data["ReportDate"], data["StateReportDate"], data["State"],StandardFault,
        #     StandardFault, IsMatchingFault, SuperFaultName, UnMatchFault)
        # qg_sql = (
        #         "replace into mdr_faultbusiness(BianMa,ProvinceName,District,County,ReportUnitName,ReportUnitAddress,ReportUnitTel,Postalcode,UnitType ,HappenDate,KnowDate,ReportDate,AcceptDate,StateReportDate,State,StandardFault,Name,IsMatchingFault,SuperFaultName,UnMatchFault)"
        #         "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # )
        # mdrsql.mdr_insert_alone(qg_sql, qg_data)

    return (IsMatchingFault, IsADRorAccident_tag, qg_setdata, sanlei)


def get_sh_info(sh_info, data):
    sh_set = []
    is_adr = None
    clinicdetail_Name = None
    clinicdetail_SubID = None
    clinicsub_ID = None
    clinicsub_Name = None
    clinic_ID = None
    clinic_NAME = None
    IsADRorAccident_tag = ""
    
    for sh_info_item in sh_info:
        sh_query_sql = "SELECT clinicdetail.SubID, clinicdetail.Name,clinicsub.ID,clinicsub.Name,clinic.ID,clinic.NAME FROM clinicdetail, clinicsub,clinic WHERE clinicdetail.SubID=clinicsub.ID and clinicsub.PID=clinic.ID and clinicdetail.Name= '%s'  limit 1" %(sh_info_item)
        rows_sh = mdrsql.mdr_select(sh_query_sql)
        if rows_sh:
            is_adr = u'是'
            for row_sh_data in rows_sh:
                #sh_s_name = row_sh_data[0]
                clinicdetail_Name = row_sh_data[1]
                clinicdetail_SubID = row_sh_data[0]
                clinicsub_ID = row_sh_data[2]
                clinicsub_Name = row_sh_data[3]
                clinic_ID = row_sh_data[4]
                clinic_NAME = row_sh_data[5]

            sh_set.append(sh_info_item)
            adr_data_list = sh_info_item
            IsADRorAccident_tag = "1"
            _un_sh_info = ""
        else:
            is_adr = u'否'
            _un_sh_info = u"[非标准:" + sh_info_item + u"]"
            sh_set.append(_un_sh_info)
            adr_data_list = utils.data_set(sh_set)
            #sh_s_name = ""
            clinicdetail_Name = ""
            clinicdetail_SubID = ""
            clinicsub_ID = ""
            clinicsub_Name = ""
            clinic_ID = ""
            clinic_NAME = ""
            
    sh_data =     [
        data["BianMa"], data["ProvinceName"], data["District"], data["County"],
        data["ReportUnitName"], data["ReportUnitAddress"], data["ReportUnitTel"], data["Postalcode"], 
        data["UnitType"], data["HappenDate"], data["KnowDate"], data["ReportDate"], 
        data["ReportDate"], data["StateReportDate"], data["State"], is_adr, 
        clinicdetail_Name, clinicdetail_Name, clinicdetail_SubID, clinicsub_ID, 
        clinicsub_Name, clinic_ID, clinic_NAME, _un_sh_info]

    sh_sql = (
        "replace into mdr_adrbusiness(BianMa,ProvinceName,District,County,ReportUnitName,ReportUnitAddress,ReportUnitTel,Postalcode,UnitType ,HappenDate,KnowDate,ReportDate,AcceptDate,StateReportDate,State,IsMatchingADR,ADRStandardID,Name,SID1,SubID,SubName,PID,PName,UnMatchADR)"
        "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    mdrsql.mdr_insert_alone(sh_sql, sh_data)
    
    return (is_adr, adr_data_list,IsADRorAccident_tag)

    
def mdr_get_report_data(obj_id,BianMa,send_date):
    data = {}
    
    mdr_Home_1_report = 'http://www.adrs.org.cn/MDR/ep/smdrFindList/FindListSmdReportService/getSmdReport'
    querydata_1_report = 'params={"funcID":"MDR_SMDR_BROWSE_00","userID":608575,"operations":[{"actionName":"query","count":1,"operationDatas":[{"FD_OBJECTID":"%s","action":"update"}]}]}' % obj_id
    report_data_full = utils.mdr_send_post(mdr_Home_1_report, querydata_1_report, 1, BianMa, send_date)
    
    try:
        _report_all = json.loads(report_data_full)
    except Exception,err:
        print 'report_id:',BianMa,u'getSmdReport 调用失败 or 解析失败！'

    esData = _report_all['ResponseMessage']['operations'][0]['operationDatas'][0]['es']
          
    icd_321 = esData[64]['v']

    if not isinstance(icd_321,str) and not isinstance(icd_321,unicode):
        icd_ok = utils.mdr_slice(str(icd_321))
    else:
        icd_ok = utils.mdr_slice(icd_321)
        
    data["icd_ok"] = icd_ok
    
    #报告来源
    _report_data_1 = esData[2]['v']
    data["UnitType"] = utils.data_check_type(utils.bgly(_report_data_1))    
    
    #联系地址
    data["ReportUnitAddress"] = utils.data_check_type(esData[6]['v'])
    #报告日期
    data["ReportDate"]= utils.data_check_type(esData[3]['v'])

    #联系电话
    data["ReportUnitTel"] = utils.data_check_type(esData[7]['v'])
    #邮编
    data["Postalcode"]= utils.data_check_type(esData[8]['v'])
    #---------------------------------------------------------------------------------------------------------------
    #注册证号
    data["CertificateNumber"] = utils.data_check_type(esData[25]['v'])

    #产品名称
    data["DeviceStandard"] = utils.data_check_type(esData[27]['v'])

    #商品名称
    data["TradeName"] = utils.data_check_type(esData[29]['v'])

    #产品分类
    data["classification"] = utils.data_check_type(esData[23]['v'])

    #生产企业名称
    data["company_name"] = utils.data_check_type(esData[35]['v'])

    #生产企业地址
    data["manufacturer_address"] = utils.data_check_type(esData[36]['v'])

    #联系电话
    data["manufacturer_tel"] = utils.data_check_type(esData[37]['v'])

    #型号规格
    data["specifications"] = utils.data_check_type(esData[30]['v'])

    #产品编号
    data["Productnumber"] = utils.data_check_type(esData[31]['v'])

    #产品批号
    data["Batchnumber"] = utils.data_check_type(esData[32]['v'])
    #操 作 人
    _report_data_18 = esData[38]['v']
    data["operator"] = utils.data_check_type(utils.type_op(_report_data_18))

    #有效期至
    data["EffectiveDate"] = utils.data_check_type(esData[39]['v'])
    #生产日期
    data["production_date"] = utils.data_check_type(esData[40]['v'])
    #停用日期
    data["StopDate"] = utils.data_check_type(esData[41]['v'])
    #植入日期
    data["ImplantationDate"] = utils.data_check_type(esData[42]['v'])
    #事件发生初步原因分析
    data["firstreason"] = utils.data_check_type(esData[43]['v'])
    #事件初步处理情况
    data["firstdone"] = utils.data_check_type(esData[44]['v'])

    #事件报告状态
    #---------------------------------------------------------------------------------------------------------------
    #姓　　名
    data["patient_name"] = utils.data_check_type(esData[9]['v'])
    #年　　龄
    data["patient_age"] = utils.data_check_type(esData[11]['v'])
    #出生日期
    data["patient_birthday"] = utils.data_check_type(esData[10]['v'])
    #性　　别
    _report_data_29 = esData[13]['v']
    data["patient_gender"] = utils.data_check_type(utils.sex(_report_data_29))
    #电　　话
    data["patient_telephone"] = utils.data_check_type(esData[14]['v'])
    #icd
    #   icd_ok
    #---------------------------------------------------------------------------------------------------------------
    #事件发生日期
    data["HappenDate"] = utils.data_check_type(esData[15]['v'])

    #发现或知悉日期
    data["KnowDate"] = utils.data_check_type(esData[16]['v'])

    #医疗器械实际使用场所
    _report_data_33 = esData[17]['v']
    data["useplace"] = utils.data_check_type(utils.use(_report_data_33))

    #事件后果
    _report_data_34 = esData[19]['v']
    data["event_consequence"] = utils.data_check_type(utils.event(_report_data_34))

    #事件陈述
    data["event_memo"] = utils.data_check_type(esData[21]['v'])
    #---------------------------------------------------------------------------------------------------------------
    #报告人类别
    _report_data_36 = esData[45]['v']
    data["reporter_class"] = utils.data_check_type(utils.type_report(_report_data_36))
    #报告人
    data["reporter"] = utils.data_check_type(esData[46]['v'])
    #---------------------------------------------------------------------------------------------------------------
    #死亡时间
    data["death_time"] = utils.data_check_type(esData[20]['v'])
    
    
    if not data["death_time"]:
        data["death_time"] = '0000-00-00'

    if not data["HappenDate"]:
        data["HappenDate"] = '0000-00-00'

    if not data["KnowDate"]:
        data["KnowDate"] = '0000-00-00'

    _year = utils.my_today[0:4]
    if data["patient_age"]:
        pass
    else:
        if data["patient_birthday"]:
            data["patient_age"] = utils.str_to_unicode(str(int(_year)-int(data["patient_birthday"][0:4])))
        else:
            data["patient_age"] = ''
    if data["patient_birthday"]:
        pass
    else:
        data["patient_birthday"] = '0000-00-00'

    if not data["EffectiveDate"]:
        data["EffectiveDate"] = '0000-00-00'

    if not data["production_date"]:
        data["production_date"] = '0000-00-00'

    if not data["StopDate"]:
        data["StopDate"] = '0000-00-00'

    if not data["ImplantationDate"]:
        data["ImplantationDate"] = '0000-00-00'

    data["age_class"] = utils.age_check(data["patient_age"])
    
    return data
