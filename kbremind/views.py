from django.shortcuts import render
from django.http import HttpResponse
from . import syslogin
import json
from . import wctx
import threading
# Create your views here.


lg = syslogin.moni_login()

def getkb_login(request):
    if request.method=="GET":
        cookie=lg.cookied_get()
        yzm=lg.get_yzm(cookie)
        yzm = {"yzm": yzm,"cookie":cookie}
        return render(request,'getkb.html',yzm)


def getkb_tj(request):
    if request.method=="POST":
        xh=request.POST.get("xh")
        psw = request.POST.get("pass")
        yzm1 = request.POST.get("yzm")
        cookie = request.POST.get("cookie")
        print(cookie)
        loginfh=lg.login(xh, psw,yzm1,cookie)
        objext=wctx.wcremind()
        kbjudge=objext.judge(xh)
        print(kbjudge)
        if kbjudge=="exit":
            return render(request,'getsus.html')
        else:
            if loginfh=="ok":
                fh=lg.getkb(xh,cookie)
                print(fh)
                if fh=="true":
                    return render(request, 'getsus.html')
                if fh=="false":
                    xyfh={"error":1,"falseinfo":"下载课表失败"}
                    return HttpResponse(json.dumps(xyfh), content_type="application/json")
            else:
                xyfh = {"error": 1,"falseinfo":"无法登录系统"}
                return HttpResponse(json.dumps(xyfh), content_type="application/json")
    else:
        xyfh = {"error": 1, "falseinfo": "无法登录系统"}
        return HttpResponse(json.dumps(xyfh), content_type="application/json")


def remindkq(request):
    if request.method=="GET":
        schoolid = request.GET.get("xh")
        sekey = request.GET.get("sekey")
        info = request.GET.get("info")
        print(sekey)
        if info=='kq':
            wctxfh=wctx.wcremind()
            fh=wctxfh.judgerun(schoolid,sekey)
            if fh=="no":
                wctxfh.insert(schoolid,sekey)
                hd=wctxfh.kqsend(schoolid,sekey)
                print(hd)
                #kqxy = {"error": 0}
                #return HttpResponse(json.dumps(kqxy), content_type="application/json")
            else:
                hd=wctxfh.kqsend(schoolid, sekey)
                print(hd)
                #kqxy = {"error": 0}
                #return HttpResponse(json.dumps(kqxy), content_type="application/json")
        elif info=='gb':
            kqxy = {"error":0}
            return HttpResponse(json.dumps(kqxy), content_type="application/json")
        else:
            kqxy = {"error":1}
            return HttpResponse(json.dumps(kqxy), content_type="application/json")
    else:
        kqxy = {"error":1}
        return HttpResponse(json.dumps(kqxy), content_type="application/json")



def remindgb(request):

    return render(request, 'kbremind.html')