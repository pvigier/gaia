
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

size = 40
proba_predator_death = 0.03
proba_predator_reproduction = 0.4
proba_predator_kill = 1
proba_prey_reproduction = 0.1

# Util functions

def occurs(proba):
	return np.random.sample() <= proba

def move(i, j):
	moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
	candidates = [(di, dj) for di, dj in moves if 0 <= i + di < size and 0 <= j + dj < size]
	di, dj = candidates[np.random.randint(len(candidates))]
	return i + di, j + dj

# Core functions

class Gaia:
	def __init__(self):
		self.predators = []
		self.preys = []
		self.pos_preys = defaultdict(list)
		self.pos_predators = defaultdict(list)

		n_init_predator = 10
		for _ in range(n_init_predator):
			i, j = np.random.randint(size), np.random.randint(size)
			self.predators.append((i, j))
		n_init_prey = 100
		for _ in range(n_init_prey):
			i, j = np.random.randint(size), np.random.randint(size)
			self.preys.append((i, j))

	def update_pos_predators(self):
		self.pos_predators.clear()
		for i_predator, (i, j) in enumerate(self.predators):
			self.pos_predators[(i, j)].append(i_predator)

	def update_pos_preys(self):
		self.pos_preys.clear()
		for i_prey, (i, j) in enumerate(self.preys):
			self.pos_preys[(i, j)].append(i_prey)

	def update_predators(self):
		new_predators = []
		for i, j in self.predators:
			if not occurs(proba_predator_death):
				new_predators.append(move(i, j))
		self.predators = new_predators
		self.update_pos_predators()

	def update_preys(self):
		new_preys = []
		for i, j in self.preys:
			if occurs(proba_prey_reproduction) and not (i, j) in self.pos_predators:
				new_preys.append((i, j))
			new_preys.append((move(i, j)))
		self.preys = new_preys
		self.update_pos_preys()

	def hunt(self):
		killed_preys = set()
		new_born_predators = []
		for i, j in self.predators:
			if (i, j) in self.pos_preys:
				feed = False
				for i_prey in self.pos_preys[(i, j)]:
					if occurs(proba_predator_kill):
						killed_preys.add(i_prey)
						feed = True
				if feed and occurs(proba_predator_reproduction):
					new_born_predators.append((i, j))
		self.predators += new_born_predators
		self.preys = [(i, j) for i_prey, (i, j) in enumerate(self.preys) if not i_prey in killed_preys]
		self.update_pos_predators()
		self.update_pos_preys()

	def plot(self):
		for i, j in self.predators:
			plt.scatter(i, j, c='r')
		for i, j in self.preys:
			plt.scatter(i, j, c='b')
		plt.show()

	def step(self):
		self.update_predators()
		self.update_preys()
		self.hunt()
		return len(self.predators), len(self.preys)

n_step = 1000
T = np.arange(n_step)
N_predators = np.zeros(n_step)
N_preys = np.zeros(n_step)
world = Gaia()
try:
	for t in T:
		N_predators[t], N_preys[t] = world.step()
		print(N_predators[t], N_preys[t])
except KeyboardInterrupt:
	pass
plt.plot(T, N_predators, c='r')
plt.plot(T, N_preys, c='b')
plt.show()
