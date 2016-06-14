# coding:utf-8

import mdrsql
import utils
from login2 import login
import simplejson as json
from utils import mdr_send_post
from utils import mdr_slice


bianma = ''
sned_date = ''
obj_id = 'fb123ef8-eb81-4ec6-b5bc-c791855d0419'
# obj_id = '064a88ff-a4a5-4de9-abfa-017dcd08c019'
# obj_id = '064a88ff-a4a5-4de9-abfa-017dcd08c019'
# a

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

    print sh_info
    return sh_info

login()

a = getSmdrWhoArt(sned_date, bianma, obj_id)
print a