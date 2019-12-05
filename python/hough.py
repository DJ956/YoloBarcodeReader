import cv2
import sys
import numpy as np

class hough:

	def __init__(self, exp = 1):
		self.exp = exp

	def convert(self, img):
		result = []
		h,w,c = img.shape
		#resize = cv2.resize(img, (int(w*self.exp), (int(h*self.exp))))
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(gray, 50, 150, apertureSize=3)
		cv2.imshow("edges", edges)
		lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
		
		for line in lines:
			for rho,theta in line:
				a = np.cos(theta)
				b = np.sin(theta)
				x0 = a * rho
				y0 = b * rho
				x1 = int(x0 + 1000 * (-b))
				y1 = int(y0 + 1000 * (a))
				x2 = int(x0 - 1000 * (-b))
				y2 = int(y0)

				result.append(((x1, y1), (x2, y2)))

		return result

def main():
	#img = cv2.imread(sys.argv[1])
	exp = float(sys.argv[1])
	con = hough(exp)
	cap = cv2.VideoCapture(0)
	while True:
		ret, img = cap.read()
		if ret == None:
			continue

		cv2.imshow("raw", img)
		try:
			points = con.convert(img)
			print(points)
			for p in points:
				cv2.line(img, p[0], p[1], (0, 0, 255), 2)
		except:
			print("error")
		
		cv2.imshow("demo", img)

		if cv2.waitKey(1) == 27:
			break
	
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()