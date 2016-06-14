#-*- coding:utf-8 -*-
import wx
import ConfigParser

def str_to_unicode(text, encoding=None, errors='strict'):
    """Return the unicode representation of text in the given encoding. Unlike
    .encode(encoding) this function can be applied directly to a unicode
    object without the risk of double-decoding problems (which can happen if
    you don't use the default 'ascii' encoding)
    """

    if encoding is None:
        encoding = 'utf-8'
    if isinstance(text, str):
        return text.decode(encoding, errors)
    elif isinstance(text, unicode):
        return text
    else:
        raise TypeError('str_to_unicode must receive a str or unicode object, got %s' % type(text).__name__)

def readini_path():
    config = ConfigParser.ConfigParser()
    config.readfp(open('path.ini'))
    a = config.get("dir", "path")
    return a

def writeini_path(somedata):
    #
    config = ConfigParser.ConfigParser()
    # set a number of parameters
    config.add_section("dir")
    config.set("dir", "path", somedata)
    # write to file
    config.write(open('path.ini', "w"))

class pathDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(440, 300))

        self.panel = wx.Panel(self)
        wx.StaticText(self.panel, -1, u"请选择附件下载文件保存路径", pos=(10, 30))
        b = wx.Button(self.panel, -1, u"选择", (130,55))
        wx.StaticText(self.panel, -1, u"保存路径", pos=(10, 90))
        #self, style=wx.TE_MULTILINE, pos=(15, 60), size=(600, 360)
        self.path = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE, size=(175, -1), pos=(100, 90))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)
        self.Centre()

    # In this case we include a "New directory" button.
    def OnButton(self, evt):
        dlg = wx.DirDialog(self, "Choose a directory:",
                          style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )

        # If the user selects OK, then we process the dialog's data.
        # This is done by getting the path data from the dialog - BEFORE
        # we destroy it.
        if dlg.ShowModal() == wx.ID_OK:
            #self.log.WriteText('You selected: %s\n' % dlg.GetPath())
            mypath = dlg.GetPath()
            mypath = mypath.replace( r'\\', r'\\\\')
            #print "mypath", mypath
            import os
            path2 = mypath.split(os.path.sep)
            #print "path2:",path2
            path3 = u"\\".join(path2)
            print "path3:", path3
            #mypath_utf_8 =mypath.decode("utf-8").encode("utf-8")
            writeini_path(path3)
            #os.path.sep
            #os.sep
            #mypath = self.path.GetValue()
        #self.path.AppendText(self.path.GetValue())

            self.path.AppendText(path3)
        # Only destroy a dialog after you're done with it.
        #dlg.Destroy()

if __name__ == '__main__':
    app = wx.App(0)
    pathDialog(None, -1, u'查询')
    #print MySelectDays.dpc1
    app.MainLoop()