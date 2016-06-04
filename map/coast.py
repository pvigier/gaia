import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2, snoise2

size = 128
octaves = 32
freq = 4 # A lot more islands
persistence = 0.4 # More noisy contours
offset = np.random.randint(size)
threshold = 256 * 0.3 # Larger islands
sigma = 1 # Center the land

noise = np.zeros((size, size), dtype=np.uint8)
for i in range(size):
	for j in range(size):
		noise[i, j] = pnoise2(offset + j * freq / size, offset + i * freq / size, octaves, persistence) * 127.0 + 128
#noise = noise  * (noise > 0)
kernel = np.zeros((size, size))
for i in range(size):
	for j in range(size):
		x = (i - size / 2) / size * np.pi
		y = (j - size / 2) / size * np.pi
		kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma))
print(kernel)
plt.subplot('221')
plt.imshow(noise, cmap='gray')
plt.subplot('222')
plt.imshow(kernel, cmap='gray')
plt.subplot('223')
plt.imshow(noise * kernel, cmap='gray')
plt.subplot('224')
plt.imshow(noise * kernel > threshold, cmap='gray')
plt.show()