from scipy.spatial import Voronoi
import numpy as np
import matplotlib.pyplot as plt

class Diagram:
	def __init__(self, points=None, vertices=None, ridge_points=None, ridge_vertices=None, regions=None, is_border=None):
		self.points = points or []
		self.vertices = vertices or []
		self.ridge_points = ridge_points or []
		self.ridge_vertices = ridge_vertices or []
		self.regions = regions or []
		self.is_border = [False] * len(self.points)
		#self.point_region = point_region if not point_region is None else []

	def lloyd_algorithm(self):
		return np.array([get_centroid([self.vertices[i_vertice] for i_vertice in region]) for region in self.regions])

	def plot(self):
		plt.gca().set_aspect('equal', adjustable='box')
		for (v1, v2) in self.ridge_vertices:
			x1, x2, y1, y2 = self.vertices[v1][0], self.vertices[v2][0], self.vertices[v1][1], self.vertices[v2][1]
			plt.plot([x1, x2], [y1, y2], c='k')
		for i, (x, y) in enumerate(self.points):
			if self.is_border[i]:
				plt.scatter(x, y, c='r')
			else:
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

def get_all_symetrics(points):
	""" Add symetrical points. """
	origins = np.array([[0, 0], [0, 0], [0, 1], [1, 0]])
	directions = np.array([[1, 0], [0, 1], [1, 0], [0, 1]])
	more_points = points
	for origin, direction in zip(origins, directions):
		more_points = np.concatenate((more_points, get_symetric_points(points, origin, direction)), axis=0)
	return more_points

def bounded_voronoi(points):
	more_points = get_all_symetrics(points)
	# Compute Voronoi diagram
	vor = Voronoi(more_points)
	# Filter vertices, ridges and regions
	diagram = Diagram(list(points))
	new_indices = {}
	for (i_point1, i_point2), i_vertices in zip(vor.ridge_points, vor.ridge_vertices):
		point1_valid = (i_point1 >= 0 and i_point1 < len(points))
		point2_valid = (i_point2 >= 0 and i_point2 < len(points))
		if point1_valid or point2_valid:
			for i_vertex in i_vertices:
				if not i_vertex in new_indices:
					new_indices[i_vertex] = len(diagram.vertices)
					diagram.vertices.append(vor.vertices[i_vertex])
			diagram.ridge_vertices.append([new_indices[i_vertex] for i_vertex in i_vertices])
			# Check if one point is a border point
			if point1_valid and not point2_valid:
				diagram.is_border[i_point1] = True
				i_point2 = -1
			elif point2_valid and not point1_valid:
				diagram.is_border[i_point2] = True
				i_point1 = -1
			diagram.ridge_points.append([i_point1, i_point2])
	for i_point, i_region in enumerate(vor.point_region[:len(points)]):
		region = vor.regions[i_region]
		diagram.regions.append([new_indices[i_vertex] for i_vertex in region])
	return diagram

def get_relaxed_voronoi(nb_points=128, nb_iter=2):
	points = np.random.rand(nb_points, 2)
	diagram = bounded_voronoi(points)
	for _ in range(nb_iter):
		points = diagram.lloyd_algorithm()
		diagram = bounded_voronoi(points)
	return diagram

def plot_diagram(nb_points=128, nb_iter=2):	
	points = np.random.rand(nb_points, 2)
	diagram = bounded_voronoi(points)
	plt.subplot('121')
	diagram.plot()
	for _ in range(nb_iter):
		points = diagram.lloyd_algorithm()
		diagram = bounded_voronoi(points)
	plt.subplot('122')
	diagram.plot()
	plt.show()

if __name__ == '__main__':
	plot_diagram()