import cv2
import sys
import os
import glob
import numpy as np
from PIL import Image
from pyzbar.pyzbar import decode
import darknet_video
import pyocr
import pyocr.builders

CFG = "./cfg/yolov3_bb.cfg"
WEIGHT = "./backup/bb/yolov3_bb_last.weights"
META = "./cfg/bb.data"


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

def read_num(img):
	tools = pyocr.get_available_tools()
	if len(tools) == 0:
		print("Not found availables ocr tools")
		quit(-1)

	tool = tools[0]
	txt = tool.image_to_string(
		cv2pil(img),
		builder=pyocr.builders.TextBuilder(tesseract_layout=6))

	return len(txt) > 0


def cut_barcode(img, detections, is_gray):
	scale = 0.1
	points = darknet_video.convert(detections)
	for point in points:				
		x = point[0] - int(point[0] * scale)
		y = point[1] - int(point[1] * scale)
		w = point[2] + int(point[2] * scale)
		h = point[3] + int(point[3] * scale)	

		cut_img = img[y:h, x:w]
		if is_gray:
			cut_img = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)

		return cut_img

def cut_num(img):
	start = 0.75
	h,w = img.shape

	start = int(start * h)
	cut = img[start:h, 0:w]

	return cut

def exe_yolo(files):
	yolo = darknet_video.YOLO(CFG, WEIGHT, META)
	yolo.start_yolo()

	count = 0
	idx = 0
	for file in files:
		img = cv2.imread(file)
		detections, resize_img = yolo.run_yolo(img)
		if len(detections) > 0:
			barcode = cut_barcode(resize_img, detections, True)
			num_img = cut_num(barcode)

			cv2.imwrite("./cut/{}.png".format(idx), num_img)

			#flag = read_num(num_img)
			#if flag:
			#	count += 1
		idx += 1

	per = count / len(files) * 100
	print("-" *  100)
	print("{}/{}".format(count, len(files)))
	print("{}%".format(per))


def main():
	argv = sys.argv

	folder = argv[1]
	files = glob.glob(folder + os.sep + "*.png")
	exe_yolo(files)

if __name__ == "__main__":
	main()