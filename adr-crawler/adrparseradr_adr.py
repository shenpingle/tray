#-*- coding:utf8 -*-
#*
#*  此文件包含抓取到的文件内容解析相关的功能实现
#*

import re
from HTMLParser import HTMLParser

####################################################################
#
# 表数据与页面label的对应关系
#
####################################################################

#业务主表字段
_business_fields = {
    'label_FIRST_REPORT'        :   "firsttraced",       #首次跟踪报告
    'label_REPORT_ID'           :   "" ,           #编码
    'label_HARM_LEVEL'          :   "reporttypedetail",        #报表类型
    'label_REPORT_SOURCE'       :   "unittype",          #报单单位类别
    'label_PATIENT_NAME'        :   "sufferername",      #患者姓名
    'label_GENDER_ID'           :   "sex",               #患者性别
    'label_NATION_NAME'         :   "ethic",             #民族
    'label_BIRTH_DATE'          :   "birthday",          #出生日期      
    'label_AGE'                 :   "age",               #年龄
    'label_AGE_UNIT'            :   "",  
    'label_WEIGHT'              :   "avoirdupois",       #体重
    'label_TELPHONE'            :   "contacttele",         #联系电话
    
    'label_ADR_RPT_DISEASE'     :   "oldsickness",       #原患疾病
    'label_HOSPITAL_NAME'       :   "hospitalname",      #医院名称
    'label_MEDICAL_RECORD_NO'   :   "clinicno",          #门诊号
    'label_ONCE_ADR_FALG'       :   "pastbuliang",       #既往药品不良反应/事件
    'label_FAMILY_ADR_FLAG'     :   "homebuliang",       #家族药品不良反应
    'label_ADR_RPT_IMPORTANT'   :   "otherimportinfo",   #相关重要信息：吸烟史、饮酒史、妊娠期、肝病史、肾病史、过敏史、其他  
    'label_ADR_RPT_ADRNAME'     :   "",                  #
    'label_ADR_DATE'            :   "happendate",        #不良反应发生时间
    'label_ADR_DESCRIBE'        :   "depictdispose",     #不良反应描述
    'label_ADR_RESULT'          :   "kickbacktype",      #不良反应事件结果
    'label_CEASE_DRUG_RESULT'   :   "stopresult",        #停药或减量后反应/事件是否消失或减轻
    'label_AGAIN_DRUG_RESULT'   :   "useagain",          #再次使用可疑药品后是否再次出现同样反应/事件
    'label_REFLECT_OLD_DISEASE' :   "infection",         #对原患疾病的影响
    'label_PICKER_EVALUATE'     :   "reportpersonappraise", #报告人评价
    'label_PICKER_EVAL_SIGN'    :   "reportpersonautograph",#报告人签名
    'label_RPT_UNIT_EVALUATE'   :   "reportunitappraise",   #报告单位评价
    'label_RPT_UNIT_SIGN'       :   "reportunitautograph",  #报告单位签名
    'label_PICKER_TEL'          :   "reportpersonphone",    #报告人联系电话
    'label_PICKER_VOCATION'     :   "reportpersonwork",  #报告人职业
    'label_PICKER_EMAIL'        :   "reportpersonmail",  #报告人邮件
    'label_PICKER_SIGN'         :   "reportpersongraph", #报告人签名：填写签名
    'label_REPORT_UNIT_NAME'    :   "reportunitname",   #报告单位名称
    'label_REPORT_UNIT_LINKMAN' :   "reportunitlinkman", #报告单位联系人
    'label_REPORT_TEL'          :   "reportunitphone",   #报告单位联系电话
    'label_REPORT_DATE'         :   "reportdate",        #报告时间
    'label_DEATH_CAUSE'         :   "deathreason",       #直接死因
    'label_DEATH_DATE'          :   "deathdate",         #死亡时间
    'label_NOTES'               :   "comments",          #备注
    'label_INFO_SOURCE'         :   "inforsource",       #信息来源
}


#怀疑用药相关Key
distrust_keys = {
        "label_APPROVAL_NO_D"				:	"licensenumber", 			#'批准文号',
        "label_DRUG_NAME_D"				    :	"tradename", 			#'商品名称',
        "label_GENERAL_NAME_D"				:	"_generalname", 			#通用名称,
        "label_DOSAGEf_FORM_D"				:	"dosagetype", 			#'药品剂型',
        "label_BATCH_NO_D"	    			:	"batchnumber", 			#'生产批号',
        "label_DOSAGE_D"				    :	"yongfa1", 			#'用法',
        "label_DRUG_UNIT_D"				:	"yongfa2", 			#'用法',
        "label_PERIOD_DAY_D"				:	"yongliang1", 			#'用量',
        "label_TIMES_D"				    :	"yongliang2", 			#'用量',
        "label_USAGE_MODE_D"				:	"usemedicineroute", 			#'用药途径',
        "label_START_DATE_D"				:	"begaindate", 			#'开始用药时间',
        "label_END_DATE_D"				:	"enddate", 			#'终止用药时间',
        "label_CAUSE_D"				:	"reason", 			#'用药原因'
        "label_FACTORY_NAME_D"				:	"standardfactory", 			#'生产厂家'
        }
        
#并用药相关Key
auxiliary_keys = {
        "label_APPROVAL_NO_M"				:	"licensenumber", 			#'批准文号',
        "label_DRUG_NAME_M"				:	"tradename", 			#'商品名称',
        "label_GENERAL_NAME_M"				:	"_generalname", 			#通用名称
        "label_DOSAGEf_FORM_M"				:	"dosagetype", 			#'药品剂型',
        "label_BATCH_NO_M"	    			:	"batchnumber", 			#'生产批号',
        "label_DOSAGE_M"				    :	"yongfa1", 			#'用法',
        "label_DRUG_UNIT_M"				:	"yongfa2", 			#'用法',
        "label_PERIOD_DAY_M"				:	"yongliang1", 			#'用量',
        "label_TIMES_M"				    :	"yongliang2", 			#'用量',
        "label_USAGE_MODE_M"				:	"usemedicineroute", 			#'用药途径',
        "label_START_DATE_M"				:	"begaindate", 			#'开始用药时间',
        "label_END_DATE_M"				:	"enddate", 			#'终止用药时间',
        "label_CAUSE_M"				:	"reason", 			#'用药原因'
        "label_FACTORY_NAME_M"				:	"standardfactory", 			#'生产厂家'
        }


##############################################################################################
#
# 各种解析用的正则
#
##############################################################################################


#国家中心接收时间
re_country_accept_time = re.compile(r'国家中心接收时间：</td><td width="12%" class="tdShow riValue leftNoBorder">(.+?)</td>',re.M|re.U)

#获取所有有用标签正则
re_lables = re.compile(r'<label\s+id="([a-zA-Z0-9_]+)">((\s|\S)*?)</label>',re.M|re.U)

#电话号码检测
re_telephone = re.compile(r"(\d{3,4}-?)?\d{7,12}",re.U)

#td
re_td = re.compile(r"<td[^>]+>(.*?)</td>",re.M|re.U)

#报告人关联性评价
re_person_relate_appraise = re.compile(r'<tr>\s+<td class="tdStyle riValue">报告人</td>([\s\S]+?)</tr>',re.U|re.M)
#报告单位关联性评价
re_unit_relate_appraise = re.compile(r'<tr>\s+<td class="tdStyle riValue">报告单位</td>([\s\S]+?)</tr>',re.U|re.M)
#各层级关联性评价
re_level_relate_appraise = re.compile(r'<tr>\s+(<td class="tdStyle riValue" style="border-bottom:none;">[\s\S]+?)</tr>\s+<tr>\s+<td class="tdStyle riValue" style="border-top:none;"></td>([\s\S]+?)</tr>\s+</table>', re.U|re.M)

def str_to_unicode(text, encoding=None, errors='strict'):
    #
    if encoding is None:
        encoding = 'utf-8'
    if isinstance(text, str):
        return text.decode(encoding, errors)
    elif isinstance(text, unicode):
        return text
    else:
        raise TypeError('str_to_unicode must receive a str or unicode object, got %s' % type(text).__name__)
    
#全角数据字换半角数字
cnstr_replace = {
    "０": "0",
    "１": "1",
    "２": "2",
    "３": "3",
    "４": "4",
    "５": "5",
    "６": "6",
    "７": "7",
    "８": "8",
    "９": "9",
    "－": "-",
}

#############################################################################################
#
# 用到的各种函数
#
#############################################################################################

def get_all_fields(body):
    '''获取所有有用的数据字段'''
    
    matches = []
    p = HTMLParser()
    for m in re_lables.finditer(body):
        val = m.group(2).decode("utf8")
        val = p.unescape(val)
        
        matches.append( ( m.group(1),val.replace("\n","").replace("\\"," ").replace("\0","") ) )
    return matches

def get_business_row(matches):
    '''业务主表数据'''
    row = {}
    for lab,val in matches:
        val = val.strip()
        if lab in _business_fields:
            key = _business_fields[lab]
            
            #电话处理
            #if key == "telephone" :
            #    for (c,n) in cnstr_replace.iteritems():
            #        val = val.replace(c,n)
            #    match = re_telephone.search(val)
            #    if match :
            #        contact = val
            #        
            #        val = match.group(0)
            #        
            #        contact = re_telephone.sub("",contact)
            #        if len(contact) > 0:
            #            row["contacttele"] = contact
            #    else:
            #        key = "contacttele"
            
            #体重处理
            if key == "avoirdupois":
                val = re.sub(r"\s","",val)
                    
            if len(key) >  0 :
                row[key] = val
    return row
        
        
def get_distrust_Rows(matches,extend):
    '''获取所有药品明细信息'''
    #怀疑用药
    return _get_leepch_rows(matches, u"怀疑", distrust_keys, extend)
    
def get_auxiliary_rows(matches,extend):
    #并用药
    return _get_leepch_rows(matches, u"并用", auxiliary_keys, extend)
    
    
def _get_leepch_rows(matches, type, fields, extend):
    auxiliary_rows = []
    for i in range(1,25):
        row = {}
        row["usegetype"] = type
        for _pre,_name in fields.iteritems():
            dst_lab = _pre + str(i)
            val = _get_lab_val(matches,dst_lab)
            if val :
                row[_name] = val
                
        yongfa = ""
        if "yongfa1" in row:
            yongfa = row["yongfa1"]
            del row["yongfa1"]
        if "yongfa2" in row:
            yongfa += row["yongfa2"]
            del row["yongfa2"]
        row["yongfa"] = yongfa
        
        yongliang = ""
        if "yongliang1" in row:
            yongliang = str_to_unicode(row["yongliang1"]) + u"日"
            del row["yongliang1"]
        if "yongliang2" in row:
            yongliang += str_to_unicode(row["yongliang2"]) + u"次"
            del row["yongliang2"]
        row["yongliang"] = yongliang
                
        if len(row) <= 3 or (yongfa == "" and yongliang == ""):
            break
        else :
            row.update( extend  )
            auxiliary_rows.append( row )
            
    return auxiliary_rows
    
def _get_lab_val(matches,lab):
    '''获取lab对应的val'''
    for l,v in matches:
        if l == lab :
            return v
    
    return None
    
def get_attachments(body):
    '''获取附件表数据'''
    
    #获取附件表格
    re_attach_table = re.compile(r'<div id="ADR_RPT_ATTACHMENT">([\s\S]+?)</table>',re.M|re.U)
    
    #获取表格的一行
    re_attach_tr  = re.compile(r'<tr>\s+<td class="tdShow botValue">\d+</td>([\s\S]+?)</tr>', re.M|re.U)
    
    #行内的一个单元格
    re_attach_td  = re.compile(r'<td[^>]+>(.*?)</td>', re.M|re.U)
    
    #行内的a标签
    re_attach_href  = re.compile(r'<a[^>]+>(.*?)</a>', re.I|re.U)
        
    ret = []
    attach_table = re_attach_table.search(body)
    if attach_table :
        for attach_tr in re_attach_tr.findall(attach_table.group(0)):
            tds = re_attach_td.findall(attach_tr)
            if len(tds) < 1:
                continue
            
            row = {}
            match = re_attach_href.search(tds[0])
            row["filename"] = match.group(1)
            row["attachmenttype"] = tds[1]
            row["summary"] = tds[2]
            row["uploaddate"] = tds[3]
            row["uploadunit"] = tds[4]
            
            ret.append(row)
            
    return ret
    
def get_person_relation_appraise(appraise_body) :
    '''获取个人关联性评价'''
    ret = None
    match = re_person_relate_appraise.search(appraise_body)
    if match :
        ret = []
        for m in re_td.finditer(match.group(0)):
            ret.append(m.group(1))
    return ret   
    
def get_unit_relation_appraise(appraise_body) :
    '''获取个人关联性评价'''
    ret = None
    match = re_unit_relate_appraise.search(appraise_body)
    if match :
        ret = []
        for m in re_td.finditer(match.group(0)):
            ret.append(m.group(1))
    return ret
    
def get_level_relateion_appraise(appraise_body):
    ret = []
    re_relate_right = re.compile(r'<td class="tdStyle riValue" width="30%"[^>]+>(.*?)</td>',re.M|re.U)
    for match in re_level_relate_appraise.finditer(appraise_body):
        row = []
        for m in re_td.finditer(match.group(1)):
            row.append(m.group(1))
        for m in re_relate_right.finditer(match.group(2)):
            row.append(m.group(1))
        ret.append(row)
        
    return ret