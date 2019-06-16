from django.http import HttpResponse
from django.shortcuts import render
from . import sys_login

lg = sys_login.moni_login()

def student_login(schoolid,psw):
    lg = sys_login.moni_login()
    lg.cookied_get()
    lg.get_yzm()
    lg.login(schoolid,psw)


def login(request):


    if request.method=="GET":
        cookie=lg.cookied_get()
        yzm=lg.get_yzm(cookie)
        yzm1 = {"yzm": yzm, "cookie": cookie}
        return render(request, 'login.html',yzm1)
    '''
    if request.method=="GET":
        yzml={'yzm':2e56}
        return render(request, 'login.html',yzml)
    '''

    if request.method=="POST":
        schoolid=request.POST.get("schoolid")
        psw = request.POST.get("psw")
        yzm1 = request.POST.get("yzm")
        cookie = request.POST.get("cookie")
        getxf="http://127.0.0.1:8080/getxf?cookie="+str(cookie)
        print(cookie)
        loginfh=lg.login(schoolid, psw,yzm1,cookie)
        if loginfh=="ok":
            cjdata=lg.get_cj(cookie)
            cjlist=cjdata
            xm = cjlist['rows'][1]['xsxm']
            jd = lg.js(cjlist)
            zxf = lg.xstsjs(cjlist)
            txf = str(zxf[0]) + '/' + str(zxf[1])
            cjlist.update({'jd': jd})
            cjlist.update({'user': xm})
            cjlist.update({'xtxf': txf})
            cjlist.update({'gxfurl': getxf})
            return render(request, 'index.html',cjlist)
        else:
            return render(request, 'hello.html')








        '''
        res=lg.login(schoolid,psw,yzm1)
        if res=="ok":
            lg.get_cj()
            return render(request, 'index.html')

        else:
            lg = sys_login.moni_login()
            lg.cookied_get()
            yzm = lg.get_yzm()
            false={"false_info":yzm}
            return render(request, 'login.html', false)
        '''


def getxf(request):
    if request.method=="GET":
        cookie = request.GET.get("cookie")
        zxf = lg.getxf(cookie)
        return render(request, 'getxf.html', zxf)


    if request.method=="POST":
        return render(request, 'hello.html')








