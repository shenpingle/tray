#-*- coding:utf-8 -*-
###########################################################################################
#  author:touchluu2010@gmail.com
#  说明:连接数据库
#  Revision: 1.0
###########################################################################################
import mysql.connector
import xml.dom.minidom as minidom

def getTagText(root, tag):
    dom = minidom.parse("dbnew.xml")
    root = dom.documentElement
    node = root.getElementsByTagName(tag)[0]
    rc = ""
    for node in node.childNodes:
        if node.nodeType in (node.TEXT_NODE, node.CDATA_SECTION_NODE):
            rc = rc + node.data
    return rc

def dbinfo():
    #
    dom = minidom.parse("dbnew.xml")
    root = dom.documentElement
    myroot = getTagText(root, "user")
    myps = getTagText(root, "ps")
    myhost = getTagText(root, "host")
    mydbname = getTagText(root, "dbname")

    import base64
    myroot = base64.b64decode(myroot)
    myps = base64.b64decode(myps)
    myhost = base64.b64decode(myhost)
    mydbname = base64.b64decode(mydbname)
    return (myroot, myps, myhost, mydbname)
    #return ('root','12345678aA', '127.0.0.1','adrmanagement')
"""
dbconfig = dbinfo()
config = dict(user=dbconfig[0], password=dbconfig[1], host=dbconfig[2], database=dbconfig[3], raise_on_warnings=True)
try:
    myconn = mysql.connector.MySQLConnection(**config)
    mycu = myconn.cursor()
    assert isinstance(mycu, object)
except mysql.connector.errors.InterfaceError:
    pass
"""

"""
myconn = myconnect()
mycu = myconn.cursor()

"""
def myconnect():
    
    myconn = None
    dbconfig = dbinfo()
    config = dict(user=dbconfig[0], password=dbconfig[1], host=dbconfig[2], database=dbconfig[3], raise_on_warnings=True, charset="utf8")
    try:
        myconn = mysql.connector.connect(**config)
    except (mysql.connector.errors.ProgrammingError,mysql.connector.errors.InterfaceError), e:
        print e

    return myconn

