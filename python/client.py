import cv2
import sys
import socket
import time
import datetime
import threading
import hcsr04
from weight_sensor import sensor_w

#商品を取り出すまでの待機猶予
HOLD_TIME = 5

#連続して短い時間でフラグが立つことがあるため待機する
WEIGHT_CHECK_SPAN = 2

class Client:
	def __init__(self, address, port):
		self.address = address
		self.port = port
		self.sensor = hcsr04.sensor()
		self.sensor_w = sensor_w()
		self.flag = 0
		self.stack_flag = []

	def send_img(self, sock, img):
		img_raw = img.tostring()
		size = "{}".format(len(img_raw)).encode('utf-8')
		sock.send(size)
		sock.send(img_raw)

		now = datetime.datetime.now()
		sys.stdout.write("\r[{}]send msg:{}".format(now, size))
		sys.stdout.flush()
		
	def handler(self):
		prev = time.time()
		while True:
			self.flag = self.sensor.get_flag()
			weight_flag = self.sensor_w.exe()

			#重量センサーのフラグが変化なし
			if weight_flag == 0:
				continue

			#重量センサーのフラグが変化アリ(-1 or 1) フラグ用のスタックに値を追加
			now = time.time()
			if (prev - now) > WEIGHT_CHECK_SPAN: #2秒以内に0以外のフラグが来たら誤作動の可能性があるので無視
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
			print("Flag:{} Dis:{}".format(self.flag, self.sensor.dis))
			#距離センサーに引っかかる
			if self.flag == 1:

				for i in range(6):
					ret, frame = capture.read()
					if ret == None:
						continue
					#self.send_img(sock, frame)
					data.append(frame)
					time.sleep(0.5)

				#画像を撮り終わった後に追加or削除のフラグスタックを確認する
				#フラグがあった場合
				if len(self.stack_flag) != 0:
					data.append(self.stack_flag.pop())
				#フラグがなかった場合　数秒フラグが出るのを待つ
				else:
					start = time.time()
					while True:
						end = time.time()
						if len(self.stack_flag) != 0:
							break
						if end - start > HOLD_TIME:
							break

				data.append(self.stack_flag.pop())
				#画像群とフラグのセットを送信
				#self.send_data(sock, data)



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
