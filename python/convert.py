import cv2
import sys
import numpy as np
from pyzbar.pyzbar import decode

def main():
	argv = sys.argv
	if len(argv) != 2:
		print("Usage: python {} img".format(argv[0]))
		quit(-1)

	img = cv2.imread(argv[1])
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	h,w = gray.shape
	scale = 3
	#gray = cv2.resize(gray, (h * scale, w * scale), interpolation=cv2.INTER_CUBIC)

	binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
		cv2.THRESH_BINARY, 11, 2)
	#ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	

	kernel = np.ones((3,3), np.uint8)
	opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
	closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

	cv2.imshow("gray", gray)
	cv2.imshow("binary", binary)
	cv2.imshow("opening", opening)
	cv2.imshow("closing", closing)

	result = decode(gray)
	print("Gray  :{}".format(result[0][0]))
	result = decode(binary)
	print("Binary:{}".format(result[0][0]))


	cv2.waitKey(0)

	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()