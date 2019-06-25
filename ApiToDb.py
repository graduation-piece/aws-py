#!/bin/bash

import datetime
import urllib
import urllib.request
import json
from pprint import pprint
import pymysql


# DB 연결
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="Dlwlrma0516!",
                     db="test")

cur = db.cursor()


#cur.execute("select * from cityPmValue")

# 오픈API / JSON 파싱
encText = urllib.parse.quote("서울")
ServiceKey = "vAaO3c%2BYkbBEM3PCSlGsVWCIWlC8bHqDPmKkt18F4tx8w%2FJ2SHjg7xl0ylBcxl99kqpGzu2wx9734hzkAdMLjQ%3D%3D"
url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey="+ServiceKey+"&numOfRows=25&pageNo=1&sidoName="+encText+"&searchCondition=DAILY&_returnType=json"
request = urllib.request.Request(url)
response = urllib.request.urlopen(request) 
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    #print(response_body.decode('utf-8'))
    dict = json.loads(response_body.decode('utf-8'))
    #pprint(dict) # 이게 json 데이터 인듯
else:
    print("Error Code:" + rescode)


json_array = dict["list"]

for i in range(0,25):
	obj=json_array[i]
	cityName=obj["cityName"]
	pm25=obj["pm25Value"]
	pm10=obj["pm10Value"]

	# 값이 빈칸(-)가 일때는 파싱하지 않게함
	if pm25==None or pm25=="" :
		pm25="0"
		sql="UPDATE cityPmValue SET pm10Value=%s where cityName=%s"
		if pm10==None or pm10.strip() is "":
 			continue
		else:
			int(pm10)
			cur.execute(sql,(pm10,cityName))
	else:
		int(pm25)
		if pm10==None or pm10.strip() is "":
			pm10="0"
			sql="UPDATE cityPmValue SET pm25Value=%s where cityName=%s"
			cur.execute(sql,(pm25,cityName))
		else:
			int(pm10)
			sql="UPDATE cityPmValue SET pm10Value=%s,pm25Value=%s where cityName=%s"
			cur.execute(sql,(pm10,pm25,cityName))
	db.commit()
db.close()
