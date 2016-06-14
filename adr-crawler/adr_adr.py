#-*- coding:utf-8 -*-
#####################################################################################################
#
#   此文件包括与adr相关的业务逻辑
#
######################################################################################################

import re
import sys

import database_adr
import utils_adr
import adrparseradr_adr
import traceback
import logging

from HTMLParser import HTMLParser
import login_new_adr


#report_show_url
REPORT_SHOW_URL = 'http://www.adrs.org.cn/ADR/page/adrpage/report/adr_report_show.jsp?id=%s'

#track date
re_track_date = re.compile(r'跟踪时间：</td><td[^>]+>(.+?)</td>',re.M|re.U)

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

def get_Medication_Match(medics):
    '''用药集合'''

    #medics = clean_invalid_chars(medics)
    #medics = clean_invalid_chars(medics)

    conn = database_adr.getConnection()
    cur = conn.cursor()

    ret_lst = []
    map = {}
    yao_list = medics.split(",")
    is_matched = True
    for ymcn in yao_list:
        ymcn = clean_invalid_chars(ymcn)
        idx = ymcn.find("(")
        if idx > 0 :
            ymcn = ymcn[0:idx]
        cur.execute("select ylid,ylname,treeid,code,myid,myname,ylyid,ylycn,id as leechdomstandardid,ymcn from ym where ymcn='%s'  limit 1" % str_to_unicode(ymcn))
        rows = cur.fetchall()
        if len(rows) == 0 :
            ret_lst.append(u"[%s:非标准]" % ymcn)
            is_matched = False
        else:
            ret_lst.append(ymcn)
            map[ymcn] = dict(zip(cur.column_names,rows.pop()))

    cur.close()
    conn.close()

    return (is_matched,",".join(ret_lst), map)

def get_Adr_Match(adrs):
    '''不良反应匹配'''

    #adrs = clean_invalid_chars(adrs)

    conn = database_adr.getConnection()
    cur = conn.cursor()

    ret_lst = []
    map = {}
    adr_lst = adrs.split(",")
    is_matched = True
    for adr_name in adr_lst:
        adr_name = clean_invalid_chars(adr_name)
        idx = adr_name.find("(")
        if idx > 0 :
			adr_name = adr_name[0:idx]
        cur.execute("select pid,pname,subid,subname,id as clinicstandardid,name from clinicdetail where name='%s'  limit 1" % str_to_unicode(adr_name))
        rows = cur.fetchall()
        if len(rows) == 0 :
            ret_lst.append(u"[%s:非标准]" % adr_name)
            is_matched = False
            map[adr_name] = False
        else:
            ret_lst.append(adr_name)
            map[adr_name] = dict(zip(cur.column_names,rows.pop()))

    cur.close()
    conn.close()

    return (is_matched,",".join(ret_lst), map)

def get_medic_factory(name):
    '''获取药品生产厂商信息'''

    #name = clean_invalid_chars(name)

    conn = database_adr.getConnection()
    cur = conn.cursor()

    ret = {}

    #查询生产厂家的许可证书和药品本位码
    try:
        cur.execute("select distinct licensenumber,basicnumber,workingcompany as standardfactory from homeproduct  where workingcompany='%s' limit 1" % str_to_unicode(name))
        rows = cur.fetchall()
        if len(rows) > 0:
            data = dict(zip(cur.column_names, rows.pop()))
            ret.update(data)
    except:
        pass

    #查询生产厂家的行政区域等
    cur.execute("SELECT DISTINCT provincial as provincename,city,certificatenumber FROM gmpauthentication WHERE workingcompany = '%s' limit 1" % str_to_unicode(name))
    rows = cur.fetchall()
    if len(rows) > 0:
        data = dict(zip(cur.column_names, rows.pop()))
        if not data["city"] :
            data["city"] = ""
        if not data["provincename"] :
            data["provincename"] = ""

        ret.update(data)

    cur.close()
    conn.close()

    return ret

def get_pass_medic(ym_dict):
    '''判断是否有不合理用药'''

    my_names = []
    my_keys = []
    ret = {}
    for ymcn,d in ym_dict.iteritems():
        if d["myname"] not in my_names:
            my_names.append(d["myname"])
            my_keys.append(ymcn)

    conn = database_adr.getConnection()
    cur = conn.cursor()

    llen = len(my_names)
    if llen < 2:
        return ret

    i = 0
    while i <= llen-2 :
        j = i+1
        while j < llen:
            sql = "select id as pass_basic_id,interaction_id,pass_main_used,pass_main,main_code,main_ylname,pass_corres_used,pass_corres,corres_code,corres_ylname,ratelevle,slipsdocument,adverseeffect from pass_basic where pass_main='%s' and pass_corres='%s'  limit 1" % (str_to_unicode(my_names[i]),str_to_unicode(my_names[j]))
            cur.execute(sql)
            rows = cur.fetchall()
            if len(rows) > 0 :
                ret[my_keys[i]] = dict(zip(cur.column_names,rows.pop()))
            j += 1

        i += 1

    cur.close()
    conn.close()

    return ret

def get_ror_match(ym_dict):
    '''获取ROR数据'''

    my_names = []
    ret = {}

    conn = database_adr.getConnection()
    cur = conn.cursor()

    for ymcn,d in ym_dict.iteritems():
        cur.execute("select my_name,code from ror_my_object where my_name='%s'  limit 1" % str_to_unicode(d["myname"]))
        rows = cur.fetchall()
        if len(rows) > 0 :
            ret[ymcn] = dict(zip(cur.column_names,rows.pop()))

    cur.close()
    conn.close()

    return ret

def get_ned_province(my_data):
    '''获取国药/省药 信息'''

    my_names = []
    ret = {}

    conn = database_adr.getConnection()
    cur = conn.cursor()

    for ymcn,d in my_data.iteritems():
        cur.execute("select name,code,yl, isned from ned_provincebasis where Name='%s'  limit 1" % str_to_unicode(d["myname"]))
        rows = cur.fetchall()

        if len(rows) > 0 :
            ret[ymcn] = dict(zip(cur.column_names,rows.pop()))

    cur.close()
    conn.close()

    return ret

def get_import_medic(ym_dict):
    '''根据母药名称获取重点监控药品信息'''

    conn = database_adr.getConnection()
    cur = conn.cursor()
    ret = {}
    for ymcn,d in ym_dict.iteritems():
        cur.execute("select ylname,code,myname from importyaopin where myname='%s'  limit 1" % str_to_unicode(d["myname"]))
        rows = cur.fetchall()
        if len(rows) > 0 :
            #ret[ymcn] = dict(zip(cur.column_names,rows.pop()))
            ret[ymcn] = True

    cur.close()
    conn.close()

    return ret

def get_otc_type(ymcn):
    '''获取药品说明书'''

    conn = database_adr.getConnection()
    cur = conn.cursor()

    ret = None

    cur.execute("select '化学药品' as descriptiontype, id as descriptionid from drugs_description where ymcn='%s'  limit 1" % ymcn.encode('utf-8'))
    rows = cur.fetchall()
    if len(rows) > 0 :
        row = rows.pop()
        ret = {"descriptiontype":row[0],"descriptionid" : row[1]}

    if not ret :
        cur.execute("select '中药OTC' as descriptiontype, id as descriptionid from drugs_otc_description where ymcn='%s'  limit 1" % ymcn.encode('utf-8'))
        rows = cur.fetchall()
        if len(rows) > 0:
            row = rows.pop()
            ret = {"descriptiontype":row[0],"descriptionid" : row[1]}

    if not ret:
        cur.execute("select '西药OTC' as descriptiontype, id as descriptionid from drugs_west_otc_description where ymcn='%s'  limit 1" % ymcn.encode('utf-8'))
        rows = cur.fetchall()
        if len(rows) > 0:
            row = rows.pop()
            ret = {"descriptiontype":row[0],"descriptionid" : row[1]}

    cur.close()
    conn.close()

    return ret

def get_unit_info(unit_name):
    '''获取报告单位或代报单位的区域信息'''
    conn = database_adr.getConnection()
    cur = conn.cursor()

    ret = None
    if isinstance(unit_name, str):
        unit_name = unit_name.decode("utf-8")

    sql = u"select provincename,districttypeid as district,county from unit where name='%s'  limit 1" % str_to_unicode(unit_name)

    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) > 0 :
        ret = dict(zip(cur.column_names,rows.pop()))

    cur.close()
    conn.close()

    return ret

#####################################################################################################
#   刘欣毅修改get_unit_info2业务：
#   没有匹配unit表，通过报表编码前6位，查询district_code_china来匹配行政区域信息
#   注意：没有匹配的情况下，新增unit表上报单位？实际是可以的，通过单位类型、名称、行政区域等信息
#   修改日期：2014-10-29
######################################################################################################
def get_unit_info2(id):
    '''获取报告单位或代报单位的区域信息'''
    conn = database_adr.getConnection()
    cur = conn.cursor()

    ret = None
    #bianma: 4116271569994201400001
    #bianma[0:6]: 411627
    id2 = id[0:6]
    #districttype_hn
    #sql = u"select provincename,districttypeid as district,county from unit where name='%s'" % str_to_unicode(id2)
    sql = u"select ProvinceName,Name as district,county from district_code_china where bianma='%s'  limit 1" % str_to_unicode(id2)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) > 0:
        ret = dict(zip(cur.column_names,rows.pop()))

    cur.close()
    conn.close()

    return ret

def get_appraises(show_id, body):
    #关联性评价  id="evaluateInfoArea"
    re_eval_info = re.compile(r'<!-- 报告评价信息层\(start\) -->([\s\S]*)<!-- 报告评价信息层\(end\) -->',re.U|re.M)
    match = re_eval_info.search(body)
    appraises = []
    data = {}
    if match :
        relate_body = match.group(0)
        person_relate = adrparseradr_adr.get_person_relation_appraise(relate_body)
        if person_relate and isinstance(person_relate,list) :
            data["relationpersonappraise"] = person_relate[1]
            data["relationpersonremark"] = person_relate[2]
            data["personappraisedate"] = person_relate[3]
            data["personappraisegraph"] = person_relate[4]


        unit_relate = adrparseradr_adr.get_unit_relation_appraise(relate_body)
        if unit_relate and isinstance(unit_relate,list) :
            data["relationunitappraise"] = unit_relate[1]
            data["relationunitremark"] = unit_relate[2]
            data["unitappraisedate"] = unit_relate[3]
            data["unitappraisegraph"] = unit_relate[4]


        levels_relate = adrparseradr_adr.get_level_relateion_appraise(relate_body)
        level_names = ["state","province","municipal","basic"]
        level_namesed = []
        n_idx = 0
        if levels_relate and isinstance(levels_relate, list) :
            lev_idx = len(levels_relate) -1
            while lev_idx >= 0 :
                row = levels_relate[lev_idx]
                lev_idx -= 1
                if len(row) < 10 :
                    continue

                unit_name = row[0]
                if n_idx == 0 and unit_name != "国家食品药品监督管理局药品评价中心" :
                    n_idx += 1

                if n_idx >= len(level_names) : #当评价数据超过4个，直接跳出
                    logging.info( "appraise is too much！ show_id : %s \n" % (show_id))
                    break

                if unit_name in level_namesed :
                    continue
                else :
                    level_namesed.append(unit_name)

                prefix = level_names[n_idx]
                data[ prefix + "unitname"] = unit_name
                data[ prefix + "appraise"] = row[1]
                data[ prefix + "remark"] = row[2]
                tmp = row[2]
                degree = []
                if "," in tmp :
                    degree = tmp.split(",")
                elif "，" in tmp:
                    degree = tmp.split("，")
                if len(degree) >= 2:
                    if "度" in degree[0] :
                        data[ prefix + "appraisedegree"] = degree[0]
                    if "级" in degree[1] :
                        data[ prefix + "appraiselevel"] = degree[1]

                data[ prefix + "appraisedate"] = row[3]
                data[ prefix + "appraisegraph"] = row[4]
                data[ prefix + "adrdateanalyse"] = row[5]
                data[ prefix + "adrtypeanalyse"] = row[6]
                data[ prefix + "stopmedicationanalyse"] = row[7]
                data[ prefix + "useagainanalyse"] = row[8]
                data[ prefix + "otherrelatedanalyse"] = row[9]

                n_idx += 1
    return data

def import_from_html(qrow):
    show_id = qrow["report_id"]

    bianma = qrow["report_id2"]                         #编码
    fungible_name = qrow["personal_his"]                #代报单位
    report_unit_name = qrow["report_unit_name"]         #报告单位
    medic_list = qrow["general_name"]                   #通用名称，用药集合
    adr_list = qrow["adr_name"]                         #不良反应名称
    data_source = qrow["data_source"]                   #个例来源
    report_type = qrow["new_flag"]                      #报告类型
    StateReportDate = qrow["report_date"]               #国家中心接收时间

    if fungible_name == "null" :
        fungible_name = ""

    if report_unit_name == "null" :
        report_unit_name = ""

    unit_name = ""
    if fungible_name != "" :
        unit_name = fungible_name
    else :
        unit_name = report_unit_name
        #此处应该修改为get_unit_info2（id），id是报表编码
    unit_area = get_unit_info(unit_name)
    #unit_area = get_unit_info2(bianma)

    #medic_list = clean_invalid_chars(medic_list)
    #adr_list = clean_invalid_chars(adr_list)

    conn = database_adr.getConnection()
    cur = conn.cursor()

    cur.execute("select count(*) from business_gather where show_id='%s'" % show_id)
    results = cur.fetchall()
    ret = results[0]
    generate_id = 0
    if ret[0] > 0 :
        logging.info("show_id:%s is repeat!" % (show_id))
        return #已经导入过了，不再重复导入
    else:
        cur.execute("insert into business_gather_serial(id) values (null)")
        cur.execute("select LAST_INSERT_ID()")
        ids = cur.fetchall().pop()
        generate_id = ids[0]

    sql = ""
    try:
        show_url = REPORT_SHOW_URL % (show_id)

        body = login_new_adr.send_adr_url(show_url)
        if not body:
            print 'get url:%s body is failure!' % show_url
            return

        all_fields = adrparseradr_adr.get_all_fields(body)

        #业务主表
        business_data = adrparseradr_adr.get_business_row(all_fields)
        if "unittype" not in business_data:
            business_data["unittype"] = ""

        #track_date
        match = re_track_date.search(body)
        if match :
            business_data["trackdate"] = match.group(1)
        else:
            business_data["trackdate"] = "0000-00-00"

        business_data["id"] = generate_id
        business_data["show_id"] = show_id
        business_data["bianma"] = bianma
        business_data["reporttype"] = report_type
        business_data["examplesource"] = data_source
        business_data["statereportdate"] = StateReportDate
        business_data["fungiblereportunit"] = fungible_name
        business_data["reportunitname"] = report_unit_name
        """
        if isinstance(unit_area, dict):
            print "get_unit_info:", unit_area
            business_data.update(unit_area)
        else:
            unit_area = get_unit_info2(bianma)
            print "get_unit_info2:", unit_area
            business_data.update(unit_area)
        """

        #患者分类
        if not "age" in business_data :
            print "unknown age! ",show_id
            business_data["sufferertype"] = ""
        else :
            try:
                age = float(business_data["age"])
                if age > 1000 :
                    age = 0
                business_data["age"] = age

                if age < 12 :
                    business_data["sufferertype"] = u"儿童"
                elif age < 18:
                    business_data["sufferertype"] = u"青少年"
                elif age < 60:
                    business_data["sufferertype"] = u"成人"
                else:
                    business_data["sufferertype"] = u"老人"

            except :
                business_data["age"] = 0

        if "该报告没有上传附件！" in body :
            business_data["isattachments"] = u"无"
        else:
            business_data["isattachments"] = u"是"

        #重点监控医院标记
        business_data["isimporthospital"] = u"否"
        if business_data["unittype"] == u"医疗机构" :
            cur.execute("select count(*) from imphospital where hospitalcn='%s'  limit 1" % str_to_unicode(business_data["reportunitname"]))
            result = cur.fetchall().pop()
            if result[0] > 0 :
                business_data["isimporthospital"] = u"是"

        #用药集合
        is_matched, medics, my_data = get_Medication_Match(medic_list)
        if is_matched:
            business_data["ismedicationmatch"] = u"是"
        else:
            business_data["ismedicationmatch"] = u"否"

        business_data["medicationlist"] = medics

        #adrlist
        is_adr_matched, adrs, adr_datas = get_Adr_Match(adr_list)
        if is_adr_matched:
            business_data["isadrmatch"] = u"是"
        else:
            business_data["isadrmatch"] = u"否"

        business_data["adrlist"] = adrs

        if "oldsickness" in business_data:
            #business_data["oldsickness"] = clean_invalid_chars(business_data["oldsickness"])
            business_data["oldsickness"] = str_to_unicode(business_data["oldsickness"])


        #公共数据
        share_data = {}
        share_data["id"] = business_data["id"]
        share_data["bianma"] = str_to_unicode(business_data["bianma"])
        share_data["reporttype"] = str_to_unicode(business_data["reporttype"])

        share_data["kickbacktype"] = str_to_unicode(business_data["kickbacktype"]) if "kickbacktype" in business_data else ""

        share_data["reportunitname"] = str_to_unicode(business_data["reportunitname"])
        share_data["unittype"] = str_to_unicode(business_data["unittype"])

        share_data["happendate"] = str_to_unicode(business_data["happendate"]) if "happendate" in business_data else str_to_unicode("0000-00-00")
        share_data["reportdate"] = str_to_unicode(business_data["reportdate"]) if "reportdate" in business_data else str_to_unicode("0000-00-00")
        share_data["statereportdate"] = str_to_unicode(business_data["statereportdate"]) if "statereportdate" in business_data else str_to_unicode("0000-00-00")
        share_data["trackdate"] = str_to_unicode(business_data["trackdate"]) if "trackdate" in business_data else str_to_unicode("0000-00-00")

        share_data["isimporthospital"] = str_to_unicode(business_data["isimporthospital"])
        share_data["imphospitalname"] = str_to_unicode(business_data["reportunitname"])

        unit_area = get_unit_info(unit_name)
        if isinstance(unit_area, dict):
            #print "get_unit_info:", unit_area
            business_data.update(unit_area)
        else:
            #unit_area = get_unit_info2(bianma)[0]
            unit_area = get_unit_info2(bianma)
            #print "get_unit_info2:", unit_area
            #business_data.update(unit_area)
            if unit_area:
                business_data.update(unit_area)
            else:
                pass
            #新增逻辑,表明
            import mdrsql
            #重复单位不再插入，2014-11-24
            #刘欣毅修改 2015-03-20
            #屏蔽单位明细表所有检测和add工作
            #cur.execute("select Name FROM unitdetail where Name='%s'" % str_to_unicode(unit_name))
            #rows = cur.fetchall()
            #if len(rows) > 0:
            #    pass
            #else:
            #    sql_id = u"SELECT max(ID) FROM unitdetail"
            #    cur.execute(sql_id)
            #    mydata = cur.fetchall()
            #    maxId = mydata[0][0]
            #    print maxId
            #    if maxId is None :
            #        maxId = 0
            #    else :
            #        maxId = int(maxId)
            #    maxId = maxId + 1
            #    data_ud = (unit_name, share_data["unittype"])
            #    print data_ud
            #    sql_insert_unitdetail = (
            #        "insert into unitdetail (Name,UnitType) "
            #        "value(%s,%s)"
            #    )
            #    mdrsql.mdr_insert_alone(sql_insert_unitdetail, data_ud)

            #conn = database_adr.getConnection()
            #cur = conn.cursor()
            #根据编码查询district_code_china.sql找到行政区域信息->组装核心单位信息->把此上报单位插入unit/Detail表
            #bianma: 4116271569994201400001
            #bianma[0:6]: 411627
            print "bianma:", bianma
            id2 = bianma[0:6]
            sql = u"select ProvinceName,Name,County,bianma from district_code_china where bianma='%s'  limit 1" % str_to_unicode(id2)
            cur.execute(sql)
            rows2 = cur.fetchall()
            if len(rows2) > 0:
                #
                import time
                insert_today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                sql_id = u"SELECT max(ID) FROM unit"
                cur.execute(sql_id)
                mydata_unit = cur.fetchall()
                #data_u = (str(mydata_unit[0][0]+1), share_data["unittype"], rows[1], unit_name, rows[0], rows[2], rows[3], u"", u"1", insert_today )
                #print "rows:", rows2
                #print "mydata_unit[0][0]:", mydata_unit[0][0]
                #print "share_data[unittype]:",share_data["unittype"]
                #print "insert_today:", insert_today
                #print "unit_name:", unit_name
                print "district_code_china:",  rows2[0][0],rows2[0][1], rows2[0][2], rows2[0][3]
                data_u = (str(int(mydata_unit[0][0])+1), share_data["unittype"], rows2[0][1], unit_name, rows2[0][0], rows2[0][2], rows2[0][3], u"1", insert_today, insert_today)
                sql_insert_unit = (
                    "insert into unit (ID,UnitTypeID,DistrictTypeID,Name,ProvinceName,County,CodeID,audit,regDate,auditDate)"
                    "value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                )
                mdrsql.mdr_insert_alone(sql_insert_unit,data_u)
            else:
                pass
            #ID,
            # UnitTypeID,
            # DistrictTypeID,
            # Name,
            # ProvinceName,
            #
            # County,
            # CodeID,
            # Address,
            # audit,
            # auditDate

        #不合理用药数据
        pass_rows = get_pass_medic(my_data)
        if len(pass_rows) > 0:
            business_data["ispass"] = u"是"
            for _ymcn,row in pass_rows.iteritems() :
                row.update(share_data)
                database_adr.insert_to_table("olappass", row)
        else:
            business_data["ispass"] = u"否"

        #ROR判断
        ror_datas = get_ror_match(my_data)
        if len(ror_datas) > 0:
            business_data["isror"] = u"是"
        else:
            business_data["isror"] = u"否"

        #重点监控药品
        imp_yaos = get_import_medic(my_data)
        business_data["isimportmedication"] = u"否"
        if len(imp_yaos) > 0 :
            business_data["isimportmedication"] = u"是"

            #基本药物
        ned_data = get_ned_province(my_data)
        business_data["isned"] = u"无"
        if len(ned_data) > 0 :
            business_data["isned"] = u"有"

        distrust_Rows = adrparseradr_adr.get_distrust_Rows(all_fields,share_data)       #怀疑用药明细
        auxiliary_rows = adrparseradr_adr.get_auxiliary_rows(all_fields,share_data)   #并用药
        leepchdom_data_rows = distrust_Rows + auxiliary_rows
        for row in leepchdom_data_rows:
            if "tradename" in row :
                row["tradename"] = str_to_unicode(row["tradename"].replace("*",""))
            if "reason" in row :
                row["reason"] = str_to_unicode(row["reason"].replace("*",""))

            factory_name = None
            if "standardfactory" in row :
                #row["standardfactory"] = clean_invalid_chars(str_to_unicode(row["standardfactory"]))
                row["standardfactory"] = str_to_unicode(row["standardfactory"])
                factory_name = str_to_unicode(row["standardfactory"])

            if factory_name:
                factory_data = get_medic_factory(factory_name)
                if len(factory_data) > 0:
                    if "licensenumber" in row and len(row["licensenumber"]) > 0 and "licensenumber" in factory_data:
                        del factory_data["licensenumber"]

                    row.update(factory_data)
                    row["ismatchingfactory"] = u"是"
                else:
                    row["ismatchingfactory"] = u"否"
                    row["unmatchfactory"] = factory_name
                    del row["standardfactory"]

            if "_generalname" in row :
                #row["_generalname"] = clean_invalid_chars(str_to_unicode(row["_generalname"]))
                row["_generalname"] = str_to_unicode(row["_generalname"])

                general_name = str_to_unicode(row["_generalname"])
                general_name = clean_invalid_chars(general_name)
                iidx = general_name.find("(")
                if iidx > 0 :
                    general_name = general_name[0:iidx]

                row["ismatchingmedication"] = u"否"
                row["unmatchmedication"] = str_to_unicode(general_name)
                if general_name in my_data:
                    #母药数据
                    row.update(my_data[general_name])
                    row["ismatchingmedication"] = u"是"
                    del row["unmatchmedication"]


                #药品类型，国药、省药
                row["isned"] = u"否"
                if general_name in ned_data:
                    ned = ned_data[general_name]
                    if ned :
                        row["isned"] = u"是"
                        if ned["isned"] == u"1":
                            row["nedtype"] = u"国药"
                        else :
                            row["nedtype"] = u"省药"

                #ROR标志
                row["isror"] = u"否"
                if general_name in ror_datas:
                    row["isror"] = u"是"

                #otc
                otc_data = get_otc_type(general_name)
                row["isdescription"] = u"无"
                if otc_data:
                    row.update(otc_data)
                    row["isdescription"] = u"有"

                #important medic
                row["isimportmedication"] = u"否"
                if general_name in imp_yaos:
                    row["isimportmedication"] = u"是"


            database_adr.insert_to_table("olapleechdom", row)

        #不良反应表
        for adr_name,adr_data in adr_datas.iteritems():
            if isinstance(adr_data,dict):
                adr_data.update(share_data)
                adr_data["ismatchingclinic"] = "是"

            else:
                adr_data = {}
                adr_data.update(share_data)
                adr_data["ismatchingclinic"] = "否"
                adr_data["unmatchclinic"] = adr_name

            database_adr.insert_to_table("olapclinic", adr_data)

        #附件表数据
        attaches = adrparseradr_adr.get_attachments(body)
        if len(attaches) > 0:
            for row in attaches:
                #row["id"] = business_data["id"]
                row["bianma"] = business_data["bianma"]
                database_adr.insert_to_table("attachments", row)

        #关联性评价
        appraise_data = get_appraises(show_id, body)
        business_data.update(appraise_data)
        #主表数据入库
        database_adr.insert_to_table("business_gather", business_data)
        print "%s is done!" % (show_id)

    except Exception as err:
        logging.info("show_id : %s \t" % (show_id))
        logging.info(str(err.args) + ":\n")
        traceback.print_exc()
        try:
            logging.info(traceback.format_exc() + "\n")
        except:
            pass

    conn.commit()
    conn.close()

def clean_invalid_chars(cont):
    '''过滤非法字符'''
    if not isinstance(cont, unicode) :
        cont = str_to_unicode(cont)
        
    ret = cont.replace(u"*","")
    ret = ret.replace(u"×","")
    ret = ret.replace(u"，",",")
    ret = ret.replace(u"；",",")
    ret = ret.replace(u"、",",")
    ret = ret.replace(u"/",",")
    ret = ret.replace(u"／",",")
    ret = ret.replace(u"。",",")
    ret = ret.replace(u"（","(")
    ret = ret.replace(u"）",")")
    ret = ret.replace(u"Ⅱ","II")
    ret = ret.replace(u"；",",")

    return ret