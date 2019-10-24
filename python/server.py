import socket
import threading
import sys
import numpy as np
import cv2

BUFFER_IMG = 480 * 640 * 3
BUFFER_MSG = 13

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
		while True:
			try:
				data = con.recv(BUFFER_MSG)
			except ConnectionResetError:
				self.remove_connection(con, address)
				break
			else:
				if not data:
					self.remove_connection(con, address)
					break
				else:					
					msg = data.decode('utf-8')
					print("Recieve:{} - {}".format(address, msg))
					width, height, size = msg.split(",")
					return int(size)

	def read_img(self, con, address):
		while True:
			try:
				data = con.recv(BUFFER_IMG)
			except ConnectionResetError:
				self.remove_connection(con, address)
				break
			else:
				if not data:
					self.remove_connection(con, address)
					break
				else:
					img_raw = np.frombuffer(data, dtype=np.uint8)
					img = np.reshape(img_raw, (480, 640, 3))				
					return img
			

	def handler(self, con, address):		
		#self.read_msg(con, address)
		img = self.read_img(con, address)
		cv2.imshow("server:{}".format(address), img)

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