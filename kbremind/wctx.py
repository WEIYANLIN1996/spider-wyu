import requests
import time
#import thread
import mysql.connector

class wcremind():

    def __init__(self):
        pass

    def send(self, title, content,sekey):
        url = "https://sc.ftqq.com/"+str(sekey)+".send"
        data = {
            "text": title,
            "desp": content
        }
        req = requests.post(url, data=data)
        textfh = eval(req.text)
        if textfh["errno"] == 0:
            print('发送成功！')
        else:
            print('发送失败！' + textfh)

    def getzc(self):
        week = 1
        month = str(time.strftime("%b", time.localtime()))
        day = int(time.strftime("%d", time.localtime()))
        if month == "Feb":
            if day >= 24 and day <= 28:
                week = 1
            else:
                week = 1

        elif month == "Mar":
            if day <= 2:
                week = 1
            elif day >= 3 and day <= 9:
                week = 2
            elif day >= 10 and day <= 16:
                week = 3
            elif day >= 17 and day <= 23:
                week = 4
            elif day >= 24 and day <= 30:
                week = 5
            else:
                week = 6

        elif month == "Apr":
            if day <= 6:
                week = 6
            elif day >= 7 and day <= 13:
                week = 7
            elif day >= 14 and day <= 20:
                week = 8
            elif day >= 21 and day <= 27:
                week = 9
            else:
                week = 10

        elif month == "May":
            if day <= 4:
                week = 10
            elif day >= 5 and day <= 11:
                week = 11
            elif day >= 12 and day <= 18:
                week = 12
            elif day >= 19 and day <= 25:
                week = 13
            else:
                week = 14

        elif month == "June":
            if day == 1:
                week = 14
            elif day >= 2 and day <= 8:
                week = 15
            elif day >= 9 and day <= 15:
                week = 16
            elif day >= 16 and day <= 22:
                week = 17
            elif day >= 23 and day <= 29:
                week = 18
            else:
                week = 19
        elif month == "July":
            if day <= 6:
                week = 19
            else:
                week = 20

        else:
            week = 1
        return week

    def getxq(self):
        a = time.strftime("%a", time.localtime())
        xq = ""
        if a == "Mon":
            xq = "1"
        elif a == "Tue":
            xq = "2"
        elif a == "Wed":
            xq = "3"
        elif a == "Thu":
            xq = "4"
        elif a == "Fri":
            xq = "5"
        elif a == "Sat":
            xq = "6"
        elif a == "Sun":
            xq = "7"
        return xq

    def wxrun(self,xh,sekey):
        kblist=[]
        cs=1
        dayzc = str(self.getzc())
        dayxq = self.getxq()
        mydb = mysql.connector.connect(
            host="localhost",  # 数据库主机地址
            user="root",  # 数据库用户名
            passwd="wyl336339",  # 数据库密码
            database="kb",
            charset='utf8'
        )
        mycursor = mydb.cursor()
        selectkb = "SELECT * FROM " + str(xh) + "_data WHERE ZC =" + dayzc + " AND XQ=" + dayxq
        mycursor.execute(selectkb)
        myresult = mycursor.fetchall()
        if myresult == []:
            title = "课表提醒开启成功，今日没课哦"
            content = "没课也要记得学习哦"
            self.send(title, content, sekey)
        else:
            for x in myresult:
                jl = str(x[2]) + "节" + " " + str(x[3]) + " " + str(x[4]) + "," + str(x[5])
                kblist.append(jl)
                cs += 1
                print(x)
            title = "课表提醒开启成功，今日有" + str(cs) + "节课哦"
            content = " ".join(kblist)
            self.send(title, content, sekey)
        while True:
            cs = 1
            kblist = []
            todayhour = time.strftime("%H", time.localtime())
            todaymin = time.strftime("%M", time.localtime())
            todaysec = time.strftime("%S", time.localtime())
            print(todayhour + "," + todaymin + todaysec)
            if str(todayhour) == '7' and str(todaymin) == '01' and str(todaysec) == '00':
                dayzc = str(self.getzc())
                dayxq = self.getxq()
                mydb = mysql.connector.connect(
                    host="localhost",  # 数据库主机地址
                    user="root",  # 数据库用户名
                    passwd="wyl336339",  # 数据库密码
                    database="kb",
                    charset='utf8'
                )
                mycursor = mydb.cursor()
                selectkb = "SELECT * FROM "+str(xh)+"_data WHERE ZC =" + dayzc + " AND XQ=" + dayxq
                mycursor.execute(selectkb)
                myresult = mycursor.fetchall()
                if myresult == []:
                    title = "今日没课哦"
                    content = "没课也要记得学习哦"
                    self.send(title, content,sekey)
                    time.sleep(86100)

                    continue
                else:
                    for x in myresult:
                        jl = str(x[2]) + "节" + " " + str(x[3]) + " " + str(x[4]) + "," + str(x[5])
                        kblist.append(jl)
                        cs += 1
                        print(x)
                title = "今日有" + str(cs) + "节课哦"
                content = " ".join(kblist)
                self.send(title, content,sekey)
                time.sleep(86100)
            else:
                continue

    def judge(self,xh):
        mydb = mysql.connector.connect(
            host="localhost",  # 数据库主机地址
            user="root",  # 数据库用户名
            passwd="wyl336339",  # 数据库密码
            database="kb"
        )
        mycursor = mydb.cursor()
        sltable="SHOW TABLES"
        mycursor.execute(sltable)
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
            if x[0] == str(xh) + "_data":
                return ("exit")
            else:
                print("noexit")

    def judgerun(self,xh,key):
        mydb=mysql.connector.connect(
            host="localhost",  # 数据库主机地址
            user="root",  # 数据库用户名
            passwd="wyl336339",  # 数据库密码
            database="kb"
        )
        mycursor = mydb.cursor()
        sqllan="SELECT * FROM xh_key WHERE schoolid =" + xh
        mycursor.execute(sqllan)
        myresult = mycursor.fetchall()
        if myresult == []:
            runjudge = "no"
            return runjudge
        else:
            runjudge = "yes"
            return runjudge

    def insert(self,xh,key):
        mydb=mysql.connector.connect(
            host="localhost",  # 数据库主机地址
            user="root",  # 数据库用户名
            passwd="wyl336339",  # 数据库密码
            database="kb"
        )
        mycursor = mydb.cursor()
        sqlinsert="INSERT INTO  xh_key(schoolid,sekey) VALUES (%s, %s)"
        data = (xh,key)
        mycursor.execute(sqlinsert,data)
        mydb.commit()

    def kqsend(self,xh,key):
        mydb = mysql.connector.connect(
            host="localhost",  # 数据库主机地址
            user="root",  # 数据库用户名
            passwd="wyl336339",  # 数据库密码
            database="kb"
        )
        mycursor = mydb.cursor()
        sqlsend = "SELECT * FROM xh_key WHERE schoolid =" + xh
        mycursor.execute(sqlsend)
        myresult = mycursor.fetchall()
        if myresult == []:
            fh="no"
            return fh
        else:
            title = "微信课表提醒开启成功"
            content = "微信课表提醒开成功，每天七点提醒你哦"
            self.send(title, content, key)
            fh = "send"
            return fh




