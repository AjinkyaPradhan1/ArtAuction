from django.db import models

# Create your models here.

class Products(models.Model):
    pid = models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    catnm=models.CharField(max_length=50)
    subcatnm=models.CharField(max_length=50)
    baseprice=models.IntegerField()
    description=models.CharField(max_length=1000)
    file1=models.CharField(max_length=100)
    file2=models.CharField(max_length=100)
    file3=models.CharField(max_length=100)
    file4=models.CharField(max_length=100)
    uid=models.CharField(max_length=100)
    bstatus=models.IntegerField()
    dt=models.CharField(max_length=1000)

class Payment(models.Model):
    txnid = models.AutoField(primary_key=True)
    pid=models.IntegerField()
    price=models.IntegerField()
    uid=models.CharField(max_length=100)
    dt=models.CharField(max_length=1000) 


class Bidding(models.Model):
    bid = models.AutoField(primary_key=True)
    pid=models.IntegerField()
    bprice=models.IntegerField()
    uid=models.CharField(max_length=100)
    dt=models.CharField(max_length=1000) 
    
    
   
