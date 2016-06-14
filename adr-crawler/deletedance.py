# -*- coding:utf-8 -*-
###########################################################################################
#  author: luu
#  info:删除数据库数据
#  Revision: 1.0
"""
    功能说明：  删除数据库数据

"""
###########################################################################################
from config import *
from mdrtime import *
from mdrsql import mdr_select


# 删除数据库数据
def dodelete(_data):
    t1 = _data["beginTime"]
    t2 = _data["endTime"]
    print t1
    print t2
    myconn = myconnect()
    mycu = myconn.cursor()
    mycu.execute("delete from mdr_business_gather where ReportDate>='%s' and ReportDate<='%s'" % (t1, t2))
    myconn.commit()
    mycu.execute("delete from mdr_adrbusiness where ReportDate>='%s' and ReportDate<='%s'" % (t1, t2))
    myconn.commit()
    mycu.execute("delete from mdr_faultbusiness where ReportDate>='%s' and ReportDate<='%s'" % (t1, t2))
    myconn.commit()
    mycu.execute("delete from mdr_icdbusiness where ReportDate>='%s' and ReportDate<='%s'" % (t1, t2))
    myconn.commit()
    mycu.execute("delete from mdr_devicebusiness where ReportDate>='%s' and ReportDate<='%s'" % (t1, t2))
    myconn.commit()
    mycu.execute("delete from mdr_errorlist where Date>='%s' and Date<='%s'" % (t1, t2))
    myconn.commit()

    mycu.execute("delete from mdr_reports where DateTag>='%s' and DateTag<='%s'" % (t1, t2))
    myconn.commit()
    # 删除新增加的不良事件评价信息表mdr_appraise数据刘欣毅20150831
    mycu.execute("delete from mdr_appraise where DateTag>='%s' and DateTag<='%s'" % (t1, t2))
    myconn.commit()
    # cur.execute('delete from  mdrlist')
    # con.commit()

    # mycu.close()
    # myconn.close()
    print u'原有数据删除结束，下面正在开始从新下载数据'


def clear_invalid_data(day):
    """
    清除某天无效的记录
    """
    recordCnt = 0
    myconn = myconnect()
    mycu = myconn.cursor()
    # 在主表中删除标记为己退回的报告
    mycu.execute(
        u"delete from mdr_business_gather where bianma in(select ReportID from mdr_fullidlist where SendDate='%s' and BackState='%s')" % (
        day, u'已退回'))
    recordCnt = mycu.rowcount
    myconn.commit()
    if recordCnt > 0:
        # 删除所有主表中已经删除的报告
        mycu.execute(
            "delete from mdr_adrbusiness where ReportDate='%s' and bianma not in(select bianma from mdr_business_gather where ReportDate='%s')" % (
            day, day))
        myconn.commit()
        mycu.execute(
            "delete from mdr_faultbusiness where ReportDate='%s' and bianma not in(select bianma from mdr_business_gather where ReportDate='%s')" % (
            day, day))
        myconn.commit()
        mycu.execute(
            "delete from mdr_icdbusiness where ReportDate='%s' and bianma not in(select bianma from mdr_business_gather where ReportDate='%s')" % (
            day, day))
        myconn.commit()
        mycu.execute(
            "delete from mdr_devicebusiness where ReportDate='%s' and bianma not in(select bianma from mdr_business_gather where ReportDate='%s')" % (
            day, day))
        myconn.commit()
        mycu.execute(
            "delete from mdr_errorlist where Date='%s' and ReportID not in(select bianma from mdr_business_gather where ReportDate='%s')" % (
            day, day))
        myconn.commit()
        mycu.execute(
            "delete from mdr_reports where DateTag='%s' and bianma not in(select bianma from mdr_business_gather where ReportDate='%s')" % (
            day, day))
        myconn.commit()
        # 删除新增加的不良事件评价信息表mdr_appraise数据刘欣毅20150831
        mycu.execute(
            "delete from mdr_appraise where DateTag='%s' and bianma not in(select bianma from mdr_business_gather where ReportDate='%s')" % (
            day, day))
        myconn.commit()

    print u'%s 无效记录清除完成！共清除%s条记录！' % (day, recordCnt)


# 以下2016.05.26新增
# 详情查看文档DX-1000001
# 功能说明：在临时表中查看已退回字段的编码，在主表中匹配编码标记为已退回
def check_back_data(day):

    # 重数据库里面把有已退回字段的编码取出来
    myconn = myconnect()
    mycu = myconn.cursor()
    sql = u"select BianMa from mdr_business_gather where bianma " \
          u"in(select ReportID from mdr_fullidlist where SendDate='%s' and BackState='%s')" % (day, u'已退回')
    result = mdr_select(sql)

    # 在MDR主表里面找到编码信息的记录，标记Reserve4字段为已退回
    num = 0
    for item in result:
        sql = u"update mdr_business_gather set Reserve4='%s' where bianma='%s'" % (u'已退回', item[0])
        mycu.execute(sql)
        myconn.commit()
        num += 1

    if num > 0:
        print u'%s 已退回%s条报表' % (day, num)


# 以下2016.05.26新增
# 详情查看文档DX-1000002
# 功能说明：对比一天的临时表跟主表的数量，如果有主表多，就写入mdr_business_gather_disappear里面
def check_disappear_data(day):

    # 获取俩个表的编码信息
    date = datetime.date.today()
    sql = "select bianma from mdr_business_gather where reportdate='%s'" % day
    diff_a = mdr_select(sql)
    sql = "select reportid from mdr_fullidlist where senddate='%s'" % day
    diff_b = mdr_select(sql)

    # 重新初始化编码信息，导入到俩个列表里面
    a = []
    b = []
    for i in diff_a:
        a.append(i[0])
    for i in diff_b:
        b.append(i[0].strip())

    # 通过比对算法，把a列表里面所有的b数据删除，最后a列表里面的数据是b列表里面没有的
    for i in range(len(b)):
        try:
            a.index(b[i])
            a.remove(b[i])
        except ValueError:
            pass

    # 进行判断，如果a列表里面有多余的数据，我们就移动到消失表里面，并且删除在主表和相关的表的数据
    if len(a) > 0:
        num = 0
        for i in range(len(a)):
            sql = "select bianma,reportunitname,reportdate,StateReportDate " \
                  "from mdr_business_gather where bianma='%s'" % a[i]
            diff_a = mdr_select(sql)
            sql = "INSERT into mdr_business_gather_disappear(bianma,reportunitname,reportdate,StateReportDate," \
                  "FoundTime) values('%s','%s','%s','%s','%s')" \
                  % (diff_a[0][0], diff_a[0][1], diff_a[0][2], diff_a[0][3], date)
            myconn = myconnect()
            mycu = myconn.cursor()
            mycu.execute(sql)
            myconn.commit()

            mycu.execute(u"delete from mdr_business_gather where bianma='%s'" % diff_a[0][0])
            myconn.commit()
            mycu.execute("delete from mdr_adrbusiness where bianma='%s'" % diff_a[0][0])
            myconn.commit()
            mycu.execute("delete from mdr_faultbusiness where bianma='%s'" % diff_a[0][0])
            myconn.commit()
            mycu.execute("delete from mdr_icdbusiness where bianma='%s'" % diff_a[0][0])
            myconn.commit()
            mycu.execute("delete from mdr_devicebusiness where bianma='%s'" % diff_a[0][0])
            myconn.commit()
            mycu.execute("delete from mdr_errorlist where reportid='%s'" % diff_a[0][0])
            myconn.commit()
            mycu.execute("delete from mdr_reports where bianma='%s'" % diff_a[0][0])
            myconn.commit()
            mycu.execute("delete from mdr_appraise where bianma='%s'" % diff_a[0][0])
            myconn.commit()
            num += 1
        print u'%s的消失记录移动完毕！共移动%s条记录！' % (day, num)
