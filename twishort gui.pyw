import requests
import wx
import re
import twishort
url_re = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?]))")

url_re2 = re.compile("(?:\w+://|www\.)[^ ,.?!#%=+][^ ]*")
bad_chars = "'\\.,[](){}:;\""


def find_urls_in_text(text):
 return [s.strip(bad_chars) for s in url_re2.findall(text)]

def convertTwishortToText(link):
	link=find_urls_in_text(link)
	link=twishort.unshorten(link[0])
	uri=twishort.get_twishort_uri(link)
	text=twishort.get_full_text(uri)
	return text

class Frame(wx.Frame):
	def __init__(self, title):
		wx.Frame.__init__(self, None, title=title, size=(350,200))
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		panel = wx.Panel(self)
		box = wx.BoxSizer(wx.VERTICAL)
		self.m_link_label = wx.StaticText(panel, -1, "Enter a twishort link or a tweet containing the twishort link")
		self.m_link = wx.TextCtrl(panel, -1, "")
		box.Add(self.m_link, 0, wx.ALL, 10)
		self.m_contents_label = wx.StaticText(panel, -1, "Contents")
		self.m_contents = wx.TextCtrl(panel, -1, "",style=wx.TE_READONLY)
		box.Add(self.m_contents, 0, wx.ALL, 10)
		self.m_add = wx.Button(panel, -1, "Convert Twishort")
		self.m_add.Bind(wx.EVT_BUTTON, self.Convert)
		box.Add(self.m_add, 0, wx.ALL, 10)
		self.m_close = wx.Button(panel, wx.ID_CLOSE, "Cancel")
		self.m_close.Bind(wx.EVT_BUTTON, self.OnClose)
		box.Add(self.m_close, 0, wx.ALL, 10)
		panel.Layout()
	def Convert(self,event):
		self.linktxt=self.m_link.GetValue()
		if self.linktxt!="":
			l=convertTwishortToText(self.linktxt)

			self.m_contents.SetValue(l)
			self.m_contents.SetFocus()

	def OnClose(self, event):
		self.Destroy()
app = wx.App(redirect=False)
window=Frame("Twishort GUI")
window.Show()
app.MainLoop()