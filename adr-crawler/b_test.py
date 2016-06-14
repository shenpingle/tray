
import mdrsql

# def test(data):
#
#     qg_data = (
#         data["BianMa"], data["ProvinceName"], data["District"], data["County"],
#         data["ReportUnitName"], data["ReportUnitAddress"], data["ReportUnitTel"], data["Postalcode"],
#         data["UnitType"], data["HappenDate"], data["KnowDate"], data["ReportDate"],
#         data["ReportDate"], data["StateReportDate"], data["State"],StandardFault,
#         StandardFault, IsMatchingFault, SuperFaultName, UnMatchFault)
#     qg_sql = (
#             "replace into mdr_faultbusiness(BianMa,ProvinceName,District,County,ReportUnitName,ReportUnitAddress,"
#             "ReportUnitTel,Postalcode,UnitType ,HappenDate,KnowDate,ReportDate,AcceptDate,StateReportDate,State,"
#             "StandardFault,Name,IsMatchingFault,SuperFaultName,UnMatchFault)"
#             "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#     )
#     mdrsql.mdr_insert_alone(qg_sql, qg_data)


def test(data):

    qg_data = (
        data["BianMa"], data["ProvinceName"], data["District"], data["County"],
        data["ReportUnitName"], data["ReportUnitAddress"], data["ReportUnitTel"], data["Postalcode"],
        data["UnitType"], data["HappenDate"], data["KnowDate"], data["ReportDate"],
        data["ReportDate"], data["StateReportDate"], data["State"],None,
        None, None, None, None)
    qg_sql = (
            "replace into mdr_faultbusiness(BianMa,ProvinceName,District,County,ReportUnitName,ReportUnitAddress,"
            "ReportUnitTel,Postalcode,UnitType ,HappenDate,KnowDate,ReportDate,AcceptDate,StateReportDate,State,"
            "StandardFault,Name,IsMatchingFault,SuperFaultName,UnMatchFault)"
            "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    # mdrsql.mdr_insert_alone(qg_sql, qg_data)
    print qg_sql



data = {'ReportDate': u'2016-01-02', 'ReportUnitTel': '13839302612', 'classification': u'6866\u533b\u7528\u9ad8\u5206\u5b50\u6750\u6599\u53ca\u5236\u54c1', 'ImplantationDate': '0000-00-00', 'patient_birthday': '0000-00-00', 'patient_gender': '\xe5\xa5\xb3', 'operator': '\xe4\xb8\x93\xe4\xb8\x9a\xe4\xba\xba\xe5\x91\x98', 'manufacturer_tel': u'0791-8554986', 'HappenDate': u'2016-01-02', 'patient_telephone': '15286922211', 'useplace': '\xe5\x8c\xbb\xe7\x96\x97\xe6\x9c\xba\xe6\x9e\x84', 'production_date': u'2015-04-02', 'reporter_class': '\xe5\x8c\xbb\xe5\xb8\x88', 'patient_name': u'\u8463\u7d20\u5a25', 'age_class': '\xe9\x9d\x92\xe5\xb9\xb4', 'UnitType': '\xe4\xbd\xbf\xe7\x94\xa8\xe5\x8d\x95\xe4\xbd\x8d', 'company_name': u'\u5357\u660c\u5e02\u671d\u9633\u533b\u7597\u4fdd\u5065\u7528\u54c1\u6709\u9650\u516c\u53f8', 'DeviceStandard': u'\u4e00\u6b21\u6027\u4f7f\u7528\u65e0\u83cc\u9634\u9053\u6269\u5f20\u5668', 'Batchnumber': '20150402', 'patient_age': '40', 'ReportUnitAddress': u'\u6fee\u9633\u53bf\u5b50\u5cb8\u4e61\u6768\u5be8\u6751\u4e1c\u5934', 'EffectiveDate': u'2017-04-02', 'reporter': u'\u5f20\u7fe0\u7ea2', 'specifications': u'\u4e2d\u53f7', 'event_memo': u'2016\u5e741\u67082\u65e5\uff0c\u60a3\u8005\u8463\u7d20\u5a25\u56e0\u4e3a\u5916\u9634\u7619\u75d2\uff0c\u6765\u6211\u9662\u68c0\u67e5\u75c5\u56e0\uff0c\u533b\u751f\u5f00\u5177\u4e00\u6b21\u6027\u4f7f\u7528\u9634\u9053\u6269\u5f20\u5668\u3002\u6253\u5f00\u5305\u88c5\u4e3a\u75c5\u4eba\u8fdb\u884c\u68c0\u67e5\u65f6\uff0c\u53d1\u73b0\u63e1\u4f4f\u624b\u67c4\u628a\u4e0a\u53f6\u548c\u4e0b\u53f6\u6253\u5f00\u65f6\uff0c\u4e2d\u95f4\u8fde\u63a5\u90e8\u5206\u7a81\u7136\u65ad\u5f00\u3002\u68c0\u67e5\u533b\u751f\u7acb\u5373\u66f4\u6362\u65b0\u7684\u6269\u5f20\u5668\u4e3a\u75c5\u4eba\u8fdb\u884c\u68c0\u67e5\u3002\u867d\u7136\u8ba9\u75c5\u4eba\u5728\u68c0\u67e5\u5e8a\u4e0a\u505c\u7559\u65f6\u95f4\u8f83\u957f\uff0c\u4f46\u5e76\u6ca1\u7ed9\u75c5\u4eba\u9020\u6210\u592a\u5927\u5f71\u54cd\u3002', 'StopDate': u'2016-01-02', 'Postalcode': '457169', 'TradeName': u'', 'icd_ok': [u'\u5916\u9634\u7619\u75d2\u75c7'], 'death_time': '0000-00-00', 'firstdone': u'\u66f4\u6362\u65b0\u7684\u6269\u5f20\u5668', 'KnowDate': u'2016-01-02', 'CertificateNumber': u'\u8d63\u98df\u836f\u76d1\u68b0(\u51c6)\u5b572014\u7b2c2660043\u53f7', 'firstreason': u'\u4ea7\u54c1\u539f\u56e0', 'Productnumber': u'', 'event_consequence': '\xe5\x85\xb6\xe5\xae\x83', 'manufacturer_address': u'\u6c5f\u897f\u7701\u5357\u660c\u5e02\u8fdb\u8d24\u53bf\u6e29\u5733\u9547\u524d\u8fdb\u5927\u9053383\u53f7'}

for i in data:
    print i, data[i]