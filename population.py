from individual import *
import itertools
from copy import *

class Population:
    def __init__(self):
        self.population = []

    def AddIndividual(self,individual):
        self.population.append(individual)

    def Show(self):
        for i in range(0,len(self.population)):
            for j in range(0,len(self.population[i].Get())):
                print(self.population[i].Get()[j].Get(),end="")
            print()

    def Get(self):
        return self.population

    def Getn(self,n):
        return self.population[n]

    def GetSize(self):
        return len(self.population)


    def Check_if_correct(self):
        pass

    def AddStart(self,start,end):
        for i in self.population:
            i.ResetLength()
            for j in i.Get():
                j.Get().update(start)
                j.Get().move_to_end("START", last=False)
                j.Get().update(end)
                i.AddLength(j)


    def RemoveStart(self):
        for i in self.population:
            for j in i.Get():
                if "START" in j.Get():
                    j.Get().popitem(last=False)
                    j.Get().popitem()
            i.ResetLength()

    def Crossing(self):     #crossing for individuals with the same amount of places in every route
        child = Individual()
        parent1 = randint(0,self.GetSize()-1)
        while True:
            parent2 = randint(0,self.GetSize()-1)
            if parent2 != parent1:
                break

        #for Individual that has at least 3 Routes 
        parent1_route = self.population[parent1].Get()[1]   #second Route from parent1 
        #print(self.population[parent1].GetSize())
        for i in range(0,self.population[parent1].GetSize()):
            route = Route()
            if i == 1:
                child.AddRoute(self.population[parent1].Get()[1])
            if i != 1:
                for j in range(0,self.population[parent2].GetSize()):
                    for place, position in self.population[parent2].Get()[j].Get().items():
                        if parent1_route.Check_place(place) == False and child.Check_place(place) == False and route.GetSize() < self.population[parent1].Get()[i].GetSize():
                            route.AddPlace(place,position)
                        #print(place,position,end="")
                child.AddRoute(route)
                #print()
        
        return child
        '''print(child.Check_if_correct())
        self.population[parent1].Show()
        print()
        self.population[parent2].Show()
        print()
        child.Show()'''
        #print(self.population[parent1].Get()[0].Get())

    def CrossingMerged(self, capacity):   #crossing for merged individuals 
        child = Individual()
        parent1 = randint(0,self.GetSize()-1)
        while True:
            parent2 = randint(0,self.GetSize()-1)
            if parent2 != parent1:
                break

        child_routes_length = []

        if self.population[parent1].GetSize() == 1:
            child_routes_length.append(len(self.population[parent1].Merge()))
        else:
            child_routes_length.append(randint(1,len(self.population[parent1].Merge())//self.population[parent1].GetSize()))
        #print(child_routes_length[0])
        def sum(child_routes_length):
            sum = 0
            for i in child_routes_length:
                sum += i 
            return sum
        
        for i in range(0,self.population[parent1].GetSize()-2): # bo jedna dlugosc dodalismy wyzej i jedna dodamy nizej
            if sum(child_routes_length) + self.population[parent1].Getn(i).GetSize() < len(self.population[parent1].Merge()):
                child_routes_length.append(self.population[parent1].Getn(i).GetSize())
            elif sum(child_routes_length) + self.population[parent2].Getn(i).GetSize() < len(self.population[parent1].Merge()):
                child_routes_length.append(self.population[parent2].Getn(i).GetSize())
            else:
                child_routes_length.append(1)

        if self.population[parent1].GetSize() == 1:
            route = Route(capacity)
            wanted_items = list(self.population[parent1].Merge().items())[:child_routes_length[0]//2]
            for place, position in wanted_items:
                route.AddPlace(place,position)
            for place, position in self.population[parent2].Merge().items():
                #print(place,position)
                if child.Check_place(place) == False and route.Check_place(place) == False:
                    route.AddPlace(place, position)
            child.AddRoute(route)

        else:
            child_routes_length.append(len(self.population[parent1].Merge())-sum(child_routes_length))

            for i in range(0,len(child_routes_length)):
                route = Route(capacity)
                if i == 0:
                    wanted_items = list(self.population[parent1].Merge().items())[:child_routes_length[i]]
                    for place, position in wanted_items:
                        route.AddPlace(place,position)
                if i > 0:
                    for j in range(0,child_routes_length[i]):
                        #print(child_routes_length[i])
                        for place, position in self.population[parent2].Merge().items():
                            #print(place,position)
                            if child.Check_place(place) == False and route.Check_place(place) == False:
                                route.AddPlace(place, position)
                                break
                child.AddRoute(route)

        #print(len(child.Merge()))
        #print(child_routes_length, len(child.Merge()))
        return child
        #child.Show()


    def Mutation(self, capacity): # Mutated individual merged is reversed (permutated in new version) parent with different routes lengths
        parent = randint(0,self.GetSize()-1)
        mutated = Individual()
        #print("parent ", parent)

        def sum(new_routes_length):
            sum = 0
            for i in new_routes_length:
                sum += i 
            return sum

        new_routes_length = []

        if self.population[parent].GetSize() == 1:
            new_routes_length.append(len(self.population[parent].Merge()))
        else:
            new_routes_length.append(randint(1,len(self.population[parent].Merge())//self.population[parent].GetSize()))
            for i in range(0,self.population[parent].GetSize()-2):
                try:
                    route_length = randint(1,(len(self.population[parent].Merge()) - sum(new_routes_length))//self.population[parent].GetSize())
                except:
                    route_length = 1
                new_routes_length.append(route_length)

            if len(self.population[parent].Merge())-sum(new_routes_length) > 0:
                new_routes_length.append(len(self.population[parent].Merge())-sum(new_routes_length))

        #print(self.population[parent].Merge())
        items = list(self.population[parent].Merge().items())
        shuffle(items)
        #print(self.population[parent])
        new_dict = OrderedDict(items)


        for i in range(0,len(new_routes_length)):
            route = Route(capacity)
            for j in range(0,new_routes_length[i]):
                #print(child_routes_length[i])
                for place, position in new_dict.items():
                    #print(place,position)
                    if mutated.Check_place(place) == False and route.Check_place(place) == False:
                        route.AddPlace(place, position)
                        break
            mutated.AddRoute(route)

        #print(mutated.Show())


        self.population[parent].Merge().clear()
        #self.population[parent] = OrderedDict(items)
        self.population[parent] = mutated


    def SortPopulation(self):
        #the less capacity and distance is the better //capacity should be low, because it means vehicle took much load
        #sorted in ascending order- the best individual has the lowest goal function value // Measure is the goal function 
        def Measure(individual):
            if individual.GetCapacity() > 0:
                size = str( int (int(individual.GetLength().km) / individual.GetCapacity()) )
                #print("size ", size)
                #print("len", len(size))
                #print("size", pow(10, len(size) - 1))
                return int(individual.GetLength().km) + pow(10, len(size) - 1)*individual.GetCapacity()
            else:
                return int(individual.GetLength().km) + individual.GetCapacity()
        self.population.sort(key=Measure)

    def SortbyDistance(self):
        def Measure(individual):
            return individual.GetLength()
        self.population.sort(key=Measure)

    def SortbyCapacity(self):
        def Measure(individual):
            return individual.GetCapacity()
        self.population.sort(key=Measure)
        

    def BestIndividual(self):
        '''min_length = self.population[0].GetLength()
        best = self.population[0]
        for i in range(1,len(self.population)):
            if self.population[i].GetLength() < min_length:
                min_length = self.population[i].GetLength()
                best = self.population[i]
        return best'''
        return self.population[0]


    def LeavenBest(self,n):
        for i in range(n,self.GetSize()):
            self.population.pop()




