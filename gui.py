#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QCheckBox, QRadioButton, QButtonGroup, QVBoxLayout, QPushButton, QScrollArea, QGroupBox, QLineEdit, QLabel
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
from PySide2.QtWidgets import QApplication
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
        self.program.ImportData("swiat.json")
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

    def button(self, name, x_pos, y_pos):
        button = QPushButton(name, self)
        #button.setToolTip('This is an example button')
        button.move(x_pos, y_pos)
        button.clicked.connect(self.on_click)

    def radio_buttons(self):
        
        self.frame = QFrame(self)
        self.frame.move(250, 90)
        self.frame.resize(125,55)
        
        self.distance = QRadioButton("Distance", self.frame)
        self.distance.setChecked(True)
        self.distance.move(0, 0)
        
        self.capacity = QRadioButton("Capacity", self.frame)
        self.capacity.move(0, 20)

        self.distance_capacity = QRadioButton("Distance and Capacity", self.frame)
        self.distance_capacity.move(0, 40)
        

    def text_boxes(self):
        #number of vehicles#
        self.l1 = QLabel(self)
        self.l1.setText("number of vehicles")
        self.l1.move(250, 5)
        self.number_of_vehicles = QLineEdit(self)
        self.number_of_vehicles.setPlaceholderText("Please enter number of vehicles")
        self.number_of_vehicles.move(250, 30)

        #vehicles capacity#
        self.l2 = QLabel(self)
        self.l2.setText("vehicles capacity")
        self.l2.move(400, 5)
        self.vehicles_capacity = QLineEdit(self)
        self.vehicles_capacity.setPlaceholderText("Please enter capacity")
        self.vehicles_capacity.move(400, 30)


    def initUI(self):
        self.resize(640, 480)
        self.button('Calculate track', 370, 400)
        self.createLayout_Container()
        self.layout_All = QVBoxLayout(self)
        self.layout_All.addWidget(self.scrollarea)
        self.text_boxes()
        self.radio_buttons()
        #self.num = self.text_box("Please enter number of vehicles", 350, 310)
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
        #print(self.number_of_vehicles.text())
        self.program.SelectData(self.names)
        number_of_vehicles = int(self.number_of_vehicles.text())
        
        #self.program.ShowData()
        if self.distance.isChecked():
            vehicle_capacity = self.program.GetTotalDataCapacity() + 1
        else:
            vehicle_capacity = int(self.vehicles_capacity.text())
        self.program.InitializePopulation(number_of_vehicles, 100, vehicle_capacity)
        self.program.GetPopulation().AddStart(START,END)
        if self.distance.isChecked():
            self.program.GetPopulation().SortbyDistance()
        elif self.capacity.isChecked():
            self.program.GetPopulation().SortbyCapacity()
        elif self.distance_capacity.isChecked():
            self.program.GetPopulation().SortPopulation()

        self.program.ShowLengthsandCapacity()
        self.program.GetPopulation().RemoveStart()
        
        for i in range(0,1):
            if self.distance.isChecked():
                #print("distance")
                self.program.PlayRound("distance", vehicle_capacity)
            elif self.capacity.isChecked():
                #print("capacity")
                self.program.PlayRound("capacity", vehicle_capacity)
            elif self.distance_capacity.isChecked():
                #print("distance_capacity")
                self.program.PlayRound("distance_capacity", vehicle_capacity)    

        self.program.ShowLengthsandCapacity()
        self.program.ShowBest()
        print("length: ", self.program.GetPopulation().BestIndividual().GetLength(), "capacity: ", self.program.GetPopulation().BestIndividual().GetCapacity())
        self.create_map(self.program)
   
        #self.program.ShowPopulation()
        

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
                points.append(position[0:2])
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



