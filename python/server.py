import socket
import threading
import sys
import datetime
import numpy as np
import cv2

BUFFER_IMG = 4096
BUFFER_MSG = 6

MAX_ACCEPT = 10

class Server:
	def __init__(self, port):
		self.address = "localhost"
		self.port = port
		self.clients = []

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
			

	def handler(self, con, address):
		cnt = 0
		while True:		
			size = self.read_msg(con, address)
			img = self.read_img(con, address, size)

			now = datetime.datetime.now()
			sys.stdout.write("\r[{}]From:{} - {}".format(now, address, size))
			sys.stdout.flush()

			path = "./img/img_{}.jpg".format(cnt)
			cv2.imwrite(path, img)
			cnt = cnt + 1


def main():
	argv = sys.argv
	argc = len(argv)
	if argc != 2:
		print("Usage: python {} port".format(argv[0]))
		quit(-1)

	port = int(argv[1])
	server = Server(port)
	server.start()

if __name__ == '__main__':
	main()