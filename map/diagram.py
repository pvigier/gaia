from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2, snoise2

class Diagram:
	def __init__(self, points=None, vertices=None, ridge_points=None, ridge_vertices=None, regions=None, point_region=None):
		self.points = points if not points is None else npself.array([])
		self.vertices = vertices if not vertices is None else []
		self.ridge_points = ridge_points if not ridge_points is None else []
		self.ridge_vertices = ridge_vertices if not ridge_vertices is None else []
		self.regions = regions if not regions is None else []
		self.border_regions = []
		#self.point_region = point_region if not point_region is None else []

	def lloyd_algorithm(self):
		return np.array([get_centroid([self.vertices[i_vertice] for i_vertice in region]) for region in self.regions])

	def plot(self):
		plt.figure()
		#plt.xlim(x_min - 0.5, x_max + 0.5)
		#plt.ylim(y_min - 0.5, y_max + 0.5)
		plt.gca().set_aspect('equal', adjustable='box')
		for (v1, v2) in self.ridge_vertices:
			x1, x2, y1, y2 = self.vertices[v1][0], self.vertices[v2][0], self.vertices[v1][1], self.vertices[v2][1]
			plt.plot([x1, x2], [y1, y2], c='k')
		for i, (x, y) in enumerate(self.points):
			plt.scatter(x, y)
			#plt.annotate(str(i), xy=(x, y), xytext=(5, 2), textcoords='offset points', ha='right', va='bottom')
		for i, (x, y) in enumerate(self.vertices):
			plt.scatter(x, y, c='g')
			#plt.annotate(str(i), xy=(x, y), xytext=(5, 2), textcoords='offset points', ha='right', va='bottom')

def get_orthogonal(vector):
	return np.array([vector[1], -vector[0]])

def get_centroid(points):
	return sum(points) / len(points)

def get_symetric_points(points, origin, direction):
	direction_orth = get_orthogonal(direction)
	symetric_points = np.zeros(points.shape)
	for i, point in enumerate(points):
		shifted_point = point - origin
		symetric_points[i,:] = origin + np.dot(shifted_point, direction) * direction - np.dot(shifted_point, direction_orth) * direction_orth
	return symetric_points

def bounded_voronoi(points):
	# Add symetrical points
	origins = np.array([[0, 0], [0, 0], [0, 1], [1, 0]])
	directions = np.array([[1, 0], [0, 1], [1, 0], [0, 1]])
	more_points = points
	for origin, direction in zip(origins, directions):
		more_points = np.concatenate((more_points, get_symetric_points(points, origin, direction)), axis=0)
	# Compute Voronoi diagram
	vor = Voronoi(more_points)
	# Filter vertices, ridges and regions
	diagram = Diagram(points)
	c = 0
	new_indices = {}
	for (i_point1, i_point2), i_vertices in zip(vor.ridge_points, vor.ridge_vertices):
		if (i_point1 >= 0 and i_point1 < len(points)) or (i_point2 >= 0 and i_point2 < len(points)):
			diagram.ridge_points.append([i_point1, i_point2])
			for i_vertex in i_vertices:
				if not i_vertex in new_indices:
					new_indices[i_vertex] = c
					c += 1
					diagram.vertices.append(vor.vertices[i_vertex])
			diagram.ridge_vertices.append([new_indices[i_vertex] for i_vertex in i_vertices])
	for i_point, i_region in enumerate(vor.point_region[:len(points)]):
		region = vor.regions[i_region]
		diagram.regions.append([new_indices[i_vertex] for i_vertex in region])
	return diagram

def generate_diagram():	
	points = np.random.rand(128, 2)
	diagram = bounded_voronoi(points)
	diagram.plot()
	n_iter = 2
	for _ in range(n_iter):
		points = diagram.lloyd_algorithm()
		diagram = bounded_voronoi(points)
	diagram.plot()
	plt.show()

generate_diagram()

size = 256
octaves = 1
freq = 64.0 * octaves
noise = np.zeros((size, size), dtype=np.int8)
for i in range(size):
	for j in range(size):
		noise[i, j] = pnoise2(j / freq, i / freq, octaves) * 127.0
#noise = noise  * (noise > 0)
plt.imshow(noise, cmap='gray')
plt.show()