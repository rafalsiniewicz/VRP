#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QButtonGroup, QVBoxLayout, QPushButton, QScrollArea, QGroupBox
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5 import QtCore
from functools import partial
from program import *
import folium
import geocoder
import webbrowser
import webview
import os 
from PySide2 import *
import sys
from PySide2.QtWidgets import QApplication, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
import numpy as np
import pandas as pd
from collections import namedtuple
from networkx import *
from osmnx import *




CRACOW_CENTRE = {"CRACOW": [50.061681, 19.938104]}

def choose_color():
    return "#{:06x}".format(randint(0, 0xFFFFFF))

class App(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.program = Program()
        self.program.ImportData("krakow.json")
        #self.names = ["A", "B", "C", "D"]
        self.names = []
        for place,position in self.program.GetData().Get().items():
            self.names.append(place)
        self.program.SelectData(self.names)
        #self.program.InitializePopulation(3,100)
        #self.interface()
        self.initUI()


    def createLayout_group(self, number):
        sgroupbox = QGroupBox("Places".format(number), self)
        layout_groupbox = QVBoxLayout(sgroupbox)
        #print(len(self.program.GetNames()))
        for i in range(len(self.names)):
            item = QCheckBox(self.program.GetNames()[i], sgroupbox)
            layout_groupbox.addWidget(item)
            item.stateChanged.connect(self.checkBoxChangedAction)
            item.toggle()
        layout_groupbox.addStretch(1)
        return sgroupbox

    def createLayout_Container(self):
        self.scrollarea = QScrollArea(self)
        self.scrollarea.setFixedWidth(200)
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget()
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)

        for i in range(1):
            self.layout_SArea.addWidget(self.createLayout_group(i))
        self.layout_SArea.addStretch(1)

    def initUI(self):
        self.resize(640, 480)
        button = QPushButton('Calculate track', self)
        #button.setToolTip('This is an example button')
        button.move(300,70)
        button.clicked.connect(self.on_click)
        self.createLayout_Container()
        self.layout_All = QVBoxLayout(self)
        self.layout_All.addWidget(self.scrollarea)
        self.show()

    '''def interface(self):

        self.resize(640, 480)
        #self.setWindowTitle("")
        checkboxes = []
        for i in range(0,len(self.program.GetNames())):
            cb = QCheckBox(self.program.GetNames()[i], self)
            cb.move(20 + 30 * (i*20//460), 20 + i * 20 % 460)
            #print(cb.text())
            cb.toggle()
            checkboxes.append(cb)



        for i in checkboxes:
            i.stateChanged.connect(self.checkBoxChangedAction)

        button = QPushButton('Calculate track', self)
        button.setToolTip('This is an example button')
        button.move(200,70)
        button.clicked.connect(self.on_click)
        self.show()
        '''

    def on_click(self):
        #print('clicked')
        #print(self.names)
        self.program.SelectData(self.names)
        #self.program.ShowData()
        self.program.InitializePopulation(2,100)
        #self.program.ShowPopulation()
        self.program.GetPopulation().AddStart(START,END)
        self.program.GetPopulation().SortPopulation()
        self.program.ShowLengths()
        self.program.GetPopulation().RemoveStart()
        
        for i in range(0,1):
            self.program.PlayRound()

        self.program.ShowLengths()
        self.program.ShowBest()
        print(self.program.GetPopulation().BestIndividual().GetLength())
        self.create_map(self.program)

    def checkBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            #print("selected")
            #print(self.sender().text())
            if self.sender().text() not in self.names:
                self.names.append(self.sender().text())
        else:
            self.names.remove(self.sender().text())

    def create_map(self, program):

        #G = graph_from_place('Krakow, Poland', network_type='drive')
        #G = graph_from_place('Poland', network_type='none', infrastructure='way["highway"~"motorway"]')
        
        '''nodes = []  
        nodes.append(get_nearest_node(G, START["START"]))
        for place,position in self.program.GetData().Get().items():
            nodes.append(get_nearest_node(G, position))

        nodes.append(get_nearest_node(G, END["END"]))

        routes = []
        for i in range(0, len(nodes)-1):
            routes.append(shortest_path(G, nodes[i], nodes[i+1], weight='length'))
        '''


        m = folium.Map(location=[CRACOW_CENTRE["CRACOW"][0], CRACOW_CENTRE["CRACOW"][1]],
            zoom_start=15, control_scale=True)


        for place, position in self.program.GetPopulation().BestIndividual().Merge().items():
            if place == "END":
                folium.Marker(
                location=[position[0], position[1]],
                popup="START/" + place,
                icon=folium.Icon(color='red', icon='ok-sign'),
            ).add_to(m)
            else:
                folium.Marker(
                    location=[position[0], position[1]],
                    popup=place,
                    icon=folium.Icon(color='green', icon='ok-sign'),
                ).add_to(m)
        for i in range(0,self.program.GetPopulation().BestIndividual().GetSize()):
            points = []
            for place, position in self.program.GetPopulation().BestIndividual().Getn(i).Get().items():
                points.append(position)
            folium.PolyLine(
                points,
                color=choose_color()
                ).add_to(m)
        #print(type(routes[0]))
        #print(routes)
        '''for i in range(0,len(routes)):
            plot_route_folium(G, routes[i], route_width=3, route_map= m, route_color=choose_color(), tiles='Stamen Terrain', popup_attribute='name')
        '''
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



