import urllib.request
from . import ShowapiRequest
import http.cookiejar
from pyquery import PyQuery as pq
import re
import mysql.connector
import time
import json




class moni_login():

    def cookied_get(self):

        cjar=http.cookiejar.CookieJar()
        #使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
        cookies=urllib.request.HTTPCookieProcessor(cjar)
        opener=urllib.request.build_opener(cookies)

        url = 'http://202.192.240.29/'
        opener.open(url)

        for item in cjar:
            print(item.name)
            print(item.value)
            cookie = item.name+"="+item.value

        #将opener安装为全局
        print(cookie)
        return cookie

        '''
        self.header = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; ?) Gecko/20100101 Firefox/60.0',
            'Referer': 'http://jmva.jiangmen.gov.cn/JmygWeb/member/memberLogin.do',
            'Cookie': cookie
        }
        urllib.request.install_opener(opener)
        
        
        req1 = urllib.request.Request(url, headers=self.header)
        
        try:
            reponse=urllib.request.urlopen(req1)
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.reason)
        '''

    # 验证码
    def get_yzm(self,cookie):

        header = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; ?) Gecko/20100101 Firefox/60.0',
            'Referer': 'http://jmva.jiangmen.gov.cn/JmygWeb/member/memberLogin.do',
            'Cookie': cookie
        }

        url2 = "http://202.192.240.29/yzm?"
        self.req2 = urllib.request.Request(url2, headers=header)
        check = urllib.request.urlopen(self.req2)
        result = check.read()
        fy = open('static/img/code.jpg', 'wb')
        fy.write(result)
        fy.close()

        r = ShowapiRequest.ShowapiRequest("http://route.showapi.com/184-4", "74292", "360efa90aede459388dc608c18a166b1")
        r.addFilePara("image", r"static/img/code.jpg")
        r.addBodyPara("typeId", "34")
        r.addBodyPara("convert_to_jpg", "0")
        r.addBodyPara("needMorePrecise", "1")  # 文件上传时设置
        res = r.post()
        yzmjs = eval(res.text)
        rescode = yzmjs["showapi_res_code"]
        if rescode == 0:
            yzm1 = yzmjs["showapi_res_body"]["Result"]

        else:
            print("验证码识别失败请刷新！")

        return yzm1

    #登录
    def login(self,schoolid,psw,yzm,cookie):

        header = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; ?) Gecko/20100101 Firefox/60.0',
            'Referer': 'http://jmva.jiangmen.gov.cn/JmygWeb/member/memberLogin.do',
            'Cookie': cookie
        }
        data = {
                'account': schoolid,
                'pwd': psw,
                'verifycode':yzm
        }
        postdata=urllib.parse.urlencode(data).encode('utf8')

        url3 = "http://202.192.240.29/new/login"
        req3=urllib.request.Request(url3,postdata,headers=header)
        res3=urllib.request.urlopen(req3)
        text=res3.read().decode()
        text=json.loads(text)
        print(text)
        falseinfo="nologin"
        trueinfo="ok"
        if text['message']=="登录成功":
            url4= "http://202.192.240.29/login!welcome.action"
            req4= urllib.request.Request(url4, headers=header)
            urllib.request.urlopen(req4)
            return trueinfo
        if text=="":
            return trueinfo

        else:
            return falseinfo


    def get_cj(self):
        data = {
            'order': 'asc',
            'page': '1',
            'rows': '20',
            'sort': 'xnxqdm',
            'xnxqdm': '201801'
        }
        getcj_data = urllib.parse.urlencode(data).encode('utf8')
        url5 = "http://202.192.240.29/xskccjxx!getDataList.action"
        req5=urllib.request.Request(url5, getcj_data, headers=self.header)
        cj_data=urllib.request.urlopen(req5)
        cjdata=eval(cj_data.read().decode())
        print(cjdata)
        return cjdata


    def js(self, chengji):
        zf = 0
        xfh = 0
        ld = chengji['total']
        for d in range(0, ld):
            xf = float(chengji["rows"][d]["xf"])
            if chengji["rows"][d]["zcj"] == "优良":
                cj = 85
            elif chengji["rows"][d]["zcj"] == "优秀":
                cj = 95
            elif chengji["rows"][d]["zcj"] == "中等":
                cj = 75
            elif chengji["rows"][d]["zcj"] == "及格":
                cj = 60
            else:
                cj = float(chengji["rows"][d]["zcj"])
            zf = zf + cj * xf
            xfh = xfh + xf
        jd = zf / xfh
        xs = (jd % 10) * 0.1
        xs=round(xs,3)
        if jd < 60:
            jd="你的绩点低于2.0"
        elif jd >= 60 and jd < 70:
            jd=str(1 + xs)
        elif jd >= 70 and jd < 80:
            jd=str(2 + xs)
        elif jd >= 80 and jd < 90:
            jd=str(3 + xs)
        else:
            jd=str(3 + xs)
        return jd

    def xstsjs(self,chengji):
        xxf = 0
        tsxf = 0
        ld=chengji['total']
        for j in range(0, ld):
            if chengji["rows"][j]["xdfsmc"] == "限选":
                xxf = xxf + float(chengji["rows"][j]["xf"])
            elif chengji["rows"][j]["xdfsmc"] == "通识课":
                tsxf = tsxf + float(chengji["rows"][j]["xf"])
            else:
                continue
            print(xxf)
        xtxf=[xxf,tsxf]

        return xtxf

    def getxf(self):
        url6 = "http://202.192.240.29/xsjxjhxx!xsxxjhMain.action?jxjhdm=J08052016&jhlxdm=01&jhfxdm="
        req6 = urllib.request.Request(url6, headers=header)
        res6 = urllib.request.urlopen(req6)
        htmltext = res6.read().decode()
        doc = pq(htmltext)
        li = doc("[colspan='5']")
        namestr=doc("[width='250px']")
        name1=namestr.text()
        rule = r'姓名：(.+)'
        slotList = re.findall(rule, name1)
        textstr = li.text()
        textlist = textstr.split(" ")
        #text=['123', '\xa0\xa0必修学分：96.5', '\xa0\xa0限选学分：16.5', '\xa0\xa0通识课：10', '\xa0\xa0创新学分：0']
        xfdict={
            "zxf":textlist[0],
            "bxxf":textlist[1],
            "xxxf": textlist[2],
            "tsxf": textlist[3],
            "cxxf": textlist[4],
            "name":slotList[0],
        }
        print(slotList)
        return xfdict

    def getkb(self,xh,cookie):
        mydb = mysql.connector.connect(
            host="localhost",  # 数据库主机地址
            user="root",  # 数据库用户名
            passwd="wyl336339",  # 数据库密码
            database="kb"
        )
        mycursor = mydb.cursor()
        sql = """CREATE TABLE """+str(xh)+"""_data(
                 ZC    INT(10) NOT NULL,
                 XQ    INT(10) NOT NULL, 
                 JS    VARCHAR(50) NOT NULL,
                 KEMC  VARCHAR(200) NOT NULL,
                 DD    VARCHAR(200) NOT NULL,
                 TEACHER  VARCHAR(100) NOT NULL)"""

        mycursor.execute(sql)
        y = 1
        header = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; ?) Gecko/20100101 Firefox/60.0',
            'Referer': 'http://jmva.jiangmen.gov.cn/JmygWeb/member/memberLogin.do',
            'Cookie': cookie
        }
        while y <= 20:
            url7 = 'http://202.192.240.29/xsgrkbcx!getKbRq.action?xnxqdm=201802&zc=' + str(y)
            req7 = urllib.request.Request(url7, headers=header)
            res7 = urllib.request.urlopen(req7)
            htmltext = res7.read().decode()
            kbdata = eval(htmltext)
            for x in kbdata[0]:
                print(x['zc'] + "," + x['xq'] + "," + x['jcdm2'] + "," + x['kcmc'] + "," + x['jxcdmc'] + "," + x[
                    'teaxms'])
                sqlinsert = "INSERT INTO "+str(xh)+"_data(ZC,XQ, JS, KEMC, DD,TEACHER) VALUES (%s, %s,%s,%s,%s,%s)"
                data = (x['zc'], x['xq'], x['jcdm2'], x['kcmc'], x['jxcdmc'], x['teaxms'])
                mycursor.execute(sqlinsert, data)
                mydb.commit()
            y += 1
            time.sleep(2)

        kbxz = "true"
        return kbxz


