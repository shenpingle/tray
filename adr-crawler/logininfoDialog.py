#-*- coding:utf-8 -*-
import wx
import yaml

import hashlib

def mymd55(lorem):
    #lorem = '12345678'
    h = hashlib.md5()
    h.update(lorem)
    return h.hexdigest().upper()

class LoginInfoDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 200))
        self.panel = wx.Panel(self)

        userLabel = wx.StaticText(self.panel, -1, u"用户名:", pos=(10, 30))
        self.userText = wx.TextCtrl(self.panel, -1, pos=(80, 30), size=(175, -1))

        pwdLabel = wx.StaticText(self.panel, -1, u"密码:", pos=(10, 70))
        self.pwdText = wx.TextCtrl(self.panel, -1, pos=(80, 70), size=(175, -1), style=wx.TE_PASSWORD)

        button = wx.Button(self.panel, label=u'保存', pos=(120, 120), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnWriteInfo, button)

        button1 = wx.Button(self.panel, label=u'退出', pos=(180, 120), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnMyClose, button1)

        self.Centre()

    def OnWriteInfo(self, event):
        #
        user = self.userText.GetValue()
        pwd = self.pwdText.GetValue()
        ps2 = mymd55(pwd)
        
        data = dict(
            name = user,
            password = ps2
        )

        with open('logininfo.yml', 'w') as outfile:
            outfile.write( yaml.dump(data, default_flow_style=True) )

        print user, ps2

    def OnMyClose(self, event):
        #
        self.Destroy()

class Frame(wx.Frame):
    def __init__(
            self, parent=None, id=wx.ID_ANY, title=u'ADR下载', pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
            ):

        #self.taskBarIcon = TaskBarIcon(self)
        pass

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
    ldlg = LoginInfoDialog(None, -1, u'登录用户信息输入窗口')
    ldlg.ShowModal()
    app.MainLoop()

if __name__ == '__main__':
    TestFrame()        
