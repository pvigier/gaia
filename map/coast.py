import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2, snoise2

# Kernel to shape particular form of islands

def uniform_kernel():
	return lambda x: 1

def gaussian_kernel(sigma):
	return lambda x: np.exp(-x**2/(2 * sigma ** 2))

def get_weights(size, kernel):
	weights = np.zeros((size, size))
	for i in range(size):
		for j in range(size):
			d = np.sqrt(((i - size / 2) / size) ** 2 + ((j - size / 2) / size) ** 2)
			weights[i, j] = kernel(d)
	return weights

def get_noise(size, freq, octaves, persistence):
	offset = np.random.randint(size)
	perlin = np.zeros((size, size), dtype=np.uint8)
	for i in range(size):
		for j in range(size):
			perlin[i, j] = pnoise2(offset + j * freq / size, offset + i * freq / size, octaves, persistence) * 127.0 + 128
	return perlin

def generate_coast_mask(size, freq=1, octaves=32, persistence=0.5, threshold=128, kernel=uniform_kernel):
	return (get_noise(size, freq, octaves, persistence) * get_weights(size, kernel)) >= threshold

def plot_coast(size, freq=1, octaves=32, persistence=0.5, threshold=100, kernel=uniform_kernel):
	perlin = get_noise(size, freq, octaves, persistence)
	weights = get_weights(size, kernel)
	weighted_perlin = perlin * weights
	coasts = weighted_perlin >= threshold
	plt.subplot('221')
	plt.imshow(perlin, cmap='gray')
	plt.subplot('222')
	plt.imshow(weights, cmap='gray')
	plt.subplot('223')
	plt.imshow(weighted_perlin, cmap='gray')
	plt.subplot('224')
	plt.imshow(coasts, cmap='gray')
	plt.show()

if __name__ == '__main__':
	plot_coast(256, 4, 16, 0.5, 100, gaussian_kernel(0.4))