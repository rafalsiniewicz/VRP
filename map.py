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


CRACOW_CENTRE = {"CRACOW": [50.061681, 19.938104]}

def create_map(self, program):
	m = folium.Map(location=[CRACOW_CENTRE["CRACOW"][0], CRACOW_CENTRE["CRACOW"][1]],
	    zoom_start=15, control_scale=True)


	for place, position in program.GetPopulation().BestIndividual().Merge().items():
	    folium.Marker(
	        location=[position[0], position[1]],
	        popup='You\'re here',
	        icon=folium.Icon(color='green', icon='ok-sign'),
	    ).add_to(m)
	    outfp = "map.html"
	    m.save(outfp)
	#webview.create_window('Hello world', 'map.html')

	#app = QApplication(sys.argv)
	#label = QLabel("Hello World!")
	self.browser = QWebEngineView()
	file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.html"))
	local_url = QUrl.fromLocalFile(file_path)
	self.browser.load(local_url)

	self.browser.show()
	#sys.exit(app.exec_())

