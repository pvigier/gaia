import numpy as np
import matplotlib.pyplot as plt

neighbors = [(-1, -1), (-1, 0), (-1, 1), \
			 ( 0, -1),          ( 0, 1), \
			 ( 1, -1), ( 1, 0), ( 1, 1)]

class Cell:
	def __init__(self, energy, cost=0):
		self.energy = energy
		self.cost = cost
		self.updated = False

	def add_energy(self, energy):
		self.energy += energy

	def grow_old(self):
		self.energy -= self.cost

	def is_alive(self):
		return self.energy > 0

class Plant(Cell):
	new_born_energy = 15
	min_neighbors = 3
	max_neighbors = 8
	def __init__(self, energy=new_born_energy):
		Cell.__init__(self, energy)

class Herbivore(Cell):
	new_born_energy = 50
	def __init__(self, energy=new_born_energy):
		Cell.__init__(self, energy, 10)

class Carnivore(Cell):
	new_born_energy = 200
	def __init__(self, energy=new_born_energy):
		Cell.__init__(self, energy, 50)

class World:
	def __init__(self):
		# Size of the grid
		self.width = 100
		self.height = 100

		# Number of individuals at the beginning
		self.nb_plants = 5000
		self.nb_herbivores = 500
		self.nb_carnivores = 50

		# Init world
		self.cells = [[None for j in range(self.height)] for i in range(self.width)]
		self.init_species(self.nb_plants, Plant)
		self.init_species(self.nb_herbivores, Herbivore)
		self.init_species(self.nb_carnivores, Carnivore)

		print(self.get_populations())

	def init_species(self, nb, species):
		while nb > 0:
			i, j  = np.random.randint(0, self.width), np.random.randint(0, self.height-1)
			if self.cells[i][j] is None:
				self.cells[i][j] = species()
				nb -= 1

	def update_plants(self):
		new_plants = []
		for i in range(self.width):
			for j in range(self.height):
				if self.cells[i][j] is None:
					n = self.get_nb_empty_neighbors(i, j)
					if Plant.min_neighbors <= n <= Plant.max_neighbors:
						new_plants.append((i, j))
		for i, j in new_plants:
			self.cells[i][j] = Plant()

	def update_herbivores(self):
		for i in range(self.width):
			for j in range(self.height):
				if type(self.cells[i][j]) == Herbivore:
					herbivore = self.cells[i][j]
					if herbivore.updated:
						break
					herbivore.updated = True
					herbivore.grow_old()
					if not herbivore.is_alive():
						self.cells[i][j] = None
						break
					offset = np.random.randint(len(neighbors))
					found = None
					for k in range(offset, len(neighbors) + offset):
						di, dj = neighbors[k % len(neighbors)]
						ni, nj = i + di, j + dj
						if self.are_valid_coordinates(ni, nj) and type(self.cells[ni][nj]) == Plant:
							found = ni, nj
							break
					if not found is None:
						ni, nj = found
						herbivore.add_energy(self.cells[i][j].energy)
						self.cells[i][j] = None
						self.cells[ni][nj] = herbivore
						if herbivore.energy > Herbivore.new_born_energy:
							herbivore.energy //= 2
							self.cells[i][j] = Herbivore(herbivore.energy)
					else:
						offset = np.random.randint(len(neighbors))
						for k in range(offset, len(neighbors) + offset):
							di, dj = neighbors[k % len(neighbors)]
							ni, nj = i + di, j + dj
							if self.are_valid_coordinates(ni, nj) and self.cells[ni][nj] is None:
								self.cells[i][j] = None
								self.cells[ni][nj] = herbivore
								break

	def update_carnivores(self):
		for i in range(self.width):
			for j in range(self.height):
				if type(self.cells[i][j]) == Carnivore:
					carnivore = self.cells[i][j]
					if carnivore.updated:
						break
					carnivore.updated = True
					carnivore.grow_old()
					if not carnivore.is_alive():
						self.cells[i][j] = None
						break
					offset = np.random.randint(len(neighbors))
					found = None
					for k in range(offset, len(neighbors) + offset):
						di, dj = neighbors[k % len(neighbors)]
						ni, nj = i + di, j + dj
						if self.are_valid_coordinates(ni, nj) and type(self.cells[ni][nj]) == Herbivore:
							found = ni, nj
							break
					if not found is None:
						ni, nj = found
						carnivore.add_energy(self.cells[i][j].energy)
						self.cells[i][j] = None
						self.cells[ni][nj] = carnivore
						if carnivore.energy > Carnivore.new_born_energy:
							carnivore.energy //= 2
							self.cells[i][j] = Carnivore(carnivore.energy)
					else:
						np.random.randint(len(neighbors))
						for k in range(offset, len(neighbors) + offset):
							di, dj = neighbors[k % len(neighbors)]
							ni, nj = i + di, j + dj
							if self.are_valid_coordinates(ni, nj) and self.cells[ni][nj] is None:
								self.cells[i][j] = None
								self.cells[ni][nj] = carnivore
								break

	def reset_updated(self):
		for i in range(self.width):
			for j in range(self.height):
				if not self.cells[i][j] is None:
					self.cells[i][j].updated = False

	def step(self):
		self.reset_updated()
		self.update_plants()
		self.update_herbivores()
		self.update_carnivores()

	def get_populations(self):
		n_plants = 0
		n_herbivores = 0
		n_carnivores = 0
		for i in range(self.width):
			for j in range(self.height):
				if type(self.cells[i][j]) == Plant:
					n_plants += 1
				elif type(self.cells[i][j]) == Herbivore:
					n_herbivores += 1
				elif type(self.cells[i][j]) == Carnivore:
					n_carnivores += 1
		return n_plants, n_herbivores, n_carnivores

	# Util functions

	def get_nb_empty_neighbors(self, i, j):
		n = 0
		for di, dj in neighbors:
			ni, nj = i + di, j + dj
			if self.are_valid_coordinates(ni, nj):
				if self.cells[ni][nj] is None:
					n += 1
		return n

	def are_valid_coordinates(self, i, j):
		return 0 <= i < self.width and 0 <= j < self.height

world = World()
n_step = 10000
T = np.arange(n_step)
N_plants = np.zeros(n_step)
N_herbivores = np.zeros(n_step)
N_carnivores = np.zeros(n_step)
try:
	for t in T:
			N_plants[t], N_herbivores[t], N_carnivores[t] = world.get_populations()
			world.step()
			print('step {}:'.format(t), N_plants[t], N_herbivores[t], N_carnivores[t])
except KeyboardInterrupt:
	pass
plt.plot(T, N_plants, c='g')
plt.plot(T, N_herbivores, c='b')
plt.plot(T, N_carnivores, c='r')
plt.show()