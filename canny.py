import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('../computer-vision/pp/combinedPositives1/115img.jpg',0)
edges = cv.Canny(img, 100, 200)
#vary 100 and 200 somehow

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'),plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image' ), plt.xticks([]), plt.yticks([])

plt.show()