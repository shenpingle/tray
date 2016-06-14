# coding:utf-8
import mdrsql
import utils
from login2 import login
import simplejson as json
from utils import mdr_send_post
from utils import mdr_slice

bianma = ''
sned_date = ''
# obj_id = 'fb123ef8-eb81-4ec6-b5bc-c791855d0419'
# obj_id = '064a88ff-a4a5-4de9-abfa-017dcd08c019'
obj_id = '064a88ff-a4a5-4de9-abfa-017dcd08c019'

def mdr_get_report_data(obj_id, BianMa, send_date):
    data = {}

    mdr_Home_1_report = 'http://www.adrs.org.cn/MDR/ep/smdrFindList/FindListSmdReportService/getSmdReport'
    querydata_1_report = 'params={"funcID":"MDR_SMDR_BROWSE_00","userID":608575,"operations":[{"actionName":"query","count":1,"operationDatas":[{"FD_OBJECTID":"%s","action":"update"}]}]}' % obj_id
    report_data_full = utils.mdr_send_post(mdr_Home_1_report, querydata_1_report, 1, BianMa, send_date)

    try:
        _report_all = json.loads(report_data_full)
    except Exception, err:
        print 'report_id:', BianMa, u'getSmdReport 调用失败 or 解析失败！'

    esData = _report_all['ResponseMessage']['operations'][0]['operationDatas'][0]['es']

    icd_321 = esData[64]['v']

    if not isinstance(icd_321, str) and not isinstance(icd_321, unicode):
        icd_ok = utils.mdr_slice(str(icd_321))
    else:
        icd_ok = utils.mdr_slice(icd_321)

    data["icd_ok"] = icd_ok

    # 报告来源
    _report_data_1 = esData[2]['v']
    data["UnitType"] = utils.data_check_type(utils.bgly(_report_data_1))

    # 联系地址
    data["ReportUnitAddress"] = utils.data_check_type(esData[6]['v'])
    # 报告日期
    data["ReportDate"] = utils.data_check_type(esData[3]['v'])

    # 联系电话
    data["ReportUnitTel"] = utils.data_check_type(esData[7]['v'])
    # 邮编
    data["Postalcode"] = utils.data_check_type(esData[8]['v'])
    # ---------------------------------------------------------------------------------------------------------------
    # 注册证号
    data["CertificateNumber"] = utils.data_check_type(esData[25]['v'])

    # 产品名称
    data["DeviceStandard"] = utils.data_check_type(esData[27]['v'])

    # 商品名称
    data["TradeName"] = utils.data_check_type(esData[29]['v'])

    # 产品分类
    data["classification"] = utils.data_check_type(esData[23]['v'])

    # 生产企业名称
    data["company_name"] = utils.data_check_type(esData[35]['v'])

    # 生产企业地址
    data["manufacturer_address"] = utils.data_check_type(esData[36]['v'])

    # 联系电话
    data["manufacturer_tel"] = utils.data_check_type(esData[37]['v'])

    # 型号规格
    data["specifications"] = utils.data_check_type(esData[30]['v'])

    # 产品编号
    data["Productnumber"] = utils.data_check_type(esData[31]['v'])

    # 产品批号
    data["Batchnumber"] = utils.data_check_type(esData[32]['v'])
    # 操 作 人
    _report_data_18 = esData[38]['v']
    data["operator"] = utils.data_check_type(utils.type_op(_report_data_18))

    # 有效期至
    data["EffectiveDate"] = utils.data_check_type(esData[39]['v'])
    # 生产日期
    data["production_date"] = utils.data_check_type(esData[40]['v'])
    # 停用日期
    data["StopDate"] = utils.data_check_type(esData[41]['v'])
    # 植入日期
    data["ImplantationDate"] = utils.data_check_type(esData[42]['v'])
    # 事件发生初步原因分析
    data["firstreason"] = utils.data_check_type(esData[43]['v'])
    # 事件初步处理情况
    data["firstdone"] = utils.data_check_type(esData[44]['v'])

    # 事件报告状态
    # ---------------------------------------------------------------------------------------------------------------
    # 姓　　名
    data["patient_name"] = utils.data_check_type(esData[9]['v'])
    # 年　　龄
    data["patient_age"] = utils.data_check_type(esData[11]['v'])
    # 出生日期
    data["patient_birthday"] = utils.data_check_type(esData[10]['v'])
    # 性　　别
    _report_data_29 = esData[13]['v']
    data["patient_gender"] = utils.data_check_type(utils.sex(_report_data_29))
    # 电　　话
    data["patient_telephone"] = utils.data_check_type(esData[14]['v'])
    # icd
    #   icd_ok
    # ---------------------------------------------------------------------------------------------------------------
    # 事件发生日期
    data["HappenDate"] = utils.data_check_type(esData[15]['v'])

    # 发现或知悉日期
    data["KnowDate"] = utils.data_check_type(esData[16]['v'])

    # 医疗器械实际使用场所
    _report_data_33 = esData[17]['v']
    data["useplace"] = utils.data_check_type(utils.use(_report_data_33))

    # 事件后果
    _report_data_34 = esData[19]['v']
    data["event_consequence"] = utils.data_check_type(utils.event(_report_data_34))

    # 事件陈述
    data["event_memo"] = utils.data_check_type(esData[21]['v'])
    # ---------------------------------------------------------------------------------------------------------------
    # 报告人类别
    _report_data_36 = esData[45]['v']
    data["reporter_class"] = utils.data_check_type(utils.type_report(_report_data_36))
    # 报告人
    data["reporter"] = utils.data_check_type(esData[46]['v'])
    # ---------------------------------------------------------------------------------------------------------------
    # 死亡时间
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
            data["patient_age"] = utils.str_to_unicode(str(int(_year) - int(data["patient_birthday"][0:4])))
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

login()

mdr_data = mdr_get_report_data(obj_id, bianma, sned_date)

print mdr_data