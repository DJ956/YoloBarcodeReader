import cv2
import sys
import os
import glob
import numpy as np
from pyzbar.pyzbar import decode

#resize gray 59%
#gray 62%
#resize gray binary 6.9%
#gray binary 35%

def exe(folder):
	scale = 1.5
	os.remove("result.txt")

	with open("result.txt", "a") as f:
		files = glob.glob(folder + os.sep + "*.png")
		count = 0
		for file in files:
			img = cv2.imread(file)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			#gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

			gray = cv2.fastNlMeansDenoising(gray, None, h=10, templeteWindowSize=7, searchWindowSize=21)

			#binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
			#	cv2.THRESH_BINARY, 11, 2)

			txt = ""
			try:
				result = decode(gray)
				txt = "{}:{}".format(os.path.basename(file), result[0][0])
				f.write(txt)
				count += 1
			except Exception as e:
				txt = "{}:{}".format(os.path.basename(file), "failed")
				f.write(txt)
			finally:
				print(txt)
				f.write("\n")
		f.flush()

	per = count / len(files) * 100
	print("-"*100)
	print("{}/{}".format(count, len(files)))
	print("{}%".format(per))



def main():
	argv = sys.argv
	if len(argv) != 2:
		print("Usage: python {} folder".format(argv[0]))
		quit(-1)

	exe(argv[1])

if __name__ == "__main__":
	main()