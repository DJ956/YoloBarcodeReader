import socket
import threading
import sys
import datetime
import numpy as np
import cv2
import time
import pyocr
import pyocr.builders
from pyzbar.pyzbar import decode
import darknet_video
import reader
import itemdb

BUFFER_IMG = 4096
BUFFER_SIZE = 6
BUFFER_FLAG = 1

MAX_ACCEPT = 10

CFG = "./cfg/yolov3_bb.cfg"
WEIGHT = "./backup/bb/yolov3_bb_last.weights"
META = "./cfg/bb.data"

#db
HOST = "localhost"
USER = "rapit"
PW = "pass"
DB = "rapit_cart"

WIDTH = 640
HEIGHT = 480

IMG_STACK_SIZE = 10
INSERT_FLAG = 1
DELETRE_FLAG = 2

FAILED = "0"
SUCCESS = "1"

class Server:
	def __init__(self, own_address, port):
		tools = pyocr.get_available_tools()
		if len(tools) == 0:
			print("Not found tools")
			quit(-1)

		self.tool = tools[0]
		print("OCR tool name:{}".format(self.tool.get_name()))
		self.address = own_address
		self.port = port
		self.clients = []
		self.Yolo = darknet_video.YOLO(CFG, WEIGHT, META)
		self.Yolo.start_yolo()
		self.db = itemdb.itemdb(host=HOST, user=USER, pw=PW, db=DB)

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

	def read_msg(self, con, address, buffer):
		try:
			data = con.recv(buffer)
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

	"""
	成否の送信
	"""
	def send_mode(self, con, address, mode):
		mode = "{}".format(mode).encode('utf-8')
		con.send(mode)

	def read_data(self, con, address):
		data = []
		data_size = 0
		for i in range(IMG_STACK_SIZE):
			size = self.read_msg(con, address, BUFFER_SIZE)
			img = self.read_img(con, address, size)
			data.append(img)
			data_size += size

		for x in range(IMG_STACK_SIZE):
			cv2.imwrite("./{}.png".format(x), data[x])

		flag = self.read_msg(con, address, BUFFER_FLAG)
		data.append(flag)

		data_size += 1
		return data, data_size

	#dbに商品コードを書き込む、削除する
	def write2db(self, con, address, number, flag):
		if flag == INSERT_FLAG:
			print("[+]detect:{}".format(number))
			self.send_mode(con, address, SUCCESS)
			self.db.insert(code=number, cart_id=1)
		elif flag == DELETRE_FLAG:
			print("[-]detect:{}".format(num))
			self.send_mode(con, address, SUCCESS)
			self.db.delete(code=number, cart_id=1)


	def handler(self, con, address):
		failed_flag = True
		while True:
			data, size = self.read_data(con, address)
			for i in range(IMG_STACK_SIZE):
				#最初にpyzbarで読み取る
				is_detect, num = reader.read_barcode_pyzbar(data[i])
				if is_detect:
					self.write2db(con, address, num, flag=data[IMG_STACK_SIZE])
					failed_flag = False
					print("pyzbar")
					break

				#pyzbarが失敗したらyoloとtesseract-ocrで試す
				detections, resize_img = self.Yolo.run_yolo(data[i])
				if len(detections) < 0:
					continue

				is_detect, num = reader.read_barcode_ocr(resize_img, detections, self.tool)
				if is_detect:
					self.write2db(con, address, num, flag=data[IMG_STACK_SIZE])
					failed_flag = False
					print("tesseract-ocr")
					break

			#あかんかった場合
			if failed_flag:
				self.send_mode(con, address, FAILED)
				print("failed")

			print("Flag:{}".format(data[IMG_STACK_SIZE]))

			now = datetime.datetime.now()
			print("[{}]From:{} - {}".format(now, address, size))

		self.remove_connection(con, address)

def main():
	argv = sys.argv
	argc = len(argv)
	if argc != 3:
		print("Usage: python {} own_address port".format(argv[0]))
		quit(-1)

	own_address = argv[1]
	port = int(argv[2])	
	server = Server(own_address, port)
	server.start()

if __name__ == '__main__':
	main()