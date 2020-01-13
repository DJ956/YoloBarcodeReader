import cv2
import sys
import socket
import time
import datetime
import threading
import hcsr04
import RPi.GPIO as GPIO
from weight_sensor import sensor_w
from led import notice_sensor

#商品を取り出すまでの待機猶予
HOLD_TIME = 5

#連続して短い時間でフラグが立つことがあるため待機する
WEIGHT_CHECK_SPAN = 2

#画像スタックサイズ
IMG_STACK_SIZE = 10

SUCCESS = 1
FAILED = 0

class Client:
	def __init__(self, address, port):
		self.address = address
		self.port = port
		self.sensor = hcsr04.sensor()
		self.sensor_w = sensor_w()
		self.flag = 0
		self.stack_flag = []
		self.lock = threading.Lock()
		self.led = notice_sensor()

	def send_img(self, sock, img):
		img_raw = img.tostring()
		size = "{}".format(len(img_raw)).encode('utf-8')
		sock.send(size)
		sock.send(img_raw)

		now = datetime.datetime.now()
		print("[{}]send msg:{}".format(now, size))

	def send_flag(self, sock, flag):
		flag_data = "{}".format(flag).encode('utf-8')
		sock.send(flag_data)
		print("send flag:{}".format(flag_data))

	def send_data(self, sock, data):
		for i in range(IMG_STACK_SIZE):
			self.send_img(sock, data[i])

		self.send_flag(sock, data[IMG_STACK_SIZE])
		self.stack_flag.clear()
		print("-" * 100)

	def read_mode(self, sock):
		try:
			data = sock.recv(1)
		except ConnectionResetError:
			self.remove_connection(con, address)

		mode = data.decode('utf-8')						
		return int(mode)
		
	def handler(self):
		prev = time.time()
		while True:
			print(self.stack_flag)
			self.flag = self.sensor.get_flag()
			weight_flag = self.sensor_w.exe()
			#重量センサーのフラグが変化なし
			if weight_flag == 0:
				continue

			#重量センサーのフラグが変化アリ(-1 or 1) フラグ用のスタックに値を追加
			now = time.time()
			if (now - prev) > WEIGHT_CHECK_SPAN: #2秒以内に0以外のフラグが来たら誤作動の可能性があるので無視
				with self.lock:
					self.stack_flag.append(weight_flag)
			prev = now


	def start(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.address, self.port))
		print("Connected:{} {}".format(self.address, self.port))

		capture = cv2.VideoCapture(0)
		print("Camera open")
		handle_thread = threading.Thread(target=self.handler, daemon=True)
		handle_thread.start()

		data = []
		while True:
			#距離センサーに引っかかる
			if self.flag == 1:
				print("Dis:{}".format(self.sensor.dis))
				self.led.shine(self.led.green)
				for i in range(IMG_STACK_SIZE):
					ret, frame = capture.read()
					if ret == None:
						continue
					data.append(frame)
					time.sleep(0.5)

				#画像を撮り終わった後に追加or削除のフラグスタックを確認する
				#フラグがあった場合
				if self.stack_flag:
					print("A")
					data.append(self.stack_flag.pop())
				#フラグがなかった場合　数秒フラグが出るのを待つ
				else:
					start = time.time()
					while True:
						end = time.time()
						if self.stack_flag:
							print("B")
							data.append(self.stack_flag.pop())
							break
						if end - start > HOLD_TIME:
							print("C")
							data.clear()
							self.stack_flag.clear()
							break

				if not data:
					continue

				#画像群とフラグのセットを送信
				self.send_data(sock, data)
				data.clear()
				mode = self.read_mode(sock)
				if mode == SUCCESS:
					self.led.shine(self.led.blue)
				elif mode == FAILED:
					self.led.shine(self.led.red)



		GPIO.cleanup()
		capture.release()
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
