import cv2
import sys
import socket
import datetime

class Client:
	def __init__(self, address, port):
		self.address = address
		self.port = port

	def send_img(self, sock, img):
		img_raw = img.tostring()
		size = "{}".format(len(img_raw)).encode('utf-8')
		sock.send(size)
		sock.send(img_raw)

		now = datetime.datetime.now()
		sys.stdout.write("\r[{}]send msg:{}".format(now, size))
		sys.stdout.flush()
		
	def start(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.address, self.port))
		print("Connected:{} {}".format(self.address, self.port))

		capture = cv2.VideoCapture(0)
		print("Camera open")
		while True:
			ret, frame = capture.read()
			if ret == None:
				continue
			self.send_img(sock, frame)

			k = cv2.waitKey(1)
			if k == 27:
				break

		capture.release()
		cv2.destroyAllWindows()
		sock.close()
		print("Disconnect")

def main():
	argv = sys.argv
	argc = len(argv)

	if argc != 3:
		print("Usage: python {} address port".format(argv[0]))
		quit(-1)

	address = argv[1]
	port = int(argv[2])

	client = Client(address, port)
	client.start()

if __name__ == '__main__':
	main()
