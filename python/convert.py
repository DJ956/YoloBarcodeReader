import cv2
import sys
import os
import glob
import numpy as np
from pyzbar.pyzbar import decode
import darknet_video

CFG = "./cfg/yolov3_bb.cfg"
WEIGHT = "./backup/bb/yolov3_bb_last.weights"
META = "./cfg/bb.data"

WIDTH = 640
HEIGHT = 480

#resize gray 59%
#gray 62%
#resize gray binary 6.9%
#gray binary 35%

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


def read(img):
	try:
		result = decode(img)
		return True, result[0][0]
	except Exception as e:
		return False, -1

def write(fp, flag, num, file):
	txt = ""
	if flag:
		txt = "{}:{}".format(os.path.basename(file), num)
		fp.write(txt)
	else:
		txt = "{}:{}".format(os.path.basename(file), "failed")
		fp.write(txt)

	fp.write("\n")
	fp.flush()

#pyzbar only
def exe_py(folder):
	with open("result_py.txt", "a") as f:
		files = glob.glob(folder + os.sep + "*.png")
		count = 0
		for file in files:
			img = cv2.imread(file)
			flag, num = read(img)
			if flag:
				count = count + 1
			write(f, flag, num, file)

	per = count / len(files) * 100
	print("-"*100)
	print("{}/{}".format(count, len(files)))
	print("{}%".format(per))

#grayscale
def exe_py_gray(folder, is_denoising):
	with open("result_gray.txt", "a") as f:
		files = glob.glob(folder + os.sep + "*.png")
		count = 0
		for file in files:
			img = cv2.imread(file)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			if is_denoising:
				gray = cv2.fastNlMeansDenoising(gray, None, 10, templateWindowSize=7, searchWindowSize=21)	

			flag, num = read(gray)
			if flag:
				count += 1

			write(f, flag, num, file)
			#gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
			#binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
			#	cv2.THRESH_BINARY, 11, 2)

	per = count / len(files) * 100
	print("-"*100)
	print("{}/{}".format(count, len(files)))
	print("{}%".format(per))


def exe_py_yolo(folder, is_gray, is_denoising):
	yolo = darknet_video.YOLO(CFG, WEIGHT, META)
	yolo.start_yolo()

	with open("result_yolo.txt", "a") as f:
		files = glob.glob(folder + os.sep + "*.png")
		count = 0
		for file in files:
			img = cv2.imread(file)

			detections, resize_img = yolo.run_yolo(img)
			if len(detections) > 0:
				barcode = cut_barcode(resize_img, detections, is_gray)
				if is_denoising:
					barcode = cv2.fastNlMeansDenoising(barcode, None, h=10, templateWindowSize=7, searchWindowSize=21)

				#cv2.imwrite("{}_y.png".format(count), barcode)
				flag, num = read(barcode)
				if flag:
					count += 1
				#	print("S")
				write(f, flag, num, file)
			else:
				#print("F")
				write(f, False, -1, file)

	per = count / len(files) * 100
	print("-"*100)
	print("{}/{}".format(count, len(files)))
	print("{}%".format(per))




def main():
	argv = sys.argv
	if len(argv) != 3:
		print("Usage: python {} folder type(1:pyonly 2:gray 3:gray&denoising, 4:yolo 5:yolo&gray 6:yolo&gray&denoising)".format(argv[0]))
		quit(-1)

	folder = argv[1]
	mode = int(argv[2])

	if mode == 1:
		exe_py(folder)
	elif mode == 2:
		exe_py_gray(folder, False)
	elif mode == 3:
		exe_py_gray(folder, True)
	elif mode == 4:
		exe_py_yolo(folder, False, False)
	elif mode == 5:
		exe_py_yolo(folder, True, False)
	elif mode == 6:
		exe_py_yolo(folder, True, True)


if __name__ == "__main__":
	main()