import cv2
import sys
import os
import glob
import numpy as np
from pyzbar.pyzbar import decode


def exe(folder):
	scale = 1.5
	with open("result.txt", "a") as f:
		for file in glob.glob(folder, "*.png"):
			img = cv2.imread(file)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

			binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
				cv2.THRESH_BINARY, 11, 2)

			try:
				result = decode(gray)
				txt = "{}:{}".format(os.basename(file), result)
				f.write(txt)
			except Exception as e:
				txt = "{}:{}".format(os.basename(file), "failed")
				f.write(txt)
			finally:
				print(txt)
				f.write("\n")
		f.flush()



def main():
	argv = sys.argv
	if len(argv) != 2:
		print("Usage: python {} folder".format(argv[0]))
		quit(-1)

	exe(folder)

if __name__ == "__main__":
	main()