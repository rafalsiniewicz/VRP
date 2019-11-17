from numpy import *
from population import * 
from data_import import *
from osmnx import *

class Program:
	def __init__(self):
		self.population = Population()
		self.data = Data()
		self.size = 300

	def GetPopulation(self):
		return self.population

	def GetData(self):
		return self.data

	def GetSize(self):
		return self.size

	def ImportData(self, name = "data.json"):
		self.data.Import(name)

	def ShowData(self):
		self.data.Show()
		print()

	def GetTotalDataCapacity(self):
		sum = 0
		for place, position in self.data.Get().items():
			sum += position[2]
		return sum

	def GetNames(self):
		names = []
		for place, position in self.data.Get().items():
			names.append(place)
		#print(names)
		return names

	def SelectData(self, list_of_places):
		self.ImportData("swiat.json")
		new_dict = self.data.Get().copy()
		for place, position in new_dict.items():
			stay = False
			for i in list_of_places:
				if i == place:
					stay = True
			if stay == False:
				del self.data.Get()[place]


	def InitializePopulation(self, number_of_vehicles = 3, number_of_individuals_to_stay = 100, vehicle_capacity = 10):
		#self.ShowData()
		self.population.Get().clear()
		for i in range(0,self.size):
			ind=Individual()
			ind.CreateIndividual(self.data, number_of_vehicles, vehicle_capacity)
			self.population.AddIndividual(ind)
			#ind.Show()
			#self.ShowPopulation()
		self.population.SortPopulation()
		#self.ShowPopulation()
		self.population.LeavenBest(number_of_individuals_to_stay)

		self.size = self.population.GetSize()


	def PlayRound(self, sort_type, capacity, number_of_cycles = 50, number_of_crossings = 50, number_of_individuals_to_stay = 100):
		self.population.AddStart(START,END)
		if sort_type == "distance_capacity":
			self.population.SortPopulation()
		if sort_type == "distance":
			self.population.SortbyDistance()
		if sort_type == "capacity":
			self.population.SortbyCapacity()
		for j in range(0,number_of_cycles):
			self.population.RemoveStart()
			for i in range(0,number_of_crossings):
				child = self.population.CrossingMerged(capacity)
				self.population.AddIndividual(child)
				
			self.population.Mutation(capacity)
			self.population.AddStart(START,END)
			if sort_type == "distance_capacity":
				self.population.SortPopulation()
			if sort_type == "distance":
				self.population.SortbyDistance()
			if sort_type == "capacity":
				self.population.SortbyCapacity()
			self.population.LeavenBest(number_of_individuals_to_stay)

		#self.population.SortPopulation()


	def ShowPopulation(self):
		self.population.SortPopulation()
		self.population.Show()
		print()

	def ShowLengths(self):
		#self.population.SortPopulation()
		for i in range(0,self.size):
			print(self.population.Getn(i).GetLength())
		print()

	def ShowLengthsandCapacity(self):
		#self.population.SortPopulation()
		for i in range(0,self.size):
			print("length: ", self.population.Getn(i).GetLength(), "capacity: ", self.population.Getn(i).GetCapacity())
		print()


	def ShowBest(self):
		self.population.BestIndividual().Show()
		print()




