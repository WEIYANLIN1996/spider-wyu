$(document).ready(function () {
    $(".dropdown").mouseenter(function () {
        $(this).children("ul").show();
    });
    $(".dropdown").mouseleave(function () {
        $(this).children("ul").hide();
    });
    $(".dropdown-menu li").click(function(){
    	var text=$(this).text();
    	$(".dropdown-toggle").empty();
    	$(".dropdown-toggle").append(text);
    })
    $("#three").click(function(){
    	var xlist=[];
    	var tslist=[];
    	var xsum=0;
    	var tsum=0;
    	$('.list-group').find('li').each(function() {
    		var kclb=$(this).find(".kb").text();
            var xf=$(this).find(".xf1").text();
            if(String(kclb)=="选修") {
            	xlist.push(xf);
                
            }
            if(String(kclb)=="通识"){
            	tslist.push(xf);
                
            }
            
        })
    	var l=xlist.length
    	console.log(l);
    	for (i=0;i<=l-1;i++){
    		ss=String(xlist[i]);
    		xsum=xsum+Number(ss);
    		console.log(xsum);		    		
    		
    	}
    	var tl=tslist.length
    	console.log(l);
    	for (i=0;i<=tl-1;i++){
    		ss=String(tslist[i]);
    		tsum=tsum+Number(ss);
    		console.log(tsum);		    		
    		
    	}
        alert("选修学分:"+String(xsum)+"     "+"通识学分:"+String(tsum));
    
    })
    $("#one").click(function(){

    	var xflist=[];
    	var fslist=[];
    	var xjsum=0;
    	var xfsum=0;
    	$(".list-group").find("li").each(function(){		    		
            var xf=$(this).find(".xf1").text();
            var fs=$(this).find(".cj1").text();
            xflist.push(xf);
            fslist.push(fs);
            console.log(xflist);
    	})
    	var l=xflist.length
    	console.log(l);
    	for (i=0;i<=l-1;i++){
    		xfs=String(xflist[i]);
    		fss=String(fslist[i]);
    		xfsum=xfsum+Number(xfs);
    		xjsum=xjsum+Number(xfs)*Number(fss);
    		console.log(xjsum);		    		
    		
    	}
    	var jd=xjsum/xfsum;
    	if (jd>=0&&jd<60){
    		alert("成绩："+String(jd)+" 绩点小于1.0");
    	}
    	if (jd>=60&&jd<70){
    		jd=jd-60;
    		jd=1.0+jd*0.1;
    		
    	}
    	
    	if (jd>=70&&jd<80){
    		jd=jd-70;
    		jd=1.0+jd*0.1;
    		
    	}
    	if (jd>=80&&jd<90){
    		jd=jd-80;
    		jd=1.0+jd*0.1;
    		
    	}
    	if (jd>=90&&jd<100){
    		jd=jd-90;
    		jd=1.0+jd*0.1;
    		
    	}
    	
    	alert("绩点："+String(jd));
    })
})
		