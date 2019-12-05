import cv2
import numpy as np

class hough:
	def convert(self, path):
		img = cv2.imread(path)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(gray, 50, 150, appertureSize=3)

		lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
		for rho,theta in lines[0]:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a * rho
			y0 = b * rho
			

