import cv2
import numpy as np
import glob
import os

def convert(path):
	root = "./convert_img"
	if not os.path.exists(root):
		os.mkdir(root)

	origin = cv2.imread(path)

	gray = cv2.cvtColor(origin, cv2.COLOR_RGB2GRAY)
	
	#pic = cv2.adaptiveThreshold(gray, 20, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
	#	47, 2)
	#ret, pic = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
	pic = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

	file_name = os.path.basename(path)
	path = "{}/{}_new.png".format(root, file_name)
	cv2.imwrite(path, pic)	
	print("save:{}".format(path))
	

def main():
	for file in glob.glob(".\\barcode_img\\*.png"):		
		convert(file)

if __name__ == "__main__":
	main()
