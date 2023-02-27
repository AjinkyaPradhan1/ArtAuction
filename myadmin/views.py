from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from myapp import models as myapp_models
from . import models

def sessioncheckmyadmin_middleware(get_response):
  def middleware(request):
    if request.path=='/myadmin/' or request.path=='/myadmin/manageusers/' or request.path=='/myadmin/addcategory/' or request.path=='/myadmin/addsubcategory/':
      if request.session['sunm']==None or request.session['srole']!='admin':
        response=redirect('/login/')
      else:
        response=get_response(request)
    else:
      response=get_response(request)
    return response
  return middleware


# Create your views here.

def adminhome(request):
  return render(request,"adminhome.html",{"sunm":request.session['sunm']})

def manageusers(request):
  userDetails=myapp_models.Register.objects.filter(role="user")
  
  return render(request,"manageusers.html",{"userDetails":userDetails,"sunm":request.session['sunm']})

def manageuserstatus(request):
  s=request.GET.get("s")
  regid=request.GET.get("regid")
  
  if s=="block":
    myapp_models.Register.objects.filter(regid=regid).update(status=0)
  elif s=="verify":
    myapp_models.Register.objects.filter(regid=regid).update(status=1)
  else:
    myapp_models.Register.objects.filter(regid=regid).delete()

  return redirect('/myadmin/manageusers/')

  #return render(request,"manageuserstatus.html",{})

def addcategory(request):
  if request.method=="GET":
    return render(request,"addcategory.html",{"msg":"","sunm":request.session['sunm']})
  else:
    catnm=request.POST.get("catnm")
    clist=models.Category.objects.filter(catnm=catnm)
  if len(clist)>0:
   return render(request,"addcategory.html",{"msg":"Category already exists please try again.....","sunm":request.session['sunm']})
  else:
    caticon=request.FILES["caticon"]
    fs=FileSystemStorage()
    caticonnm=fs.save(caticon.name,caticon)
    p=models.Category(catnm=catnm,caticonnm=caticonnm)
    p.save()
    return render(request,"addcategory.html",{"msg":"Category Added successfully","sunm":request.session['sunm']})

def addsubcategory(request):
  catlist=models.Category.objects.all()
  if request.method=="GET":
    return render(request,"addsubcategory.html",{"msg":"","catlist":catlist,"sunm":request.session['sunm']})
  else:
    catnm=request.POST.get("catnm")
    subcatnm=request.POST.get("subcatnm")
    sclist=models.SubCategory.objects.filter(subcatnm=subcatnm)
  if len(sclist)>0:
   return render(request,"addsubcategory.html",{"msg":"Sub category already exists please try again.....","clist":clist,"sunm":request.session['sunm']})
  else:
    caticon=request.FILES["caticon"]
    fs=FileSystemStorage()
    subcaticonnm=fs.save(caticon.name,caticon)
    p=models.SubCategory(catnm=catnm,subcatnm=subcatnm,subcaticonnm=subcaticonnm)
    p.save()
    return render(request,"addsubcategory.html",{"msg":"Sub Category Added successfully","catlist":catlist,"sunm":request.session['sunm']})