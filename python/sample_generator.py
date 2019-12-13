import cv2
import sys
import os
import numpy as np
import darknet_video

CFG = "./cfg/yolov3_bb.cfg"
WEIGHT = "./backup/bb/yolov3_bb_last.weights"
META = "./cfg/bb.data"

def main():

	argv = sys.argv
	if len(argv) != 3:
		print("Usage: python {} out_folder ext(*.bmp|*.png)".format(argv[0]))
		quit(-1)

	out_folder = argv[1]
	ext = argv[2]

	cap = cv2.VideoCapture(0)
	yolo = darknet_video.YOLO(CFG, WEIGHT, META)
	yolo.start_yolo()

	idx = 0
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == None:
			continue
		try:
			detections, resize_img = yolo.run_yolo(frame)
			if len(detections) > 0:
				points = darknet_video.convert(detections)
				for point in points:
					x,y,w,h = point[0], point[1], point[2], point[3]
					cut_img = resize_img[y:h, x:w]

					cv2.imshow("Frame", cut_img)				
					name = os.path.basename(src).split(".")[0]
					cv2.imwrite("{}/{}_{}.{}".format(out_folder, name, idx, ext), cut_img)

			idx += 1
		except:
			print("error")

		if cv2.waitKey(1) == 27:
			break


	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()