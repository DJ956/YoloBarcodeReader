import cv2
import sys
import socket

class Client:
	def __init__(self, address, port):
		self.address = address
		self.port = port

	def start(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.address, self.port))
		print("Connected:{} {}".format(self.address, self.port))

		while True:
			msg = input("Enter message | Exit(exit): ")
			if msg == "exit":
				break
			sock.send(msg.encode('utf-8'))
		"""
		capture = cv2.VideoCapture(0)
		print("Camera open")
		while True:
			ret, frame = capture.read()
			if ret == NULL:
				continue

			cv2.imshow("barcode", frame)


			k = cv2.waitKey(1)
			if k == 27:
				break

		sock.close()
		capture.release()
		cv2.destroyAllWindows()
		"""
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
