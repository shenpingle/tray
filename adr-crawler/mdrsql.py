#-*- coding:utf-8 -*-
###########################################################################################
#  author: luu
#  info:封装mysql的操作
#  Revision: 1.0
"""
    功能说明：  封装mysql的操作

"""
###########################################################################################
from config import *

def mdr_dict_query(sql):
    myconn = myconnect()
    mycu = myconn.cursor(dictionary=True)
    mycu.execute(sql)
    backdata = mycu.fetchall()
    return backdata

def mdr_select(sql):
    #
    myconn = myconnect()
    mycu = myconn.cursor()
    mycu.execute(sql)
    backdata = mycu.fetchall()
    return backdata

def mdr_insert(sql, data):
    #
    myconn = myconnect()
    mycu = myconn.cursor()
    mycu.executemany(sql, data)
    myconn.commit()
    return sql

def mdr_insert_alone(sql, data):
    #
    myconn = myconnect()
    mycu = myconn.cursor()
    mycu.execute(sql, data)
    myconn.commit()
    return sql

def mdr_update(sql, data):
    #update
    myconn = myconnect()
    mycu = myconn.cursor()
    mycu.executemany(sql, data)
    myconn.commit()

    return sql

def mdr_update_alone(sql, data):
    #update
    myconn = myconnect()
    mycu = myconn.cursor()
    mycu.execute(sql, data)
    myconn.commit()

    return sql

def mdr_delete_alone(sql):
    #update
    myconn = myconnect()
    mycu = myconn.cursor()
    mycu.execute(sql)
    myconn.commit()

    return sql

if __name__ == '__main__':
    #
    sql_select = "SELECT BianMa FROM `mdr_business_gather` LIMIT 1000"
    out = mdr_select(sql_select)
    print out
    value = tuple(out)
    print value

    for abc in out:
        print abc[0]

    #"update mdr_business_gather set  IsnotifyUnit= %s,IsnotifyFactory= %s where BianMa=%s", (_t1,_t2, r_5)
    update_sql = "update mdr_checklist set Item =%s"
    update_data = [(1,), (2,), (3,), (4,), (5,), (6,),
                   (21,), (22,), (23,), (24,), (25,), (26,),
                   (31,), (32,), (33,), (34,), (35,), (36,),
                   (41,), (42,), (43,), (44,), (45,), (46,),
                   (51,),(52,),(53,),(54,),(55,),(56,),
                   (61,),(62,),(63,),(64,),(65,),(66,),
                   (71,),(72,),(73,),(74,),(75,),(76,),
                   (81,),(82,),(83,),(84,),(85,),(86,),
                   (91,),(92,),(93,),(94,),(95,),(96,),
                   (111,),(112,),(113,),(114,),(115,),(116,),
                   (221,),(222,),(223,),(224,),(225,)
                   ]
    mdr_update(update_sql,update_data)
