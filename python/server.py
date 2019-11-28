import socket
import threading
import sys
import datetime
import numpy as np
import cv2
import time
from pyzbar.pyzbar import decode
import darknet_video

BUFFER_IMG = 4096
BUFFER_MSG = 6

MAX_ACCEPT = 10

CFG = "./cfg/yolov3_bb.cfg"
WEIGHT = "./backup/bb/yolov3_bb_last.weights"
META = "./cfg/bb.data"

WIDTH = 640
HEIGHT = 480

class Server:
	def __init__(self, own_address, port, out_path):
		self.address = own_address
		self.port = port
		self.clients = []
		self.out = cv2.VideoWriter(
			out_path, cv2.VideoWriter_fourcc(*"MJPG"), 10.0,
			(WIDTH, HEIGHT))
		self.Yolo = darknet_video.YOLO(CFG, WEIGHT, META)
		self.Yolo.start_yolo()

	def remove_connection(self, con, address):
		con.close()
		print("[-]Disconnect:{}".format(address))
		self.clients.remove((con, address))

	def start(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((self.address, self.port))
		sock.listen(MAX_ACCEPT)
		print("Start server {}:{}".format(self.address, self.port))

		while True:
			con, address = sock.accept()
			print("[+]Connected:{}".format(address))
			self.clients.append((con, address))
			handle_thread = threading.Thread(target=self.handler,
											args=(con, address),
											daemon=True)
			handle_thread.start()

	def read_msg(self, con, address):
		try:
			data = con.recv(BUFFER_MSG)
		except ConnectionResetError:
			self.remove_connection(con, address)

		msg = data.decode('utf-8')						
		return int(msg)

	def read_img(self, con, address, size):		
		
		data = b''
		while len(data) < size:
			try:
				to_read = size - len(data)
				data += con.recv(BUFFER_IMG if to_read > BUFFER_IMG else to_read)
			except ConnectionResetError:
				self.remove_connection(con, address)
				break
				
		img_raw = np.frombuffer(data, dtype=np.uint8)		
		img = np.reshape(img_raw, (480, 640, 3))
				
		return img
			

	def read_barcode(self, img):
		data = decode(img)
		if not data:
			return None
		return data[0][0].decode("utf-8", "ignore")

	def handler(self, con, address):
		while True:		
			size = self.read_msg(con, address)
			img = self.read_img(con, address, size)

			prev_time = time.time()
			detections, resize_img = self.Yolo.run_yolo(img)
			#print("FPS:{}".format(1/(time.time() - prev_time)))

			if len(detections) > 0:
				points = darknet_video.convertBack(detections)
				for point in points:
					cut_img = resize_img[point[0], point[1], point[2], point[3]]
					cv2.imshow("demo", cut_img)					

			#resize_img = darknet_video.cvDrawBoxes(detections, resize_img)
			data = self.read_barcode(resize_img)
			if not data is None:
				print("Code:{}".format(data))

			now = datetime.datetime.now()
			sys.stdout.write("\r[{}]From:{} - {}".format(now, address, size))
			sys.stdout.flush()

			#self.out.write(resize_img)
			if cv2.waitKey(1) == 27:
				break

		#self.out.release()
		cv2.destroyAllWindows()
		self.remove_connection(con, address)


def main():
	argv = sys.argv
	argc = len(argv)
	if argc != 4:
		print("Usage: python {} own_address port out(*.avi)".format(argv[0]))
		quit(-1)

	own_address = argv[1]
	port = int(argv[2])
	out_path = argv[3]
	server = Server(own_address, port, out_path)
	server.start()

if __name__ == '__main__':
	main()