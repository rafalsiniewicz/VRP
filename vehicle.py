from route import *
from random import *

class Vehicle:
	def __init__(self, _capacity = 10):
		self.capacity = _capacity
		self.route = Route()

	def Load(self, charge):
		self.capacity -= charge


	def AddRoute(self, _route):
		self.route = _route

	def ShowRoute(self):
		self.route.Show()

	def ShowCapacity(self):
		print(self.capacity)

	def GetRoute(self):
		return self.route

	def GetCapacity(self):
		return self.capacity

d = OrderedDict()
d["A"] = [randrange(0,10), randrange(0,10)]
r = Route()
r.AddPlace(list(d)[0], list(d.values())[0])
v = Vehicle()
v.AddRoute(r)
v.ShowRoute()
v.ShowCapacity()
v.Load(5)
v.ShowCapacity()
