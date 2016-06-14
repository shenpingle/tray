#-*- coding:utf-8 -*-
import wx
import wx.grid as gridlib
import mdrsql


class QueryDlg(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(880, 600))

        panel = wx.Panel(self)
        self.myGrid = gridlib.Grid(panel)
        self.myGrid.CreateGrid(1000, 5)

        cbtn = wx.Button(panel, label=u'查询', pos=(738, 240))
        cbtn.Bind(wx.EVT_BUTTON, self.OnQuery)

        cbtn = wx.Button(panel, label=u'下载', pos=(738, 300))
        cbtn.Bind(wx.EVT_BUTTON, self.OnDown)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.myGrid)
        panel.SetSizer(sizer)

    def OnQuery(self, e):
        #wx.grid
        self.myGrid.Refresh()
        for x in range(0, 500):
            #print data[x]
            for y in range(0, 3):
                self.myGrid.SetCellValue(x, y, '')
                #print myGrid.GetCellValue(x, y)
        query_sql = "select ReportID, FileID,ShowFileName BackUp1 from pusr_dwfinfo_down_error limit 500 "
        #query_sql = "select FileType,UploadDepartmentName,FileSize,FileID,ShowFileName from pusr_dwfinfo_down limit 100 "
        query_set = mdrsql.mdr_select(query_sql)
        id = len(query_set)

        for x in range(0, id):
            #print data[x]
            for y in range(0, 3):
                outdata = query_set[x][y]
                self.myGrid.SetCellValue(x, y, outdata)

    def OnDown(self, e):
        #
        import psur_extradownload
        import threading
        t = threading.Thread(target=psur_extradownload.extradown)
        t.start()

if __name__ == '__main__':
    app = wx.App(0)
    QueryDlg(None, -1, u'查询')
    #print MySelectDays.dpc1
    app.MainLoop()