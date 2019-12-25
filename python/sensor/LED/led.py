import RPi.GPIO as GPIO
import time
import threading

class notice_sensor:

	def __init__(self):
		self.green = 21
		self.blue = 20
		self.red = 16
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.green, GPIO.OUT)
		GPIO.setup(self.blue, GPIO.OUT)
		GPIO.setup(self.red, GPIO.OUT)


	def job(self, color):
		if color == self.green:
			GPIO.output(color, GPIO.HIGH)
			time.sleep(3)
			GPIO.output(color, GPIO.LOW)
		elif color == self.blue:
			for i in range(3):
				GPIO.output(color, GPIO.HIGH)
				time.sleep(0.5)
			GPIO.output(color, GPIO.LOW)
		elif color == self.red:
			for i in range(3):
				GPIO.output(color, GPIO.HIGH)
				time.sleep(0.5)
			GPIO.output(color, GPIO.LOW)


	def shine(self, color):
		work = threading.Thread(target=job, args=([color]))
		work.start()

