import time
def ikuntime(hour1,minute1):
	kunhour = hour1 // 2.5
	a = hour1 % 2.5
	b = a * 60 + minute1
	kunminute = b // 2.5
	if kunminute >= 60:
		kunminute -= 60
		kunhour += 1

	print("输出时间：" + str(kunhour) + "坤时" , str(kunminute) + "坤分" )
	time.sleep(5)
	exit()
