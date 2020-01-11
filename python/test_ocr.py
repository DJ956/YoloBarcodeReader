import cv2
import sys
import os
import glob
import time
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

def read_num(img, tool):
	txt = tool.image_to_string(
		cv2pil(img),
		builder=pyocr.tesseract.DigitBuilder())

	txt = txt.strip()
	txt = txt.replace('-', '')
	txt = txt.replace('.', '')

	return len(txt) > 0, txt


def cut_barcode(img, detections, is_gray):
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

		if is_gray:
			cut_img = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)
		return cut_img

def cut_num(img):
	start = 0.75
	h,w = img.shape

	#幅より高さのほうが大きかった場合数字は左右のどちらか
	if h > w:
		start = int((1 - start) * w)
		cut = img[0:h, 0:start]
		cut = cv2.rotate(cut, cv2.ROTATE_90_COUNTERCLOCKWISE)
		return cut
	else:#逆の場合数字は上下のどちらか(この場合下しか想定していない)
		start = int(start * h)
		cut = img[start:h, 0:w]
		return cut

def exe_yolo(files):
	tools = pyocr.get_available_tools()
	if len(tools) == 0:
		print("Not found tools")
		quit(-1)
	tool = tools[0]

	yolo = darknet_video.YOLO(CFG, WEIGHT, META)
	yolo.start_yolo()

	start = time.time()

	count = 0
	idx = 0
	ANSW = "4901121172880"
	if os.path.exists("result.txt"):
		os.remove("result.txt")

	with open("result.txt", "a") as f:
		for file in files:
			img = cv2.imread(file)
			detections, resize_img = yolo.run_yolo(img)
			if len(detections) > 0:
				barcode = cut_barcode(resize_img, detections, True)
				if barcode is None:
					continue
				num_img = cut_num(barcode)

				gamma = 1.8
				imax = num_img.max()
				num_img = imax * (num_img / imax) ** (1/gamma)

				cv2.imwrite("./cut/{}".format(os.path.basename(file)), num_img)

				flag, num = read_num(num_img, tool)
				#桁数が12だった場合、先頭に4を追加する
				if len(num) == 12 and num[0] != "4":
					 num = "4{}".format(num)
				#桁数が13だった場合、先頭の1桁を削除する
				if len(num) > 13:
					num = num[1:]

				if flag and num == ANSW:
					count += 1
				f.write("Code:{} - File:{}\n".format(num, file))

				sys.stdout.write("\r[{}/{}]".format(idx, len(files)))
				sys.stdout.flush()

			idx += 1

	end = time.time()

	per = count / len(files) * 100
	print("-" *  100)
	print("{}/{}".format(count, len(files)))
	print("{}%".format(per))

	print("time:{}s".format(end - start))


def main():
	argv = sys.argv

	folder = argv[1]
	files = glob.glob(folder + os.sep + "*.png")
	exe_yolo(files)

if __name__ == "__main__":
	main()