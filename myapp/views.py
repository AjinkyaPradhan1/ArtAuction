#url ROUTING---->IT IS USED TO REDIRECT FROM ONE uRL TO THE OTHER uRL
#we cannot go from one viw to other view, we have to go to url from one view to connect other kind of view
#url routing can be done on the basis of method checking and path checking

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from .import models

from .import emailAPI

import time
dt=time.asctime()

def sessioncheck_middleware(get_response):
     def middleware(request):
          if request.path=='/login/':
               request.session['sunm']=None
               request.session['srole']=None
               response=get_response(request)
          else:
               response=get_response(request)
          return response
     return middleware

def home(request):
    return render(request,"home.html",{}) 

def about(request):
     return render(request,"about.html",{})

def contact(request):
     return render(request,"contact.html",{})


def service(request):
     return render(request,"service.html",{})

def register(request):
     if request.method=="GET":
          return render(request,"register.html",{'msg':''})
     else:
          name=request.POST.get("name")
          username=request.POST.get("username")
          password=request.POST.get("password")
          mobile=request.POST.get("mobile")
          address=request.POST.get("address")
          city=request.POST.get("city")
          gender=request.POST.get("gender")
          p=models.Register(name=name,username=username,password=password,address=address,mobile=mobile,city=city,status=0,role="user",dt=dt)
          p.save()
          emailAPI.sendEmail(username,password)
          return render(request,"register.html",{'msg':'Registration done successfully'})


def login(request):
     if request.method=="GET":
          return render(request,"login.html",{'msg':''})
     else:
          email=request.POST.get("email")
          password=request.POST.get("password")

          userDetails=models.Register.objects.filter(username=email,password=password,status=1)
          if len(userDetails)>0:
               request.session['sunm']=userDetails[0].username
               request.session['srole']=userDetails[0].role
               if userDetails[0].role=="user":
                    return redirect("/user/")
               else:
                    return redirect("/myadmin/")
          else:
               return render(request,"login.html",{'msg':'Invalid user,Please try again!!!!'})
