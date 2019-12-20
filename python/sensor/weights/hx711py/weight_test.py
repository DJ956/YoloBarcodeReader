import sys
from weight_sensor import sensor_w

def main():
	sensor = sensor_w()

	while True:
		flag = sensor.exe()
		print("Flag:{} Val:{}".format(flag, sensor.val))

if __name__ == "__main__":
	main()