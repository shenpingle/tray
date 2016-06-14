#coding=utf-8
###########################################################################################
#  author: luu
#  info:任意天数选择窗体
#  Revision: 1.0
"""
    功能说明：  任意天数选择窗体

"""
###########################################################################################
import wx
import os
import time
import  wx.calendar as wxcal
import ConfigParser
APP_SIZE_X = 300
APP_SIZE_Y = 200

def readini_s():
    config = ConfigParser.ConfigParser()
    config.readfp(open('timeconfig_start.ini'))
    a = config.get("time", "start")
    return a

def readini_e():
    config = ConfigParser.ConfigParser()
    config.readfp(open('timeconfig_end.ini'))
    a = config.get("time", "end")
    return a

def writeini_s(somedata):
    #
    config = ConfigParser.ConfigParser()
    # set a number of parameters
    config.add_section("time")
    config.set("time", "start", somedata)
    # write to file
    config.write(open('timeconfig_start.ini', "w"))

def writeini_e(somedata):
    #
    config = ConfigParser.ConfigParser()
    # set a number of parameters
    config.add_section("time")
    config.set("time", "end", somedata)
    # write to file
    config.write(open('timeconfig_end.ini', "w"))

def _pydate2wxdate(date):
     import datetime
     assert isinstance(date, (datetime.datetime, datetime.date))
     tt = date.timetuple()
     dmy = (tt[2], tt[1]-1, tt[0])
     return wx.DateTimeFromDMY(*dmy)

def _wxdate2pydate(date):
    import datetime
    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        ymd = map(int, date.FormatISODate().split('-'))
        return datetime.date(*ymd)
    else:
        return None

class MySelectDays(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(APP_SIZE_X, APP_SIZE_Y))

        self.panel = wx.Panel(self)

        wx.Button(self, 1, u'确定', (50, 130))
        start = wx.StaticText(self, -1, u'开始时间:')
        end = wx.StaticText(self, -1, u'结束时间:')

        sizer = wx.GridBagSizer(4, 4)
        """
        dpc1 = wx.GenericDatePickerCtrl(
            self, size=(120, -1),
            style = wx.TAB_TRAVERSAL
            | wx.DP_DROPDOWN
            | wx.DP_SHOWCENTURY
            | wx.DP_ALLOWNONE
        )
        """
        dpc1 = wx.GenericDatePickerCtrl(
            self, size=(120, -1)
        )
        dpc2 = wx.GenericDatePickerCtrl(
            self, size=(120, -1),
            style = wx.TAB_TRAVERSAL
            | wx.DP_DROPDOWN
            | wx.DP_SHOWCENTURY
            | wx.DP_ALLOWNONE
        )

        self.Bind(wx.EVT_BUTTON, self.OnClose, id=1)
        #EVT_LEFT_DOWN
        self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged, dpc1)
        self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged2, dpc2)

        sizer.Add(start, pos=(1, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        sizer.Add(dpc1, pos=(1, 1), flag=wx.LEFT, border=0)
        sizer.Add(end, pos=(2, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        sizer.Add(dpc2, pos=(2, 1), flag=wx.LEFT, border=0)
        sizer.AddGrowableRow(2)
        sizer.AddGrowableCol(1)

        self.SetSizer(sizer)
        self.Centre()
        self.ShowModal()
        #self.Destroy()
 
    def OnClose(self, evt):
        self.Close(True)

    def OnDateChanged(self, evt):
        start = evt.GetDate().FormatISODate()
        print "OnDateChanged: %s\n" % start
        writeini_s(start)
        #FormatISODate
        #FormatISOTime

    def OnDateChanged2(self, evt):
        end = evt.GetDate().FormatISODate()
        print "OnDateChanged: %s\n" % end
        writeini_e(end)

if __name__ == '__main__':
    app = wx.App(0)
    MySelectDays(None, -1, u'任意天数选择')
    #print MySelectDays.dpc1
    app.MainLoop()