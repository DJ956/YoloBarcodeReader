import cv2
import sys
import os

def main():
	argv = sys.argv
	if len(argv) != 2:
		print("Usage: python {} output_folder".format(argv[0]))
		quit(-1)

	output_folder = argv[1]

	cap = cv2.VideoCapture(0)
	idx = 0
	while True:
		ret, frame = cap.read()
		if ret == None:
			continue

		path = "{}/{}.png".format(output_folder, idx)

		print(path)
		cv2.imwrite(path, frame)
		idx += 1

		cv2.imshow("samp", frame)

		if cv2.waitKey(1) == 27:
			break

	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()