# -*- coding: utf-8 -*-
###########################################################################################
#  author: luu
#  info:托盘程序，封装界面和功能函数，主要包含main.py和main_adr.py
#  Revision: 1.0
#
#功能说明：  托盘程序，封装界面和功能函数，主要包含main.py和main_adr.py
###########################################################################################
import wx
import configxml
import os
import main
import mdrsql
import hashlib
#import multiprocessing
import main_adr
import checkitemmdr
import threading
import login_new_adr
from readconfig import readconfiginfo

from readyaml import readlogininfo

executeflag = 0

def mymd55(lorem):
    #lorem = '12345678'
    h = hashlib.md5()
    h.update(lorem)
    return h.hexdigest()

class LoginDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 200))
        self.panel = wx.Panel(self)

        userLabel = wx.StaticText(self.panel, -1, u"用户名:", pos=(10, 30))
        self.userText = wx.TextCtrl(self.panel, -1, pos=(80, 30), size=(175, -1))

        pwdLabel = wx.StaticText(self.panel, -1, u"密码:", pos=(10, 70))
        self.pwdText = wx.TextCtrl(self.panel, -1, pos=(80, 70), size=(175, -1), style=wx.TE_PASSWORD)

        button = wx.Button(self.panel, label=u'登录', pos=(120, 120), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnTestWindow, button)

        button1 = wx.Button(self.panel, label=u'退出', pos=(180, 120), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnMyClose, button1)

        self.Centre()

    def OnTestWindow(self, event):
        #
        user = self.userText.GetValue()
        pwd = self.pwdText.GetValue()
        ps2 = mymd55(pwd)

        print user, ps2
        select_sql = "SELECT LoginName,PassWord FROM `mhisuser`  where (Role='4' or Role='3')  and LoginName='%s' and `PassWord`='%s'"  % (user, ps2)
        dbok = mdrsql.mdr_select(select_sql)
        #print dbok

        if True : #dbok:
            #
            wx.MessageBox(u'登录成功', u'登录测试', wx.OK | wx.ICON_INFORMATION)
            global executeflag
            executeflag = 1
            self.Hide()
        else:
            #
            wx.MessageBox(u'登录失败，请重新检查输入数据', u'登录测试', wx.OK | wx.ICON_INFORMATION)

    def OnMyClose(self, event):
        #
        global executeflag
        executeflag = 0
        self.Hide()

class TaskBarIcon(wx.TaskBarIcon):
    ID_Play = wx.NewId()
    ID_About = wx.NewId()
    ID_Minshow=wx.NewId()
    ID_Maxshow=wx.NewId()
    ID_Closeshow=wx.NewId()

    ID_Act_today = wx.NewId()
    ID_Act_anytime = wx.NewId()
    ID_Act_thisweek = wx.NewId()
    ID_Act_lastweek = wx.NewId()
    ID_Act_lastmonth = wx.NewId()
    ID_Act_byear = wx.NewId()
    ID_Act_ayear = wx.NewId()
    ID_Act_lastyear = wx.NewId()

    ID_Act_today_adr = wx.NewId()
    ID_Act_anytime_adr = wx.NewId()
    ID_Act_thisweek_adr = wx.NewId()
    ID_Act_lastweek_adr = wx.NewId()
    ID_Act_lastmonth_adr = wx.NewId()
    ID_Act_byear_adr = wx.NewId()
    ID_Act_ayear_adr = wx.NewId()
    ID_Act_lastyear_adr = wx.NewId()

    ID_Act_config = wx.NewId()
    ID_Act_configtime = wx.NewId()
    ID_Act_autocheck = wx.NewId()
    ID_Act_autocheck_adr = wx.NewId()

    ID_Act_checklist_mdr = wx.NewId()
    ID_Act_checklist_adr = wx.NewId()

    ID_Act_Host_mdr = wx.NewId()
    ID_Act_LoginInfo = wx.NewId()

    ID_Act_psur = wx.NewId()
    ID_Act_psur_query = wx.NewId()
    ID_Act_psur_path = wx.NewId()

    ID_Act_Mdr_Appraise = wx.NewId()
    ID_Act_Adr_Appraise = wx.NewId()


    def __init__(self, frame):
        self.P = []
        self.count = 0

        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon(name='wx.ico', type=wx.BITMAP_TYPE_ICO), u'ADR下载!')  #wx.ico为ico图标文件
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.ID_About)
        self.Bind(wx.EVT_MENU, self.OnCloseshow, id=self.ID_Closeshow)

        self.Bind(wx.EVT_MENU, self.OnToday, id=self.ID_Act_today)
        self.Bind(wx.EVT_MENU, self.OnAnytime, id=self.ID_Act_anytime)
        self.Bind(wx.EVT_MENU, self.OnThisWeek, id=self.ID_Act_thisweek)
        self.Bind(wx.EVT_MENU, self.OnLastWeek, id=self.ID_Act_lastweek)
        self.Bind(wx.EVT_MENU, self.OnLastMonth, id=self.ID_Act_lastmonth)
        self.Bind(wx.EVT_MENU, self.OnAyear, id=self.ID_Act_ayear)
        self.Bind(wx.EVT_MENU, self.OnByear, id=self.ID_Act_byear)
        self.Bind(wx.EVT_MENU, self.OnLastYear, id=self.ID_Act_lastyear)

        self.Bind(wx.EVT_MENU, self.OnToday_adr, id=self.ID_Act_today_adr)
        self.Bind(wx.EVT_MENU, self.OnAnytime_adr, id=self.ID_Act_anytime_adr)
        self.Bind(wx.EVT_MENU, self.OnThisWeek_adr, id=self.ID_Act_thisweek_adr)
        self.Bind(wx.EVT_MENU, self.OnLastWeek_adr, id=self.ID_Act_lastweek_adr)
        self.Bind(wx.EVT_MENU, self.OnLastMonth_adr, id=self.ID_Act_lastmonth_adr)
        self.Bind(wx.EVT_MENU, self.OnAyear_adr, id=self.ID_Act_ayear_adr)
        self.Bind(wx.EVT_MENU, self.OnByear_adr, id=self.ID_Act_byear_adr)
        self.Bind(wx.EVT_MENU, self.OnLastYear_adr, id=self.ID_Act_lastyear_adr)

        self.Bind(wx.EVT_MENU, self.OnConfig, id=self.ID_Act_config)
        self.Bind(wx.EVT_MENU, self.Ontime, id=self.ID_Act_configtime)

        self.Bind(wx.EVT_MENU, self.Onautocheck, id=self.ID_Act_autocheck)
        self.Bind(wx.EVT_MENU, self.Onautocheck_adr, id=self.ID_Act_autocheck_adr)

        self.Bind(wx.EVT_MENU, self.OnCheckList_adr, id=self.ID_Act_checklist_adr)
        self.Bind(wx.EVT_MENU, self.OnCheckList_mdr, id=self.ID_Act_checklist_mdr)

        self.Bind(wx.EVT_MENU, self.OnHost_mdr, id=self.ID_Act_Host_mdr)
        self.Bind(wx.EVT_MENU, self.OnLoginInfo, id=self.ID_Act_LoginInfo)

        self.Bind(wx.EVT_MENU, self.OnPsurMain, id=self.ID_Act_psur)
        self.Bind(wx.EVT_MENU, self.OnPsurQuery, id=self.ID_Act_psur_query)
        self.Bind(wx.EVT_MENU, self.OnPsurPath, id=self.ID_Act_psur_path)

        self.Bind(wx.EVT_MENU, self.OnMdrAppraise, id=self.ID_Act_Mdr_Appraise)
        self.Bind(wx.EVT_MENU, self.OnAdrAppraise, id=self.ID_Act_Adr_Appraise)
    #bad
    #new mdr24.py
    def OnHost_mdr(self, event):
        #
        pass
    def OnLoginInfo(self, event):
        import logininfoDialog
        dbcdlg = logininfoDialog.LoginInfoDialog(None, -1, u'登录用户信息输入窗口')
        dbcdlg.ShowModal()
    #bad
    def OnCheckList_adr(self, event):
        #
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"自动核查（ADR）:", executeflag
        if executeflag == 1:
            import sd4
            sd4.MySelectMonth(None, -1, u'任意月份选择')
            ty = sd4.readini_year()
            tmstart = sd4.readini_month()
            tmending = sd4.readini_month2()
            executeflag = 0
            #import zoe3
            #t = threading.Thread(target=zoe3.main3, args=(ty, tmstart, tmending))
            import adr_regulate
            t = threading.Thread(target=adr_regulate.adr_regulate, args=(ty, tmstart, tmending))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    #yup
    def OnCheckList_mdr(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"自动核查（MDR）:", executeflag
        if executeflag == 1:
            import sd4
            sd4.MySelectMonth(None, -1, u'任意月份选择')
            ty = sd4.readini_year()
            tmstart = sd4.readini_month()
            tmending = sd4.readini_month2()
            executeflag = 0
            import zoe2
            t = threading.Thread(target=zoe2.RegulateMdrData, args=(ty, tmstart, tmending))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    #bad
    def OnToday(self, event):
        #
        pass

    #yup
    def OnAnytime(self, event):
        #
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"任意时间下载（MDR）:", executeflag
        if executeflag == 1:
            import sd3
            sd3.MySelectDays(None, -1, u'任意天数选择')
            t1 = sd3.readini_s()
            print "t1:", t1
            t2 = sd3.readini_e()
            print "t2:", t2
            executeflag = 0
            t = threading.Thread(target=main.crawler_anytime2, args=(t1, t2))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"
    #yup
    def OnThisWeek(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"本周下载（MDR）:", executeflag
        if executeflag == 1:
            executeflag = 0
            t = threading.Thread(target=main.crawler_current_week)
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    #yup
    def OnLastWeek(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"上周下载（MDR）:", executeflag
        if executeflag == 1:
            executeflag = 0
            t = threading.Thread(target=main .crawler_last_week)
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    #yup
    def OnLastMonth(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"上月下载（MDR）:", executeflag
        if executeflag == 1:
            executeflag = 0
            t = threading.Thread(target=main.crawler_last_month)
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"
    #yup
    def OnAyear(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"下半年度下载（MDR）:", executeflag
        if executeflag == 1:
            executeflag = 0
            t = threading.Thread(target=main.crawler_second_half_year)
            self.P.append(t)
            t.start()
            #main.crawler_second_half_year()
        else:
            print u"一些东西出错了"

    #yup
    def OnByear(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"上半年度下载（MDR）:", executeflag
        if executeflag == 1:
            executeflag = 0
            t = threading.Thread(target=main.crawler_first_half_year)
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    #yup
    def OnLastYear(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"上一年度下载（MDR）:", executeflag
        if executeflag == 1:
            executeflag = 0
            t = threading.Thread(target=main.crawler_last_year())
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"
    #bad
    def OnToday_adr(self, event):
        #
        pass
    #yup
    def OnAnytime_adr(self, event):
        #
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()
        import crawler_by_time_adr
        global executeflag
        print u"任意时间下载（ADR）:", executeflag
        if executeflag == 1:
            import sd3
            sd3.MySelectDays(None, -1, u'任意天数选择')
            t1 = sd3.readini_s()
            print "t1:", t1
            t2 = sd3.readini_e()
            print "t2:", t2
            executeflag = 0
            somedata = readlogininfo()
            name = somedata[0]
            password = somedata[1]
            t = threading.Thread(target=crawler_by_time_adr.crawler_by_time, args=(name, password, t1, t2))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"
    #yup
    def OnThisWeek_adr(self, event):
        #
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"本周下载（ADR）:", executeflag
        if executeflag == 1:
            executeflag = 0
            somedata = readlogininfo()
            name = somedata[0]
            password = somedata[1]
            t = threading.Thread(target=main_adr.crawler_current_week, args=(name, password))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    #yup
    def OnLastWeek_adr(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"上周下载（ADR）:", executeflag
        if executeflag == 1:
            executeflag = 0
            somedata = readlogininfo()
            name = somedata[0]
            password = somedata[1]
            t = threading.Thread(target=main_adr.crawler_last_week, args=(name, password))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    #yup
    def OnLastMonth_adr(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"上月下载（ADR）:", executeflag
        if executeflag == 1:
            executeflag = 0
            somedata = readlogininfo()
            name = somedata[0]
            password = somedata[1]
            t = threading.Thread(target=main_adr.crawler_last_month, args=(name, password))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"
    #yup
    def OnAyear_adr(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"下半年度下载（ADR）:", executeflag
        if executeflag == 1:
            executeflag = 0
            somedata = readlogininfo()
            name = somedata[0]
            password = somedata[1]
            t = threading.Thread(target=main_adr.crawler_second_half_year, args=(name, password))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"
    #yup
    def OnByear_adr(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"上半年度下载（ADR）:", executeflag
        if executeflag == 1:
            executeflag = 0
            somedata = readlogininfo()
            name = somedata[0]
            password = somedata[1]
            t = threading.Thread(target=main_adr.crawler_first_half_year, args=(name, password))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    #yup
    def OnLastYear_adr(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"上一年度下载（ADR）:", executeflag
        if executeflag == 1:
            executeflag = 0
            somedata = readlogininfo()
            name = somedata[0]
            password = somedata[1]
            t = threading.Thread(target=main_adr.crawler_last_year, args=(name, password))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    #yup
    def OnConfig(self, event):
        import Ddbdialog
        dbcdlg = Ddbdialog.DBCDialog(None, -1, u'数据库配置')
        dbcdlg.ShowModal()
    #yup
    def Ontime(self, event):
        import datepicker
        datepicker.MyForm(None, -1, u'任意时间段选择')
        print u'7x24执行时间配置'

    def Onautocheck(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"获取单月智能报表总数（MDR）:", executeflag
        if executeflag == 1:
            import sd4
            sd4.MySelectMonth(None, -1, u'任意月份选择')
            ty = sd4.readini_year()
            tmstart = sd4.readini_month()
            tmending = sd4.readini_month2()
            executeflag = 0
            t = threading.Thread(target=checkitemmdr.myauto, args=(ty, tmstart, tmending))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    def Onautocheck_adr(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"获取单月智能报表总数（ADR）:", executeflag
        if executeflag == 1:
            import sd4
            sd4.MySelectMonth(None, -1, u'任意月份选择')
            ty = sd4.readini_year()
            tmstart = sd4.readini_month()
            tmending = sd4.readini_month2()
            executeflag = 0
            t = threading.Thread(target=login_new_adr.checklistauto, args=(ty, tmstart,tmending))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    def OnPsurMain(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"PSUR:", executeflag
        if executeflag == 1:
            import sd3
            import psur
            sd3.MySelectDays(None, -1, u'任意天数选择')
            t1 = sd3.readini_s()
            print "t1:", t1
            t2 = sd3.readini_e()
            print "t2:", t2
            executeflag = 0
            t = threading.Thread(target=psur.autopsur, args=(t1, t2))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    def OnPsurQuery(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"PSUR 查询:", executeflag
        if executeflag == 1:
            
            import queryDlg
            querydlg = queryDlg.QueryDlg(None, -1, u'查询')
            querydlg.Show()
            
        else:
            print u"一些东西出错了"

    def OnPsurPath(self, event):
         import pathDlg
         pathdlg = pathDlg.pathDialog(None, -1, u'附件下载文件保存路径选择')
         pathdlg.ShowModal()


    def OnAbout(self,event):
        wx.MessageBox(u'香象科技智能机器人系统 Ver 2.0 Copyright@2010-2020 All Rights Reserved  \n版权所有,违者必究', u'香象科技智能机器人系统 Ver 2.0')


    def OnCloseshow(self,event):
        self.frame.Close(True)

    def OnMdrAppraise(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"更新再评价（MDR）:", executeflag
        if executeflag == 1:
            import sd4
            sd4.MySelectMonth(None, -1, u'任意月份选择')
            year = sd4.readini_year()
            start_month = sd4.readini_month()
            end_month = sd4.readini_month2()
            executeflag = 0
            import mdr_appraise
            t = threading.Thread(target=mdr_appraise.crawler_appraise, args=(year, start_month, end_month))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    def OnAdrAppraise(self, event):
        ldlg = LoginDialog(None, -1, u'登录窗口')
        ldlg.ShowModal()

        global executeflag
        print u"更新再评价（MDR）:", executeflag
        if executeflag == 1:
            import sd4
            sd4.MySelectMonth(None, -1, u'任意月份选择')
            year = sd4.readini_year()
            start_month = sd4.readini_month()
            end_month = sd4.readini_month2()
            executeflag = 0
            import adr_appraise
            t = threading.Thread(target=adr_appraise.crawler_appraise, args=(year, start_month, end_month))
            self.P.append(t)
            t.start()
        else:
            print u"一些东西出错了"

    # 右键菜单
    def CreatePopupMenu(self):

        menu = wx.Menu()
        #menu.Append(self.ID_Act_today, u'抓取今天')
        menu.Append(self.ID_Act_anytime, u'任意时间')
        menu.Append(self.ID_Act_thisweek, u'抓取本周')
        menu.Append(self.ID_Act_lastweek, u'抓取上周')
        menu.Append(self.ID_Act_lastmonth, u'抓取上月')
        menu.Append(self.ID_Act_byear, u'抓取上半年度')
        menu.Append(self.ID_Act_ayear, u'抓取下半年度')
        menu.Append(self.ID_Act_lastyear, u'抓取上一年度')
        menu.AppendSeparator()
        menu.Append(self.ID_Act_checklist_mdr, u'自动核查')
        menu.Append(self.ID_Act_autocheck, u"获取单月智能报表总数")
        menu.Append(self.ID_Act_Mdr_Appraise, u"更新再评价")

        menu_a = wx.Menu()
        #menu_a.Append(self.ID_Act_today_adr, u'抓取今天')
        menu_a.Append(self.ID_Act_anytime_adr, u'任意时间')
        menu_a.Append(self.ID_Act_thisweek_adr, u'抓取本周')
        menu_a.Append(self.ID_Act_lastweek_adr, u'抓取上周')
        menu_a.Append(self.ID_Act_lastmonth_adr, u'抓取上月')
        menu_a.Append(self.ID_Act_byear_adr, u'抓取上半年度')
        menu_a.Append(self.ID_Act_ayear_adr, u'抓取下半年度')
        menu_a.Append(self.ID_Act_lastyear_adr, u'抓取上一年度')
        menu_a.AppendSeparator()
        menu_a.Append(self.ID_Act_checklist_adr, u"自动核查")
        menu_a.Append(self.ID_Act_autocheck_adr, u"获取单月智能报表总数")
        menu_a.Append(self.ID_Act_Adr_Appraise, u"更新关联性评价")


        menu_b = wx.Menu()
        menu_b.Append(self.ID_About, u'关于')

        menu_c = wx.Menu()
        menu_c.Append(self.ID_Act_config, u'数据库参数配置')
        menu_c.Append(self.ID_Act_LoginInfo, u'登录用户信息配置')
        menu_c.Append(self.ID_Act_configtime, u'7x24执行时间配置')

        menu_d = wx.Menu()
        menu_d.Append(self.ID_Act_psur, u"Psur下载")
        menu_d.Append(self.ID_Act_psur_query, u"Psur 附件下载异常查询")
        menu_d.Append(self.ID_Act_psur_path, u"Psur 附件下载路径配置")

        fileMenu = wx.Menu()
        somedata = readconfiginfo()
        mdr = somedata[0]
        adr = somedata[1]
        psur = somedata[2]
        #print mdr,adr,psur
        if mdr:
            #
            fileMenu.AppendMenu(wx.ID_ANY, u"器械（MDR）", menu)
        if adr:
            #
            fileMenu.AppendMenu(wx.ID_ANY, u"药品（ADR）", menu_a)
        if psur:
            #
            fileMenu.AppendMenu(wx.ID_ANY, u"PSUR", menu_d)
        fileMenu.AppendMenu(wx.ID_ANY, u"配置参数", menu_c)
        fileMenu.AppendMenu(wx.ID_ANY, u"关于(2015v)", menu_b)

        return fileMenu

class Frame(wx.Frame):
    def __init__(
            self, parent=None, id=wx.ID_ANY, title=u'ADR下载', pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
            ):

        self.taskBarIcon = TaskBarIcon(self)

    def OnHide(self, event):
        self.Hide()
    def OnIconfiy(self, event):
        self.Hide()
        event.Skip()
    def OnClose(self, event):
        self.taskBarIcon.Destroy()
        self.Destroy()

def TestFrame():
    app = wx.App()
    #TaskBarIcon()
    Frame(size=(640, 480))
    app.MainLoop()

if __name__ == '__main__':
    TestFrame()