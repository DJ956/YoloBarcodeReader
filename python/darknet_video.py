from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import darknet

def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax

def convert(detections):
	points = []
	for detection in detections:
		x, y, w, h = detection[2][0],\
					detection[2][1],\
					detection[2][2],\
					detection[2][3]
		xmin, ymin,xmax, ymax = convertBack(
			float(x), float(y), float(w), float(h))

		point = [xmin, ymin, xmax, ymax]
		points.append(point)
		
	return points


def cvDrawBoxes(detections, img):
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        xmin, ymin, xmax, ymax = convertBack(
            float(x), float(y), float(w), float(h))
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
        cv2.putText(img,
                    detection[0].decode() +
                    " [" + str(round(detection[1] * 100, 2)) + "]",
                    (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    [0, 255, 0], 2)
    return img

class YOLO():
	def __init__(self, cnf_path, weight_path, meta_path):
		self.cnf_path = cnf_path
		self.weight_path = weight_path
		self.meta_path = meta_path

		self.netMain = None
		self.metaMain = None
		self.altNames = None

		if not os.path.exists(self.cnf_path):
			raise ValueError("Invalid config path {}".format(os.path.abspath(self.cnf_path)))
		if not os.path.exists(self.weight_path):
			raise ValueError("Invalid weight path {}".format(os.path.abspath(self.weight_path)))
		if not os.path.exists(self.meta_path):
			raise ValueError("Invalid data file path {}".format(os.path.abspath(self.meta_path)))

	def start_yolo(self):
		if self.netMain is None:
			self.netMain = darknet.load_net_custom(self.cnf_path.encode("ascii"), self.weight_path.encode("ascii"), 0, 1)  # batch size = 1

		if self.metaMain is None:
			self.metaMain = darknet.load_meta(self.meta_path.encode("ascii"))

		if self.altNames is None:
			try:
				with open(self.meta_path) as metaFH:
					metaContents = metaFH.read()
					import re
					match = re.search("names *= *(.*)$", metaContents, re.IGNORECASE | re.MULTILINE)

					if match:
						result = match,group(1)
					else:
						result = None
					try:
						if os.path.exists(result):
							with open(result) as namesFH:
								nameList = namesFH.read().strip().split("\n")
								self.altNames = [x.strip() for x in nameList]
					except TypeError:
						pass
			except Exception:
				pass
		"""
		self.out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"MJPG"), 10.0,
			(darknet.network_width(self.netMain), darknet.network_height(self.netMain)))
		"""
		self.darknet_image = darknet.make_image(darknet.network_width(self.netMain),
												darknet.network_height(self.netMain), 3)


	def run_yolo(self, frame_read):		
		frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
		frame_resized = cv2.resize(frame_rgb,
									(darknet.network_width(self.netMain),
									darknet.network_height(self.netMain)))

		darknet.copy_image_from_bytes(self.darknet_image, frame_resized.tobytes())
		detections = darknet.detect_image(self.netMain, self.metaMain, self.darknet_image, thresh=0.25)

		return detections, frame_resized
