# -*- coding: utf-8 -*-
###########################################################################################
#  author: luu
#  info:任意月份选择窗体
#  Revision: 1.0
"""
    功能说明：  任意月份选择窗体

"""
###########################################################################################
import wx
import time
#---------------------------------------------------------------------------
APP_SIZE_X = 300
APP_SIZE_Y = 250

import ConfigParser

def readini_year():
    config = ConfigParser.ConfigParser()
    config.readfp(open('select_year.ini'))
    a = config.get("time", "year")
    return a

def readini_month():
    config = ConfigParser.ConfigParser()
    config.readfp(open('select_month.ini'))
    a = config.get("time", "month")
    return a

def readini_month2():
    config = ConfigParser.ConfigParser()
    config.readfp(open('select_month2.ini'))
    a = config.get("time", "month")
    return a

def writeini_year(somedata):
    #
    config = ConfigParser.ConfigParser()
    config.add_section("time")
    config.set("time", "year", somedata)
    config.write(open('select_year.ini', "w"))

def writeini_month(somedata):
    #
    config = ConfigParser.ConfigParser()
    config.add_section("time")
    config.set("time", "month", somedata)
    config.write(open('select_month.ini', "w"))

def writeini_month2(somedata):
    #
    config = ConfigParser.ConfigParser()
    config.add_section("time")
    config.set("time", "month", somedata)
    config.write(open('select_month2.ini', "w"))

class MySelectMonth(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(APP_SIZE_X, APP_SIZE_Y))

        self.panel = wx.Panel(self)
        self.mymonth = None
        self.mymonth2 = None
        self.myyear = None

        ThisYear = time.strftime('%Y-%m-%d', time.localtime(time.time()))[0:4]
        #print type(ThisYear)

        YaerList = []
        MonthList = []

        for y in range(2006, int(ThisYear)+1):
            #
            YaerList.append(str(y))
        for x in range(1, 13):
            #
            MonthList.append(str(x))

        wx.StaticText(self, -1, u"选择下面的年份和月份", (80, 10))
        wx.StaticText(self, -1, u"年份选择:", (15, 50), (75, 18))

        # This combobox is created with a preset list of values.
        #wx.Choice
        """
        cb = wx.ComboBox(self, 500, u"", (90, 50), (160, -1), YaerList, wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.EvtYear, cb)

        wx.StaticText(self, -1, u"开始月份:", (15, 80), (75, 18))
        cb2 = wx.ComboBox(self, 500, u"", (90, 80), (160, -1), MonthList, wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.EvtMonth, cb2)
        wx.StaticText(self, -1, u"结束月份:", (15, 110), (75, 18))
        cb3 = wx.ComboBox(self, 500, u"", (90, 110), (160, -1), MonthList, wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.EvtMonth2, cb3)

        """

        cb = wx.Choice(self, -1, (90, 50), choices=YaerList)
        self.Bind(wx.EVT_CHOICE, self.EvtYear, cb)

        wx.StaticText(self, -1, u"开始月份:", (15, 80), (75, 18))
        cb2 = wx.Choice(self, -1, (90, 80), choices=MonthList)
        self.Bind(wx.EVT_CHOICE, self.EvtMonth, cb2)
        wx.StaticText(self, -1, u"结束月份:", (15, 110), (75, 18))
        cb3 = wx.Choice(self, -1, (90, 110), choices=MonthList)
        self.Bind(wx.EVT_CHOICE, self.EvtMonth2, cb3)

        self.button = wx.Button(self, label=u'确定', pos=(60, 150), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnSure, self.button)

        self.button = wx.Button(self, label=u'退出', pos=(160, 150), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnMyClose, self.button)

        self.Centre()
        self.ShowModal()

    def EvtYear(self, evt):
        self.myyear = evt.GetString()
        print 'Year: %s\n' % self.myyear
        writeini_year(self.myyear)
        evt.Skip()

    def EvtMonth(self, evt):
        self.mymonth = evt.GetString()
        print 'Strat: %s\n' % self.mymonth
        writeini_month(self.mymonth)
        evt.Skip()

    def EvtMonth2(self, evt):
        self.mymonth2 = evt.GetString()
        #print type(mymonth)
        print 'Ending: %s\n' % self.mymonth2
        nima = int(self.mymonth) > int(self.mymonth2)
        #print nima
        if nima:
            wx.MessageBox(u'开始月份不能大于或者等于结束月份', u'警告', wx.OK | wx.ICON_INFORMATION)
        else:
            writeini_month2(self.mymonth2)
        evt.Skip()

    def OnMyClose(self, evt):
        #self.Destroy()
        self.Hide()

    def OnSure(self, event):
        self.Hide()

if __name__ == '__main__':
    app = wx.App()
    frame = MySelectMonth(None, -1, u'任意月份选择')
    #frame.Show()
    app.MainLoop()