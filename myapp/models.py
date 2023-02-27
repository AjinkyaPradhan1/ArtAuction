from django.db import models

class Register(models.Model):
    regid = models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=10)
    address=models.CharField(max_length=1000)
    mobile=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    status=models.IntegerField()
    role=models.CharField(max_length=20)
    dt=models.CharField(max_length=1000)