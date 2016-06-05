import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from diagram import get_relaxed_voronoi

colors = {'WATER': 'b', 'LAND': 'g'}

class Region:
    def __init__(self, point, vertices=None, is_border=False):
        self.point = None # ID
        self.vertices = vertices or [] # IDs
        self.adjacent_regions = {} # {i_point: i_ridge}
        self.biome = 'LAND'
        self.is_border = is_border

class Map:
    def __init__(self):
        self.points = [] # Coordinates
        self.vertices = [] # Coordinates
        self.ridges = [] # [(i_vertice1, i_vertice2)]
        self.regions = []

    def from_diagram(self, diagram):
        self.points = diagram.points
        self.vertices = diagram.vertices
        self.ridges = diagram.ridge_vertices
        for i_point, (i_vertices, is_border) in enumerate(zip(diagram.regions, diagram.is_border)):
            self.regions.append(Region(i_point, i_vertices, is_border))
            if is_border:
                self.regions[-1].biome = 'WATER'
        for i_ridge, (i_point1, i_point2) in enumerate(diagram.ridge_points):
            self.regions[i_point1].adjacent_regions[i_point2] = i_ridge
            self.regions[i_point2].adjacent_regions[i_point1] = i_ridge

    def plot(self):
        fig, ax = plt.subplots()
        plt.gca().set_aspect('equal', adjustable='box')
        # Plot regions
        for region in self.regions:
            polygon = Polygon([self.vertices[i] for i in region.vertices], True, color=colors[region.biome])
            ax.add_patch(polygon)
        # Plot ridges
        for (v1, v2) in self.ridges:
            x1, x2, y1, y2 = self.vertices[v1][0], self.vertices[v2][0], self.vertices[v1][1], self.vertices[v2][1]
            plt.plot([x1, x2], [y1, y2], c='k')
        # Plot points
        for i, (x, y) in enumerate(self.points):
            if self.regions[i].is_border:
                plt.scatter(x, y, c='r')
            else:
                plt.scatter(x, y)
        for x, y in self.vertices:
            plt.scatter(x, y, c='g')

if __name__ == '__main__':
    diagram = get_relaxed_voronoi(128, 2)
    map = Map()
    map.from_diagram(diagram)
    map.plot()
    plt.show()

