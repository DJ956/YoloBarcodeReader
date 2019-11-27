
with open("log.txt", "r") as f:
	cnt = 1
	line = f.readline()
	sum = float(line)
	while line:
		print(line.strip())
		sum = sum + float(line.strip())
		line = f.readline()
		cnt = cnt + 1

	avg = sum / cnt
	print("AVG:{}".format(avg))
