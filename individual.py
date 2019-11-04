from collections import *
from route import *
from random import *

class Individual:
	def __init__(self):
		#self.individual=OrderedDict()
		self.individual=[]
		#self.length = 0
		self.length = Geodesic_distance([0, 0],[0, 0])
	def AddRoute(self,route):
		#self.individual.update(route.Get())
		self.individual.append(route)
		self.length+=route.GetLength()
		#self.AddPlaceength(route)
	def Get(self):
		return self.individual
	def Getn(self,n):
		return self.individual[n]
	def GetLength(self):
		return self.length
	def GetSize(self):
		return len(self.individual)
	def GetCapacity(self):
		capacity = 0
		for i in self.individual:
			capacity += i.GetCapacity()
		return capacity
	def Show(self):
		for i in range(0,len(self.individual)):
			print(self.individual[i].Get(),end="")
		print()
	def AddLength(self, route):
		self.length += route.GetLength()
	def ResetLength(self):
		#self.length = 0
		self.length = Geodesic_distance([0, 0],[0, 0])


	def CreateIndividual(self, data, n, vehicle_capacity):
		#Routes =[]
		#self.individual=[]
		#self.length=0
		'''
		function creates individual and returns true if number of places for individual is equal len(data.Get()) otherwise returns false
		'''
		numbers=[]
		for i in range(0,len(data.Get())):
			numbers.append(i)

		def sum(routes_length):
			sum = 0
			for i in routes_length:
				sum += i 
			return sum

		routes_length = []

		if n == 1:
			routes_length.append(len(data.Get()))
		else:
			rand = randint(1,len(data.Get())//n)
			routes_length.append(rand)
			for i in range(0,n-2):
				try: 
					route_length = randint(1,(len(data.Get()) - sum(routes_length) - 1)//(n-1-i))
				except:
					print("error during getting random route length- route gets length of 1")
					route_length = 1
				routes_length.append(route_length)

			routes_length.append(len(data.Get())-sum(routes_length))

		#print(numbers)
		routes_length.sort(reverse=True)
		#print(routes_length)
		for i in range(0,n):
			route = Route(vehicle_capacity)
			for j in range(0,routes_length[i]):
				random = choice(numbers)
				route.AddPlace(data.GetName(random),data.GetValue(random))
				numbers.remove(random)
				
				
			self.AddRoute(route)
		'''for i in range(0,n):
			route = Route()
			#route.AddPlace("START",START.get("START"))
			if(len(numbers))>=(2*len(data.Get())//n):
				for j in range(0,len(data.Get())//n):
					if(len(numbers) != 0):
						random=sample(numbers,k=1)
						route.AddPlace(data.GetName(random[0]),data.GetValue(random[0]))
						numbers.remove(random[0])
				#route.AddPlace("START",START.get("START"))
			else:
				for j in range(0,ceil(len(data.Get())/n)):
					if(len(numbers) != 0):
						random=sample(numbers,k=1)
						route.AddPlace(data.GetName(random[0]),data.GetValue(random[0]))
						numbers.remove(random[0])
				#route.AddPlace("START",START.get("START"))
			#Routes.append(route.Get())
			route.Show()
			self.AddRoute(route)
		'''
		#print(len(self.Merge()))

		#print(route.Get())
		#return Routes

	def Merge(self):
		merged = OrderedDict()
		for i in self.individual:
			merged.update(i.Get())

		return merged

	def Check_if_correct(self):
		for i in self.individual:
			for j in self.individual:
				if i != j:
					for i_keys in i.Get():
						for j_keys in j.Get():
							if i_keys == j_keys:
								return False

		return True


	def Check_place(self,name):
		for i in self.individual:
			for j in i.Get():
				if j == name:
					return True
		return False