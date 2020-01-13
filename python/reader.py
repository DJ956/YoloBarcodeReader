import cv2
import numpy as np
import pyocr
import pyocr.builders
from PIL import Image
from pyzbar.pyzbar import decode
import darknet_video

def cv2pil(img):
	new_img = img.copy()
	if new_img.ndim == 2:
		pass
	elif new_img.shape[2] == 3:
		new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
	elif new_img.shape[2] == 4:
		new_img = cv2.cvtColor(new_img, cv2.COLOR_BGRA2RGBA)
	new_img = Image.fromarray(new_img)
	return new_img

#画像からバーコードが移っている部分を切り取る 本来の部分から0.1倍拡大している
def cut_barcode(img, detections):
	scale = 0.1
	points = darknet_video.convert(detections)
	for point in points:
		x = point[0] - int(point[0] * scale)
		y = point[1] - int(point[1] * scale)
		w = point[2] + int(point[2] * scale)
		h = point[3] + int(point[3] * scale)

		cut_img = img[y:h, x:w]

		h,w,c = cut_img.shape
		if h == 0 or w == 0:
			return None

		cut_img = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)
		return cut_img

#バーコード画像から数字の部分のみを切り出す
def cut_num(img):
	start = 0.75
	h,w = img.shape

	if h > w:
		start = (int(1 - start) * w)
		cut = img[0:h, 0:start]
		cut = cv2.rotate(cut, cv2.ROTATE_90_COUNTERCLOCKWISE)
		return cut
	else:
		start = int(start * h)
		cut = img[start:h, 0:w]
		return cut

#tesseract-orcで数字を直接読み取る
def read_barcode_ocr(img, detections, tool):
	try:
		img = cut_barcode(img, detections)
		if img is None:
			return False, -1
		img = cut_num(img)
		txt = tool.image_to_string(
			cv2pil(img),
			builder=pyocr.tesseract.DigitBuilder())

		txt = txt.strip()
		txt = txt.replace('-', '')
		txt = txt.replace('.', '')

		return len(txt) > 0, txt
	except Exception as e:
		return False, -1

#pyzbarで番号を読み取る
def read_barcode_pyzbar(img):
	try:
		data = decode(img)
		return True, data[0][0].decode("utf-8", "ignore")
	except Exception as e:
		return False, -1