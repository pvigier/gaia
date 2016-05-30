class Region:
	def __init__(self):
		self.point = None # ID
		self.vertices = [] # IDs
		self.adjacent_regions = {} # ID -> (vertex)
		self.biome = 'LAND'
		self.border = False

class Map:
	def __init__(self):
		self.points = []
		self.vertices = []
		self.regions = []

	def from_diagram(self):
		pass

