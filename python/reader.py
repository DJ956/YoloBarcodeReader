import cv2
import numpy as np
from pyzbar.pyzbar import decode

def convert(img):
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

	ret, pic = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

	return ret, pic

def read_barcode(img):
	data = decode(img)
	if not data:
		return None
	return data[0][0].decode("utf-8", "ignore")