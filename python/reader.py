import cv2
import numpy as np
from pyzbar.pyzbar import decode
import darknet_video

def convert(img):
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

	ret, pic = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

	return ret, pic

def binary(img):
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
		cv2.THRESH_BINARY, 11, 2)

	return binary

def read_barcode(img, detections):
	points = darknet_video.convert(detections)
		for point in points:				
			x = point[0]
			y = point[1]
			w = point[2]
			h = point[3]	
			try:
				cut_img = img[y:h, x:w]
				cut_img = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)
				data = decode(img)

				return data[0][0].decode("utf-8", "ignore")
			except Exception as e:
				return None
				print(e)
