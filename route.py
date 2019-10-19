from collections import *
from math import *
from collections import *
from geopy.distance import *
from osmnx import *
from networkx import *

def Distance(x1,y1,x2,y2):
	x1=float(x1)
	x2=float(x2)
	y1=float(y1)
	y2=float(y2)
	return sqrt(pow(x1-x2,2)+pow(y1-y2,2))

def Geodesic_distance(place1,place2):
	return geodesic(place1,place2)

def Great_circle_distance(place1,place2):
	return great_circle(place1,place2)

def Haversine(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = radius * c

    return d

def Street_distance(G, place1, place2):
    return shortest_path_length(G, place1, place2, weight='length')

START = {"START":[50.057767, 19.931321]}
END = {"END":[50.057767, 19.931321]}

#G = graph_from_place('Krakow, Poland', network_type='drive')
	
class Route:
	def __init__(self):
		self.route=OrderedDict()
	def AddPlace(self,name,values):
		if name != None:
			self.route[name]=values
	def Get(self):
		return self.route
	def GetSize(self):
		return len(self.route)
	def Show(self):
		print(self.route)
	def GetLength(self):
		length = Geodesic_distance([0, 0],[0, 0])
		#length = Street_distance(G, [0, 0],[0, 0])
		#print(length)
		#print(self.route[0])
		#print(list(self.route.values())[0][0])
		for i in range(0,len(self.route)-1):
			#length += Distance(list(self.route.values())[i][0],list(self.route.values())[i][1],list(self.route.values())[i+1][0],list(self.route.values())[i+1][1])
			length += Geodesic_distance(list(self.route.values())[i], list(self.route.values())[i+1])
			#length += Street_distance(G, get_nearest_node(G, list(self.route.values())[i]), get_nearest_node(G, list(self.route.values())[i+1]))
			#print(i)
		return length

	def FindNearest(self,place,value,data):
		distances = OrderedDict()
		del data[place]
		for j in data:
			distances[j] = (Distance(value[0],value[1],data[j][0],data[j][1]))
		return min(distances,key=distances.get)

	def Check_if_correct(self,n):
		if n == self.GetSize():
			return True
		else:
			#print("false")
			return False

	def Check_place(self,name):
		for i in self.route:
			if i == name:
				return True
		return False
