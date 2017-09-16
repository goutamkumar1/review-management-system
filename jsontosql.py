import json
import MySQLdb
from pprint import pprint
testfile=open("data.json")
data=json.load(testfile)
#usrdata= data[0]
#connect to db
db = MySQLdb.connect("localhost","root","root","testdb" ) 
#setup cursor
cursor = db.cursor()
 
#create prodinfo table
cursor.execute("DROP TABLE IF EXISTS prodinfo")
sql = """CREATE TABLE prodinfo (
		 id INT AUTO_INCREMENT PRIMARY KEY,
         name VARCHAR(200),  
         url VARCHAR(50),
         price VARCHAR(20),
         5star VARCHAR(20),
         4star VARCHAR(20),
         3star VARCHAR(20),
         2star VARCHAR(20),
         1star VARCHAR(20) )"""

cursor.execute(sql)

#create reviewinfo table
cursor.execute("DROP TABLE IF EXISTS reviewinfo")
newsql = """CREATE TABLE reviewinfo (
		 rid INT AUTO_INCREMENT PRIMARY KEY,
         name VARCHAR(200),  
         rhead VARCHAR(200),
         rtext VARCHAR(10000),
         rcommentcount VARCHAR(10),
         rdate VARCHAR(20),
         rrating VARCHAR(10),
         rauthor VARCHAR(50) )"""

cursor.execute(newsql)

#data filling
for j in range(2):
	usrdata=data[j]
	usrreview=usrdata["reviews"]
	usrrating=usrdata["ratings"]
	usrprice=usrdata["price"]
	usrurl=usrdata["url"]
	usrname=usrdata["name"]

	#insert to table
	try:
	    cursor.execute("""INSERT INTO prodinfo(name,url,price,5star,4star,3star,2star,1star) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(usrname,usrurl,usrprice,usrrating["5 star"],usrrating["4 star"],usrrating["3 star"],usrrating["2 star"],usrrating["1 star"]))

	    db.commit()
	except:     
	    db.rollback()

	l=len(usrreview)
	for i in range(l):
		sreview=usrreview[i]
		rh=sreview["review_header"]
		rt=sreview["review_text"]
		rcc=sreview["review_comment_count"]
		rpd=sreview["review_posted_date"]
		rr=sreview["review_rating"]
		ra=sreview["review_author"]
		#insert to table
		try:
		    cursor.execute("""INSERT INTO reviewinfo(name,rhead,rtext,rcommentcount,rdate,rrating,rauthor) VALUES (%s,%s,%s,%s,%s,%s,%s)""",(usrname,rh,rt,rcc,rpd,rr,ra))

		    db.commit()
		except:     
		    db.rollback()
		




#insert to table
#try:
#    cursor.execute("""INSERT INTO anooog1 VALUES (%s,%s)""",(188,90))
#    db.commit()
#except:     
#    db.rollback()
#show table
#cursor.execute("""SELECT * FROM prodinfo;""")
#print cursor.fetchall()
db.close()