import sys
from weight_sensor import sensor_w

def main():
	sensor = sensor_w()

	while True:
		flag = sensor.exe()
		print("Flag:{} Val:{} g_weight:{}".format(flag, sensor.val, sensor.g_weight))

if __name__ == "__main__":
	main()