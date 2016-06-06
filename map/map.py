import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from diagram import get_relaxed_voronoi
from coasts import generate_coast_mask, gaussian_kernel

colors = {'SEA': 'b', 'LAND': 'g', 'LAKE': '#50a0b0'}

class Region:
    def __init__(self, point, vertices=None, is_border=False):
        self.point = point # ID
        self.vertices = vertices or [] # IDs
        self.adjacent_regions = {} # {i_point: i_ridge}
        self.biome = 'LAKE'
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

    def plot(self, ax=None):
        ax = ax or plt.subplot('111')
        plt.gca().set_aspect('equal', adjustable='box')
        # Plot regions
        for region in self.regions:
            polygon = Polygon([self.vertices[i] for i in region.vertices], True, fc=colors[region.biome])
            ax.add_patch(polygon)

if __name__ == '__main__':
    plt.subplot('221')
    diagram = get_relaxed_voronoi(256, 2)
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

