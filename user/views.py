from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

from . import models

from myadmin import models as myadmin_models
from myapp import models as myapp_models

import time

media_url=settings.MEDIA_URL

# Create your views here.
def sessioncheckuser_middleware(get_response):
  def middleware(request):
    if request.path=='/user/' or request.path=='/user/viewproducts/' or request.path=='/user/subcatviewproducts/' or request.path=='/user/addproducts/' or request.path=='/user/showSubCategory/' or request.path=='/user/editprofileuser/' or request.path=='/user/showSubCategory/' or request.path=='/user/updateDataUser/':
      if request.session['sunm']==None or request.session['srole']!='user':
        response=redirect('/login/')
      else:
        response=get_response(request)
    else:
      response=get_response(request)
    return response
  return middleware
        


def userhome(request):
  return render(request,"userhome.html",{"sunm":request.session['sunm']})

def viewproducts(request):
  clist=myadmin_models.Category.objects.all()
  return render(request,"viewproducts.html",{"media_url":media_url,"clist":clist,"sunm":request.session['sunm']})

def subcatviewproducts(request):

  catnm=request.GET.get("catnm")
  sclist=myadmin_models.SubCategory.objects.filter(catnm=catnm)
  return render(request,"subcatviewproducts.html",{"media_url":media_url,"sclist":sclist,"catnm":catnm,"sunm":request.session['sunm']})

def addproducts(request):
  clist=myadmin_models.Category.objects.all()
  if request.method=="GET":
    return render(request,"addproducts.html",{"clist":clist,"sunm":request.session['sunm'],"msg":""})
  else:
    title=request.POST.get("title")
    catnm=request.POST.get("catnm")
    subcatnm=request.POST.get("subcatnm")
    baseprice=request.POST.get("baseprice")
    description=request.POST.get("description")

    file1=request.FILES['file1']        
    fs=FileSystemStorage()
    file1_nm=fs.save(file1.name,file1)

    if request.POST.get('file2')==None:
      file2=request.FILES['file2']        
      fs=FileSystemStorage()
      file2_nm=fs.save(file2.name,file2)
    else:
      file2_nm="img1.jpg"

    if request.POST.get('file3')==None:
      file3=request.FILES['file3']        
      fs=FileSystemStorage()
      file3_nm=fs.save(file3.name,file3)
    else:
      file3_nm="img1.jpg"

    if request.POST.get('file4')==None:
      file4=request.FILES['file4']        
      fs=FileSystemStorage()
      file4_nm=fs.save(file4.name,file4)
    else:
      file4_nm="img1.jpg" 
    uid=request.session['sunm']
    bstatus=0
    dt=time.time()
  
  p=models.Products(title=title,catnm=catnm,subcatnm=subcatnm,baseprice=baseprice,description=description,file1=file1_nm,file2=file2_nm,file3=file3_nm,file4=file4_nm,uid=uid,bstatus=bstatus,dt=dt)
  p.save() 
  return render(request,"addproducts.html",{"clist":clist,"sunm":request.session['sunm'],"msg":"Product added successfully"})

def showSubCategory(request):
  catnm=request.GET.get("cnm")
  sclist=myadmin_models.SubCategory.objects.filter(catnm=catnm)
  sclist_options="<option>Select SubCategory</option>"
  for row in sclist:
    sclist_options+=("<option>"+row.subcatnm+"</option>")
  return HttpResponse(sclist_options)

def editprofileuser(request):
  userDetails=myapp_models.Register.objects.filter(username=request.session['sunm'])
  return render(request,"editprofileuser.html",{"msg":"","sunm":request.session['sunm'],"userDetails":userDetails[0]})

def updateDataUser(request):
  name=request.POST.get("name")
  email=request.POST.get("username")
  mobile=request.POST.get("mobile")
  address=request.POST.get("address")
  city=request.POST.get("city")

  myapp_models.Register.objects.filter(username=email).update(name=name,mobile=mobile,address=address,city=city)
   
  return redirect("/user/editprofileuser/") 

def changepassworduser(request):
  if request.method=="GET":
      return render(request,"changepassworduser.html",{"sunm":request.session['sunm'],"msg":""})
  else:
    oldpass=request.POST.get("oldpass")
    newpass=request.POST.get("newpass")
    confirmnewpass=request.POST.get("confirmnewpass")
    userDetails=myapp_models.Register.objects.filter(username=request.session['sunm'],password=oldpass)
    
    if len(userDetails)>0:
      if newpass==confirmnewpass:
        myapp_models.Register.objects.filter(username=request.session['sunm']).update(password=confirmnewpass)
        msg="Password changed successfully , please login again"      
      else:
        msg="New & confirm new password not matched"            
    else:
      msg="Invalid old password , please try again"         
  return render(request,"changepassworduser.html",{"sunm":request.session['sunm'],"msg":msg})
  
def viewproductuser(request):
  paypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
  paypalID="sb-8y7jv4990175@business.example.com"
  pDetails=models.Products.objects.filter(uid=request.session['sunm'])
  return render(request,"viewproductuser.html",{"sunm":request.session['sunm'],"pDetails":pDetails,"media_url":media_url,"paypalURL":paypalURL,"paypalID":paypalID})

def payment(request):
    pid=request.GET.get('pid')
    price=request.GET.get('price')
    uid=request.GET.get('uid')
    dt=time.time()

    p=models.Payment(pid=int(pid),price=int(price),uid=uid,dt=dt)
    p.save()
    
    models.Products.objects.filter(pid=int(pid)).update(bstatus=1,dt=dt)
    
    return redirect("/user/viewproductuser/")

def cancel(request):
    return render(request,"cancel.html",{'sunm':request.session['sunm']})

def viewbiddingproducts(request):
    scnm=request.GET.get("scnm")
    sunm=request.session["sunm"]
    pDetails=models.Products.objects.filter(~Q(uid=sunm),subcatnm=scnm)    
    return render(request,"viewbiddingproducts.html",{'media_url':media_url,'sunm':request.session['sunm'],'pDetails':pDetails})

def bidproduct(request):
    pid=request.GET.get("pid")
    pDetails=models.Products.objects.filter(pid=int(pid))
    stime=float(pDetails[0].dt)
    ctime=time.time()
    dtime=ctime-stime
    if dtime<192800:
        bDetails=models.Bidding.objects.filter(pid=int(pid))
        if len(bDetails)>0:
            max_cprice=bDetails[0].bprice        
            for row in bDetails:
                if max_cprice<row.bprice:
                    max_cprice=row.bprice
            cprice=max_cprice
        else:
            cprice=pDetails[0].baseprice                
        s=1    
    else:
        s=0
        cprice=None
    return render(request,"bidproduct.html",{'pDetails':pDetails,'sunm':request.session['sunm'],'s':s,'cprice':cprice})

def mybid(request):
    pid=request.POST.get('pid')
    bprice=request.POST.get('bprice')
    uid=request.session['sunm']
    dt=time.asctime()

    p=models.Bidding(pid=int(pid),bprice=int(bprice),uid=uid,dt=dt)
    p.save()
    
    return redirect('/user/bidproduct/?pid='+str(pid))   

def viewbid(request):
  pid = request.GET.get("pid")
  bDetails=models.Bidding.objects.filter(pid=int(pid))
  return render(request,"viewbid.html",{'bDetails':bDetails,'sunm':request.session['sunm']})