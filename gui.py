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
import matplotlib.pyplot as plt




CRACOW_CENTRE = {"CRACOW": [50.061681, 19.938104]}

def choose_color():
    return "#{:06x}".format(randint(0, 0xFFFFFF))

class App(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.program = Program()
        self.program.ImportData("test1.json")
        # 1. option:
        '''self.names = ["A", "B", "C", "D"]
        for place,position in self.program.GetData().Get().items():
            self.names.append(place)
        self.program.SelectData(self.names)'''
        # 2. option:
        self.names = []
        for place,position in self.program.GetData().Get().items():
            #print(place)
            self.names.append(place)
        self.program.SelectData(self.names)

        # 3. option:
        '''self.names = []
        i = 0
        for place,position in self.program.GetData().Get().items():
            if i < 30:
                self.names.append(place)
            i += 1
        self.program.SelectData(self.names)'''
        
        #self.program.InitializePopulation(3,100)
        #self.interface()
        self.initUI()


    def createLayout_group(self, number):
        sgroupbox = QGroupBox("Places".format(number), self)
        layout_groupbox = QVBoxLayout(sgroupbox)
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

    '''def radio_buttons(self):
        
        self.frame = QFrame(self)
        self.frame.move(250, 90)
        self.frame.resize(125,55)
        
        self.distance = QRadioButton("Distance", self.frame)
        self.distance.setChecked(True)
        self.distance.move(0, 0)
        
        self.capacity = QRadioButton("Capacity", self.frame)
        self.capacity.move(0, 20)

        self.distance_capacity = QRadioButton("Distance and Capacity", self.frame)
        self.distance_capacity.move(0, 40)'''


    def plot_2d(self, name, x_pos, y_pos):
        button = QPushButton(name, self)
        #button.setToolTip('This is an example button')
        button.move(x_pos, y_pos)
        button.clicked.connect(self.on_click_plot)
        

    def text_boxes(self):
        #number of vehicles#

        self.ag = QLabel(self)
        self.ag.setText("GENETIC ALGORITHM PARAMETERS")
        self.ag.move(330, 90)
        self.ag.resize(200, 10)

        self.par = QLabel(self)
        self.par.setText("GENERAL PARAMETERS")
        self.par.move(360, 5)
        self.par.resize(200, 10)


        self.l1 = QLabel(self)
        self.l1.setText("number of vehicles")
        self.l1.move(250, 15)
        self.number_of_vehicles = QLineEdit(self)
        self.number_of_vehicles.setText("5")
        self.number_of_vehicles.move(250, 40)

        #vehicles capacity#
        self.l2 = QLabel(self)
        self.l2.setText("vehicles capacity")
        self.l2.move(360, 15)
        self.vehicles_capacity = QLineEdit(self)
        self.vehicles_capacity.setText("100")
        self.vehicles_capacity.move(360, 40)

        self.l9 = QLabel(self)
        self.l9.setText("base name")
        self.l9.move(470, 15)
        self.base_name = QLineEdit(self)
        self.base_name.setText("Base")
        self.base_name.move(470, 40)

        self.l10 = QLabel(self)
        self.l10.setText("base coord1, coord2")
        self.l10.move(580, 15)
        self.base_coord = QLineEdit(self)
        self.base_coord.setText("82, 76")
        self.base_coord.move(580, 40)


        self.l3 = QLabel(self)
        self.l3.setText("number of iterations")
        self.l3.move(250, 175)
        self.number_of_iterations = QLineEdit(self)
        self.number_of_iterations.setText("300")
        self.number_of_iterations.move(250, 200)


        '''self.l4 = QLabel(self)
        self.l4.setText("crossing probability")
        self.l4.move(250, 115)
        self.crossing_probability = QLineEdit(self)
        self.crossing_probability.setText("100")
        self.crossing_probability.move(250, 140)'''

        self.l5 = QLabel(self)
        self.l5.setText("mutation probability")
        self.l5.move(360, 115)
        self.mutation_probability = QLineEdit(self)
        self.mutation_probability.setText("50")
        self.mutation_probability.move(360, 140)

        self.l6 = QLabel(self)
        self.l6.setText("number of individuals in generation")
        self.l6.resize(400, 30)
        self.l6.move(470, 115)
        self.individuals_in_generation = QLineEdit(self)
        self.individuals_in_generation.setText("100")
        self.individuals_in_generation.move(470, 140)

        self.l7 = QLabel(self)
        self.l7.setText("number of individuals to stay")
        self.l7.resize(400, 30)
        self.l7.move(360, 175)
        self.individuals_to_stay = QLineEdit(self)
        self.individuals_to_stay.setText("80")
        self.individuals_to_stay.move(360, 200)


        self.l8 = QLabel(self)
        self.l8.setText("Result")
        #self.l8.resize(400, 30)
        self.l8.move(500, 370)
        self.result = QLineEdit(self)
        #self.result.setText("0")
        self.result.move(500, 400)


    def initUI(self):
        self.resize(700, 480)
        self.button('Calculate track', 370, 400)
        self.plot_2d('Draw', 250, 400)
        self.createLayout_Container()
        self.layout_All = QVBoxLayout(self)
        self.layout_All.addWidget(self.scrollarea)
        self.text_boxes()
        #self.radio_buttons()
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
        
        vehicle_capacity = int(self.vehicles_capacity.text())

        individuals_in_generation = int(self.individuals_in_generation.text())

        individuals_to_stay = int(self.individuals_to_stay.text())

        #crossing_probability = int(self.crossing_probability.text())

        mutation_probability = int(self.mutation_probability.text())

        base_name = self.base_name.text()
        base_name_end = self.base_name.text() + "_end"

        base_coord0 = self.base_coord.text().split(',')[0]
        base_coord1 = self.base_coord.text().split(',')[1]

        self.START = {base_name:[float(base_coord0), float(base_coord1)]}
        self.END = {base_name_end:[float(base_coord0), float(base_coord1)]}

        self.program.InitializePopulation(number_of_vehicles=number_of_vehicles, individuals_in_generation=individuals_in_generation, number_of_individuals_to_stay=individuals_to_stay, vehicle_capacity=vehicle_capacity)
        self.program.GetPopulation().AddStart(self.START,self.END)
        '''if self.distance.isChecked():
            self.program.GetPopulation().SortbyDistance()
        elif self.capacity.isChecked():
            self.program.GetPopulation().SortbyCapacity()
        elif self.distance_capacity.isChecked():
            self.program.GetPopulation().SortPopulation()'''
        self.program.GetPopulation().SortbyDistance()

        self.program.ShowLengthsandCapacity()

        self.program.GetPopulation().RemoveStart(self.START)
        
        
        self.best = self.program.PlayRound(number_of_vehicles=number_of_vehicles, individuals_in_generation=individuals_in_generation, 
            START=self.START, END=self.END, sort_type="distance", capacity=vehicle_capacity, 
            number_of_cycles = int(self.number_of_iterations.text()), number_of_individuals_to_stay=individuals_to_stay, 
            crossing_probability=100, mutation_probability=mutation_probability)
               

        self.program.ShowLengthsandCapacity()
        if self.program.GetPopulation().GetSize() > 0:
            self.best.Show()
            print("length: ", self.best.GetLength(), "capacity: ", self.best.GetCapacity())
            #self.create_map(self.program)
        else:
            print("population size = 0")
            print("zwieksz capacity")
       
        self.result.setText(str(self.best.GetLength()))
        f = open("output.txt", "w")
        f.write("best solution: \n")
        f.write("".join((str(item.Get()) + "\n") for item in self.best.Get()))
        f.write("\ngoal function value: ") 
        f.write(str(self.best.GetLength()))
        f.close()
        #self.program.ShowPopulation()

        '''color = ["r", "g", "b", "k", "y"]

        for r in range(0, best.GetSize()):
            points = best.Getn(r).GetValues()
            for i in range(0, len(points)-1):
                plt.plot([points[i][0], points[i+1][0]], [points[i][1], points[i+1][1]], color[r] + "o-")

        plt.grid()
        plt.show()'''

    def on_click_plot(self):

        color = ["r", "g", "b", "k", "y"]

        for r in range(0, self.best.GetSize()):
            points = self.best.Getn(r).GetValues()
            for i in range(0, len(points)-1):
                plt.plot([points[i][0], points[i+1][0]], [points[i][1], points[i+1][1]], color[r] + "o-")

        plt.grid()
        plt.show()

        

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
            if place == list(self.END.keys())[0]:
                folium.Marker(
                location=[position[0], position[1]],
                popup= list(self.START.keys())[0] + "/" + place,
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



