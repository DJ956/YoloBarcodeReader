import socket
import threading
import sys

class Server:
	def __init__(self, port):
		self.address = "localhost"
		self.port = port
		self.clients = []

	def remove_connection(self, con, address):
		con.close()
		print("Disconnect:{}".format(address))
		self.clients.remove((con, address))

	def start(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((self.address, self.port))
		sock.listen(10)
		print("Start server {}:{}".format(self.address, self.port))

		while True:
			con, address = sock.accept()
			print("Connected:{}".format(address))
			self.clients.append((con, address))
			handle_thread = threading.Thread(target=self.handler,
											args=(con, address),
											daemon=True)
			handle_thread.start()

	def handler(self, con, address):
		while True:
			try:
				data = con.recv(1024)
			except ConnectionResetError:
				self.remove_connection(con, address)
				break
			else:
				if not data:
					self.remove_connection(con, address)
					break
				else:
					msg = data.decode("utf-8")
					print("Recieve:{} - {}".format(address, msg))

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