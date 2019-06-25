import pymysql
import datetime
import paramiko
import json


# DB 연결
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="Dlwlrma0516!",
                     db="test")

cur = db.cursor()

#Json 파일 읽어서 변수에 저장
with open('/home/ec2-user/bum/graduation-portfolio/autoDb/raspDb.json') as json_data:
	data = json.load(json_data)

	list=data[0]
	pm10=list["pm10"]
	pm25=list["pm25"]
	latitude=list["latitude"]
	longitude=list["longitude"]

#UPDATE 쿼리
sql="update raspGpsPmValue set pm10=%s,pm25=%s,latitude=%s,longitude=%s"
pm10=int(pm10)
pm25=int(pm25)
latitude=float(latitude)
longitude=float(longitude)


#쿼리 실행
cur.execute(sql,(pm10,pm25,latitude,longitude))
db.commit()


#DB 종료
db.close()

