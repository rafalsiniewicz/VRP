import folium
import geocoder
import webbrowser
import webview
import os 
from PySide2 import *
import sys
from PySide2.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

g = geocoder.ip('me')
# Create a Map instance
m = folium.Map(location=[g.lat, g.lng],
    zoom_start=15, control_scale=True)

folium.Marker(
    location=[g.lat, g.lng],
    popup='You\'re here',
    icon=folium.Icon(color='green', icon='ok-sign'),
).add_to(m)
outfp = "map.html"
m.save(outfp)
#webview.create_window('Hello world', 'map.html')

app = QApplication(sys.argv)
#label = QLabel("Hello World!")
browser = QWebEngineView()
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.html"))
local_url = QUrl.fromLocalFile(file_path)
browser.load(local_url)

browser.show()
app.exec_()



#webbrowser.open_new_tab('map.html')
#webview.create_window('Todos magnificos', outfp)
'''import wx
import wx.html

class MyHtmlFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)
        html = wx.html.HtmlWindow(self)
        if "gtk2" in wx.PlatformInfo:
            html.SetStandardFonts()

        print(html.LoadFile(
            "map.html"))


app = wx.App()
frm = MyHtmlFrame(None, "Simple HTML")
frm.Show()
app.MainLoop()'''
