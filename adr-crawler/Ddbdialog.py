# -*- coding: utf-8 -*-
###########################################################################################
#  author: luu
#  info:数据库参数输入窗体
#  Revision: 1.0
"""
    功能说明：   数据库参数输入窗体

"""
###########################################################################################

import wx
import os
import configxml

def GenerateXml(puser,pps,phost,pdbname):
    #
    import xml.dom.minidom
    import base64
    puser = base64.b64encode(puser)
    pps = base64.b64encode(pps)
    phost = base64.b64encode(phost)
    pdbname = base64.b64encode(pdbname)
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'mysqlcongig', None)
    root = dom.documentElement
    employee = dom.createElement('dbconfigs')
    root.appendChild(employee)

    userE = dom.createElement('user')
    userT = dom.createTextNode(puser)
    userE.appendChild(userT)
    employee.appendChild(userE)

    psE = dom.createElement('ps')
    psT = dom.createTextNode(pps)
    psE.appendChild(psT)
    employee.appendChild(psE)

    hostE = dom.createElement('host')
    hostT = dom.createTextNode(phost)
    hostE.appendChild(hostT)
    employee.appendChild(hostE)

    dbnameE = dom.createElement('dbname')
    dbnameT = dom.createTextNode(pdbname)
    dbnameE.appendChild(dbnameT)
    employee.appendChild(dbnameE)

    try:
        os.remove('dbnew.xml')
    except WindowsError:
        pass

    f = open('dbnew.xml', 'w')
    dom.writexml(f, addindent='  ', newl='\n', encoding='utf-8')
    f.close()

class DBCDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 200))
        self.panel = wx.Panel(self)

        userLabel = wx.StaticText(self.panel, -1, u"用户名:", pos=(10, 10))
        self.userText = wx.TextCtrl(self.panel, -1, size=(175, -1), pos=(100, 10))

        pwdLabel = wx.StaticText(self.panel, -1, u"密码:", pos=(10, 40))
        self.pwdText = wx.TextCtrl(self.panel, -1, size=(175, -1), pos=(100, 40), style=wx.TE_PASSWORD)

        hostLabel = wx.StaticText(self.panel, -1, u"数据库IP:", pos=(10, 70))
        self.hostText = wx.TextCtrl(self.panel, -1, size=(175, -1), pos=(100, 70))

        dbLabel = wx.StaticText(self.panel, -1, u"数据库名字:", pos=(10, 100))
        self.dbText = wx.TextCtrl(self.panel, -1, size=(175, -1), pos=(100, 100))

        button = wx.Button(self.panel, label=u'测试', pos=(120, 130), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnTestWindow, button)

        button1 = wx.Button(self.panel, label=u'退出', pos=(180, 130), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnMyClose, button1)

        self.Centre()

    def OnTestWindow(self, event):
        #
        user = self.userText.GetValue()
        pwd = self.pwdText.GetValue()
        host = self.hostText.GetValue()
        db = self.dbText.GetValue()
        #print user, pwd, host, db
        GenerateXml(user, pwd, host, db)

        if configxml.mysqlme():
            #
            wx.MessageBox(u'数据库连接成功', u'数据库测试', wx.OK | wx.ICON_INFORMATION)
        else:
            #
            wx.MessageBox(u'数据库连接失败，请重新检查输入数据', u'数据库测试', wx.OK | wx.ICON_INFORMATION)

    def OnMyClose(self, event):
        #
        self.Hide()