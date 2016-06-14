#-*- coding:utf-8 -*-
##############################################################################################
#
#   此文件包括数据库相关操作
#
##############################################################################################

from mysql.connector import *
import codecs
import re
import logging
import traceback
import sys
import config

import xml.dom.minidom as minidom

def getConnection():
    return config.myconnect()

def insert_to_table(tabName,data):
    '''把Dict插入数据库'''
    
    conn = getConnection()
    
    data = _check_date_value(data)
    
    del_keys = data.keys()
    for k in del_keys:
        if k.startswith("_"): #下划线打头的字段，不入库
            del data[k]
    
    sql = ""
    show_id = data["show_id"] if "show_id" in data else ""
    bianma = data["bianma"] if "bianma" in data else ""
    try:
        cur = conn.cursor()
        keys = data.keys()
        sql = "insert into " + tabName + "(" + (",".join(keys)) + ")values("
        values = []
        for k in keys:
            if isinstance(data[k],unicode):
                data[k] = data[k].encode("utf8")
            elif not isinstance(data[k],str):
                data[k] = str(data[k])
            values.append( "'" + data[k].replace("'","\’").strip() + "'")
        if isinstance(sql,unicode):
            sql = sql.encode("utf-8")
            
        sql += ",".join(values)
        
        sql += ");"
        
        cur.execute(sql)
        cur.close()
    except Exception as err :
        show_id = data["show_id"] if "show_id" in data else ""
        bianma = data["bianma"] if "bianma" in data else ""
        error_log = "show_id:%s\t bianma:%s" % (show_id, bianma)
        error_log += "error :%s \n sql: %s \n" % (err, sql )
        if not isinstance(error_log, unicode) :
            error_log = error_log.decode("utf-8")
        
        logging.info(error_log)
        
    conn.commit()
    conn.close()


  
def _check_date_value(row):
    re_date = re.compile(r'\d{4}-\d{2}-\d{2}', re.U)
    keys = ["happendate", "reportdate", "acceptdate", "statereportdate", "provincereportdate", 
        "trackdate", "birthday", "deathdate", "personappraisedate", "unitappraisedate",
        "basicappraisedate", "municipalappraisedate", "provinceappraisedate", "stateappraisedate" ]
    for key in keys:
        if key in row :
            match = re_date.match(row[key])
            if match :
                row[key] = match.group(0)
            else :
                del row[key]
    
    return row