#-*- coding:utf-8 -*-
###########################################################################################
#  author: luu
#  info:任意时间段选择dialog
#  Revision: 1.0
"""
    功能说明：   任意时间段选择dialog

"""
###########################################################################################

import wx
import wx.lib.scrolledpanel as scrolled
import wx.lib.masked as masked
import ConfigParser

########################################################################
def readini_minute():
    config = ConfigParser.ConfigParser()
    config.readfp(open('timeconfig_minute.ini'))
    a = config.get("time", "minute")
    return a

def writeini_minute(somedata):
    #
    config = ConfigParser.ConfigParser()
    # set a number of parameters
    config.add_section("time")
    config.set("time", "minute", somedata)
    # write to file
    config.write(open('timeconfig_minute.ini', "w"))

def readini_minute_adr():
    config = ConfigParser.ConfigParser()
    config.readfp(open('timeconfig_minute_adr.ini'))
    a = config.get("time", "minute")
    return a

def writeini_minute_adr(somedata):
    #
    config = ConfigParser.ConfigParser()
    # set a number of parameters
    config.add_section("time")
    config.set("time", "minute", somedata)
    # write to file
    config.write(open('timeconfig_minute_adr.ini', "w"))

ABC = 0

class MyForm(wx.Dialog):
    #----------------------------------------------------------------------
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 550))
        # Add a panel so it looks the correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)
        # --------------------
        # Scrolled panel stuff
        self.scrolled_panel = scrolled.ScrolledPanel(self.panel, -1,  style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="panel1")
        myseletetime = readini_minute()
        mytitle = u"上次设定时间:" + myseletetime+"  "+"ADR:"+readini_minute_adr()
        box_labelx = wx.StaticBox(self, -1, mytitle, pos=(25, 10))

        box_label = wx.StaticBox(self, -1, u"请确认选取的时间" )
        buttonbox = wx.StaticBoxSizer(box_label, wx.HORIZONTAL)
        #小时      格式
        text2 = wx.StaticText(self, -1, u"24-小时 格式:")
        spin2 = wx.SpinButton(self, -1, wx.DefaultPosition, (-1, 20), wx.SP_VERTICAL)
        self.time24 = masked.TimeCtrl(
            self, -1, name="24 hour control", fmt24hr=True,
            spinButton=spin2
        )

        grid = wx.FlexGridSizer(cols=2, hgap=10, vgap=5)

        grid.Add(text2, 0, wx.ALIGN_RIGHT | wx.TOP | wx.BOTTOM)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.time24, 0, wx.ALIGN_CENTRE)
        hbox2.Add(spin2, 0, wx.ALIGN_CENTRE)
        grid.Add(hbox2, 0, wx.LEFT)

        buttonChange = wx.Button(self, -1,  u"确认")
        buttonbox.Add(buttonChange, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(grid, 0, wx.ALIGN_LEFT | wx.ALL, 15)
        hbox.Add(buttonbox, 0, wx.ALIGN_RIGHT | wx.BOTTOM, 20)


        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((20, 20))
        vbox.Add(hbox, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        outer_box = wx.BoxSizer(wx.VERTICAL)
        outer_box.Add(vbox, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        sampleList = [u'MDR', u'ADR']

        #sizer = wx.BoxSizer(wx.VERTICAL)
        #(-1, -1)
        self.rb = wx.RadioBox(
                self, -1, u"配置设定", (10, 70), wx.DefaultSize,
                sampleList, 2, wx.RA_SPECIFY_COLS
                )
        self.rb.SetToolTip(wx.ToolTip(u"请选择一个选项"))
        #self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.rb)

        self.SetAutoLayout(True)
        self.SetSizer(outer_box)
        outer_box.Fit(self)

        self.Bind(wx.EVT_BUTTON, self.OnClose, buttonChange)
        self.Bind(masked.EVT_TIMEUPDATE, self.OnTimeChange, self.time24)

        self.Centre()
        self.ShowModal()
        self.Destroy()

    """
    def EvtRadioBox(self, event):
        #print wx.DefaultPosition
        global ABC
        keys = event.GetInt()
        if keys == 0:
            ABC = 2
        elif keys == 1:
            ABC = 3
    """
    def OnTimeChange(self, event):
        timectrl = self.FindWindowById(event.GetId())
        mytime = timectrl.GetValue()
        print u"设定时间:", mytime
        #GetSelection()
        print "GetSelection():", self.rb.GetSelection()
        mycpp  = self.rb.GetSelection()
        if mycpp == 0:
            print "MDR :", mycpp
            writeini_minute(mytime)
        elif mycpp == 1:
            print "ADR :", mycpp
            writeini_minute_adr(mytime)

    def OnClose(self, evt):
        self.Close(True)

    def OnButtonClick(self, event):
        """
        something
        """

# Run the program
if __name__ == "__main__":
        app = wx.App(0)
        MyForm(None, -1, u'任意时间段选择')
        app.MainLoop()