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
		self.ImportData("test1.json")
		new_dict = self.data.Get().copy()
		for place, position in new_dict.items():
			stay = False
			for i in list_of_places:
				if i == place:
					stay = True
			if stay == False:
				del self.data.Get()[place]


	def InitializePopulation(self, number_of_vehicles = 3, individuals_in_generation = 300, number_of_individuals_to_stay = 100, vehicle_capacity = 10):
		#self.ShowData()
		self.population.Get().clear()
		i = 0
		j = 0
		while i < individuals_in_generation and j < 1000*individuals_in_generation:
			ind=Individual()
			if ind.CreateIndividual(self.data, number_of_vehicles, vehicle_capacity, self.GetTotalDataCapacity()) == True:
				self.population.AddIndividual(ind)
				i += 1
			#ind.Show()
			#self.ShowPopulation()
			j += 1
			print(j)
		print("population size = ", self.population.GetSize())
		self.population.SortbyDistance()
		#self.ShowPopulation()
		self.population.LeavenBest(number_of_individuals_to_stay)

		self.size = self.population.GetSize()


	def PlayRound(self, number_of_vehicles, individuals_in_generation, START, END, sort_type, capacity, number_of_cycles = 50, 
		number_of_crossings = 100, number_of_individuals_to_stay = 100, crossing_probability = 100, mutation_probability = 100):
		'''
		najpierw sortujemy, ustalamy najlepszego i ilosc krzyzowan i mutacji
		w petli:
			wybieramy elite, usuwamy baze z rozwiazan, robimy number_of_crossings nowych rozwiazan ze wszystkich, tzn. nie tylko
			elita bierze udzial w krzyzowaniu tylko wszystkie osobniki, dolaczajmy je do poprzednich, czyli jak bylo np. 100 i 
			robimy 80 to mamy potem 180, powyzej 100 iteracji zwiekszamy prawdopodobienstwo mutacji,
			robimy mutacje na nowo powstalych, czyli dla poprzedniego przykladu dla 80 nowo powstalych
			powyzej 100 iteracji co 2 iteracje robimy kontrolowana mutacje dla elity
			sortujemy i wybieramy najlepszego

		'''


		self.population.AddStart(START,END)
		if sort_type == "distance_capacity":
			self.population.SortPopulation()
		if sort_type == "distance":
			self.population.SortbyDistance()
		if sort_type == "capacity":
			self.population.SortbyCapacity()

		number_of_crossings = individuals_in_generation - number_of_individuals_to_stay

		best = self.population.Get()[0]

		for j in range(0,number_of_cycles):	
			self.population.LeavenBest(number_of_individuals_to_stay)																							
			self.population.RemoveStart(START)
			elite = Population()
			if 100 * random() <= crossing_probability:
				for cross in range(0, 2*number_of_crossings):
					child = self.population.CrossingMerged(capacity=capacity, data=self.data, range_ind=number_of_individuals_to_stay)
					count = 0
					while child == False:	
						#print("crossing")
						child = self.population.CrossingMerged(capacity=capacity, data=self.data, range_ind=number_of_individuals_to_stay)
						count += 1
					elite.AddIndividual(child)
					
			elite.SortbyDistance()
			elite.LeavenBest(number_of_crossings)
			for child in elite.Get():
				self.population.AddIndividual(child)

			if j == 50:
				mutation_probability *= 1.5
				'''new = 0
				while new < 10:
					ind=Individual()s
					if ind.CreateIndividual(self.data, number_of_vehicles, capacity, self.GetTotalDataCapacity()) == True:
						self.population.AddIndividual(ind)
						new += 1'''
	
			if 100 * random() <= mutation_probability:
				for mut in range(0, number_of_crossings):
				#for mut in range(number_of_individuals_to_stay, self.population.GetSize()):
					mutation = self.population.Mutation(capacity=capacity, data=self.data, range_ind=individuals_in_generation)
					count = 0
					while mutation == False:
						#print("controlled")
						mutation = self.population.Mutation(capacity=capacity, data=self.data, range_ind=individuals_in_generation)
						count += 1

			if j > 0 and j % 2 == 0:
				for mut in range(0, 2 * number_of_crossings):
				#for mut in range(number_of_individuals_to_stay, self.population.GetSize()):
					mutation = self.population.ControlledMutation(capacity=capacity, data=self.data, range_ind=individuals_in_generation)
					count = 0
					while mutation == False:
						#print("controlled")
						mutation = self.population.ControlledMutation(capacity=capacity, data=self.data, range_ind=individuals_in_generation)
						count += 1

			self.population.AddStart(START,END)
			
			if sort_type == "distance_capacity":
				self.population.SortPopulation()
			if sort_type == "distance":
				self.population.SortbyDistance()
			if sort_type == "capacity":
				self.population.SortbyCapacity()


			print(j, " ", self.population.BestIndividual().GetLength(), "	", self.population.BestIndividual().GetCapacity())
			#print(j, " ", best.GetLength(), "	", best.GetCapacity())
			if self.population.BestIndividual().GetLength() < best.GetLength():
				best = copy(self.population.BestIndividual())

			#self.population.LeavenBest(number_of_individuals_to_stay)
			
			#self.population.SortPopulation()
		return best



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
		for i in range(0,self.population.GetSize()):
			print("length: ", self.population.Getn(i).GetLength(), "capacity: ", self.population.Getn(i).GetCapacity())
		print()


	def ShowBest(self):
		self.population.BestIndividual().Show()
		print()




