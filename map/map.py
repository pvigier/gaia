import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from diagram import get_relaxed_voronoi
from coasts import generate_coast_mask, gaussian_kernel

class Region:
    def __init__(self, point, vertices=None, is_border=False):
        self.point = point # ID
        self.vertices = vertices or [] # IDs
        self.adjacent_regions = {} # {i_point: i_ridge}
        self.biome = 'LAKE'
        self.is_border = is_border
        self.altitude = 0

    def get_color(self):
        if self.biome == 'LAND':
            g = hex(int(105 + self.altitude * 150))[2:]
            r = hex(int(15 + self.altitude * 240))[2:]
            r = '0' + r if len(r) == 1 else r
            return '#' + r + g + r
        elif self.biome == 'SEA':
            return '#002f7c'
        elif self.biome == 'LAKE':
            return '#50a0b0'

class Map:
    def __init__(self):
        self.points = [] # Coordinates
        self.vertices = [] # Coordinates
        self.altitudes = []
        self.ridges = [] # [(i_vertice1, i_vertice2)]
        self.regions = []

    def from_diagram(self, diagram):
        self.points = diagram.points
        self.vertices = diagram.vertices
        self.ridges = diagram.ridge_vertices
        for i_point, (i_vertices, is_border) in enumerate(zip(diagram.regions, diagram.is_border)):
            self.regions.append(Region(i_point, i_vertices, is_border))
        for i_ridge, (i_point1, i_point2) in enumerate(diagram.ridge_points):
            if i_point1 >= 0:
                self.regions[i_point1].adjacent_regions[i_point2] = i_ridge
            if i_point2 >= 0:
                self.regions[i_point2].adjacent_regions[i_point1] = i_ridge

    def set_coasts(self, mask):
        size = mask.shape[0]
        for region in self.regions:
            #if region.is_border:
            #    self.regions[-1].biome = 'SEA'
            x, y = self.points[region.point] * size
            if mask[int(y), int(x)]:
                region.biome = 'LAND'
        self.set_lake()
        self.set_altitude()


    def set_lake(self):
        to_see = []
        for i, region in enumerate(self.regions):
            if region.is_border:
                to_see.append(i)
        while to_see:
            region = self.regions[to_see.pop()]
            region.biome = 'SEA'
            for i in region.adjacent_regions:
                if i >= 0:
                    adjacent_region = self.regions[i]
                    if adjacent_region.biome == 'LAKE':
                        to_see.append(i)

    def set_altitude(self):
        self.altitudes = [0] * len(self.vertices)
        graph = self.get_vertices_graph()
        queue = [(i_vertice, 0) for i_vertice in self.get_zero_altitude_vertices()]
        visited = [False] * len(self.vertices)
        # Set altitudes to vertices
        for i_vertice, _ in queue:
            visited[i_vertice] = True
        while queue:
            i_vertice, altitude = queue.pop(0)
            self.altitudes[i_vertice] = altitude
            for i_neighbor in graph[i_vertice]:
                if not visited[i_neighbor]:
                    visited[i_neighbor] = True
                    queue.append((i_neighbor, altitude+1))
        # Set altitudes to points
        for region in self.regions:
            region.altitude = sum(self.altitudes[i] for i in region.vertices) / len(region.vertices)
        # Normalize altitudes
        max_altitude = max(region.altitude for region in self.regions)
        for region in self.regions:
            region.altitude /= max_altitude

    def get_zero_altitude_vertices(self):
        vertices = set()
        for region in self.regions:
            if region.biome == 'SEA':
                for _, i_ridge in region.adjacent_regions.items():
                    i_vertice1, i_vertice2 = self.ridges[i_ridge]
                    vertices.add(i_vertice1)
                    vertices.add(i_vertice2)
        return vertices


    def get_vertices_graph(self):
        graph = [[] for _ in self.vertices]
        for i_vertice1, i_vertice2 in self.ridges:
            graph[i_vertice1].append(i_vertice2)
            graph[i_vertice2].append(i_vertice1)
        return graph

    def plot(self, ax=None):
        ax = ax or plt.subplot('111')
        plt.gca().set_aspect('equal', adjustable='box')
        # Plot regions
        for region in self.regions:
            polygon = Polygon([self.vertices[i] for i in region.vertices], True, fc=region.get_color())
            ax.add_patch(polygon)
        # Altitude
        #if self.altitudes:
        #    for i, (x, y) in enumerate(self.vertices):
        #        plt.scatter(x, y, c='g')
        #        plt.annotate(self.altitudes[i], xy=(x, y), xytext=(5, 2), textcoords='offset points', ha='right', va='bottom')

if __name__ == '__main__':
    plt.subplot('221')
    diagram = get_relaxed_voronoi(1024, 2)
    diagram.plot()
    map = Map()
    map.from_diagram(diagram)
    map.plot(plt.subplot('222'))
    plt.subplot('223')
    mask = generate_coast_mask(256, 4, 16, 0.5, 100, gaussian_kernel(0.5))
    plt.imshow(mask, cmap='gray', origin='lower')
    map.set_coasts(mask)
    map.plot(plt.subplot('224'))
    plt.show()

