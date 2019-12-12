import numpy
from numpy import *
from json import *
from population import * 
#def Distance(name1,name2):
#	return sqrt(pow(name1[0]-name2[0],2)+pow(name1[1]-name2[1],2))

class Data:
	def __init__(self):
		self.data=OrderedDict()
	def Import(self,filename):
		file = open(filename)
		filedata = file.read()
		self.data = loads(filedata,object_pairs_hook=OrderedDict)

	def Show(self):
		print(self.data)
	def Get(self):
		return self.data
	def GetValue(self,i):
		if i < len(self.data) and i >= 0:
			return list(self.data.values())[i]
		else:
		 	pass
	def GetName(self,i):
		if i < len(self.data) and i >= 0:
			return list(self.data)[i]
		else:
			pass
	'''def Distances(self):
		matrix=[]
		for i in self.data:
			distances = []
			for j in self.data:
				distances.append(Distance(self.data[i][0],self.data[i][1],self.data[j][0],self.data[j][1]))
			matrix.append(distances)
		return matrix
	'''


	

'''data = genfromtxt("data.txt",dtype='str')
print(data)
place=[]
data_x=[]
data_y=[]


for i in range(1,len(data)):
	place.append(data[i][0])
	data_x.append(data[i][1])
	data_y.append(data[i][2])

data = dict(zip(place,zip(data_x,data_y)))
print(data["A"])'''

'''data = Data()
data.Import("data.json")
data.Show()
print("\n\n")

print(Geodesic_distance(data.GetValue(0),data.GetValue(1)))
print(Great_circle_distance(data.GetValue(0),data.GetValue(1)))
print(Distance(data.GetValue(0)[0],data.GetValue(0)[1],data.GetValue(1)[0],data.GetValue(1)[1]))

print(Haversine(data.GetValue(0),data.GetValue(1)))

#print(ind.CreateIndividual(data,3))
#print(ind.GetLength())
print()
pop = Population()

for i in range(0,100):
	ind=Individual()
	ind.CreateIndividual(data,3)
	pop.AddIndividual(ind)

#pop.Show()
#pop.AddStart(START,END)
#pop.Show()

#pop.Getn(0).Show()
#print(pop.Getn(0).Merge())

pop.AddStart(START,END)
pop.SortPopulation()
for i in range(0,100):
	print(pop.Getn(i).GetLength())
print()
#pop.RemoveStart()
for j in range(0,50):
	pop.RemoveStart()
	for i in range(0,40):
		pop.AddIndividual(pop.CrossingMerged())

	pop.AddStart(START,END)
	pop.SortPopulation()
	pop.LeavenBest(100)
#pop.SortPopulation()

#pop.AddStart(START,END)
pop.SortPopulation()
for i in range(0,100):
	print(pop.Getn(i).GetLength())

pop.BestIndividual().Show()
#print(pop.BestIndividual().GetLength())'''


